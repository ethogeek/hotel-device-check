# Device Lifecycle API

A FastAPI application to manage and track network device models, including EOL (End-of-Life) and EOS (End-of-Sale) dates. Supports role-based access, SSO, image uploads to S3, and CSV data handling.

---

## 🚀 Features

- OAuth2 + SSO (Google, Microsoft)
- Role-based access (admin, viewer)
- Pending submissions and approvals
- Device image uploads to AWS S3
- CSV import/export
- Contributor scores and leaderboards
- Swagger API docs

---

## 🛠 Setup

```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

---

## 🔐 Environment Variables

```env
SECRET_KEY=your-secret-key
S3_BUCKET_NAME=your-s3-bucket
AWS_REGION=us-east-1
S3_PHOTO_PREFIX=device-photos
MAX_PHOTO_MB=5
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
MS_CLIENT_ID=your-ms-client-id
MS_CLIENT_SECRET=your-ms-client-secret
```

---

## 🗄 Database Setup (SQLite)

To initialize the SQLite database:

```bash
sqlite3 device_lifecycle.db < create_schema.sql
```

Ensure your `get_db()` method connects to this file using SQLAlchemy.

---

## ☁️ S3 Bucket Setup

To use AWS S3 for storing device images:

1. Create an S3 bucket in your AWS console.
2. Add these environment variables to your `.env`:

```env
S3_BUCKET_NAME=your-s3-bucket
AWS_REGION=us-east-1
S3_PHOTO_PREFIX=device-photos
```

3. Ensure your IAM user has these permissions:

```json
{
  "Effect": "Allow",
  "Action": ["s3:PutObject", "s3:GetObject", "s3:DeleteObject"],
  "Resource": "arn:aws:s3:::your-s3-bucket/device-photos/*"
}
```

---

## 📚 API Docs

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 📄 License

MIT
