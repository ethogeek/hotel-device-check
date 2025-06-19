from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
from enum import Enum
from io import StringIO
import csv
import os
import boto3

# App initialization
app = FastAPI(
    title="Device Lifecycle API",
    description="Track network device models, EOL/EOS data, and manage device records",
    version="1.0.0"
)

# S3 client setup
AWS_S3_BUCKET = os.getenv("S3_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_S3_PREFIX = os.getenv("S3_PHOTO_PREFIX", "device-photos")
s3_client = boto3.client("s3")

# Enum for device approval
class ApprovalState(str, Enum):
    pending = "pending"
    published = "published"

# Dummy User and Device classes (replace with real models)
class User:
    username: str
    role: str

class Device:
    id: str
    name: str
    manufacturer: str
    model: str
    eos_date: Optional[str]
    eol_date: Optional[str]
    life_status: Optional[str]
    notes: Optional[str]
    photo: Optional[str]
    approval_state: ApprovalState
    created_by: str

# Dummy dependency functions
def get_db():
    pass

def require_role(role: str):
    def role_checker(user: User = Depends(lambda: User(username="demo", role=role))):
        return user
    return role_checker

# ---------------------------------------------------------------------------
# 🔄 Delete Device and Photo from S3
# ---------------------------------------------------------------------------
@app.delete('/device/{did}', status_code=204, tags=['device'])
async def delete_device(did: str, db: Session = Depends(get_db), admin: User = Depends(require_role('admin'))):
    device = db.query(Device).filter(Device.id == did).first()
    if not device:
        raise HTTPException(status_code=404, detail='Device not found')

    if device.photo and device.photo.startswith(f"https://{AWS_S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{AWS_S3_PREFIX}/"):
        s3_key = device.photo.split(f".amazonaws.com/")[-1]
        try:
            s3_client.delete_object(Bucket=AWS_S3_BUCKET, Key=s3_key)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete image from S3: {str(e)}")

    db.delete(device)
    db.commit()
    return JSONResponse(status_code=204, content={})

# ---------------------------------------------------------------------------
# 📥 CSV Upload Endpoint
# ---------------------------------------------------------------------------
@app.post("/admin/device/upload-csv", tags=["device"])
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Invalid file type")
    content = await file.read()
    reader = csv.DictReader(StringIO(content.decode("utf-8")))
    count = 0
    for row in reader:
        try:
            device = Device(
                name=row['name'],
                manufacturer=row['manufacturer'],
                model=row['model'],
                eos_date=row['eos_date'],
                eol_date=row['eol_date'],
                life_status=row['life_status'],
                notes=row.get('notes', ''),
                photo=row.get('photo', ''),
                approval_state=ApprovalState.published,
                created_by=current_user.username
            )
            db.add(device)
            count += 1
        except Exception:
            continue
    db.commit()
    return {"imported": count}

# ---------------------------------------------------------------------------
# 📤 CSV Download Endpoint
# ---------------------------------------------------------------------------
@app.get("/admin/device/download-csv", tags=["device"])
async def download_csv(db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    def iter_csv():
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "name", "manufacturer", "model", "eos_date", "eol_date", "life_status", "approval_state", "created_by", "notes", "photo"])
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)
        for device in db.query(Device).all():
            writer.writerow([
                device.id, device.name, device.manufacturer, device.model,
                device.eos_date, device.eol_date,
                device.life_status, device.approval_state, device.created_by, device.notes or "", device.photo or ""
            ])
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)
    return StreamingResponse(iter_csv(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=device_export.csv"})
