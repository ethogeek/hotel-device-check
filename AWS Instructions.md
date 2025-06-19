# 🚀 Deploying Device Lifecycle API to AWS

This guide provides step-by-step instructions for deploying your FastAPI application on AWS using **Elastic Beanstalk**, **S3**, and **SQLite**.

---

## ✅ 1. Prepare Local Files

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Create a zipped app:
```bash
zip -r application.zip . -x "*.git*" "__pycache__/*"
```

---

## ☁️ 2. Set Up AWS S3

1. **Create an S3 bucket** in the AWS Console.
2. Set the bucket name in your `.env`:
   ```
   S3_BUCKET_NAME=your-bucket-name
   AWS_REGION=us-east-1
   S3_PHOTO_PREFIX=device-photos
   ```
3. Grant your IAM user or role the following policy:
   ```json
   {
     "Effect": "Allow",
     "Action": ["s3:PutObject", "s3:GetObject", "s3:DeleteObject"],
     "Resource": "arn:aws:s3:::your-bucket-name/device-photos/*"
   }
   ```

---

## 🏗 3. Deploy with Elastic Beanstalk (Python App)

### Step 1: Initialize Beanstalk
```bash
eb init -p python-3.11 device-lifecycle-api --region us-east-1
```

### Step 2: Create environment
```bash
eb create device-api-env
```

### Step 3: Deploy
```bash
eb deploy
```

> Ensure your `.ebextensions` directory includes any necessary configuration (e.g., environment variables, `uwsgi` or `gunicorn` setup).

---

## 🧾 4. Environment Variables

Add the following to your Elastic Beanstalk environment:

- `SECRET_KEY`
- `S3_BUCKET_NAME`
- `AWS_REGION`
- `S3_PHOTO_PREFIX`
- `MAX_PHOTO_MB`
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`
- `MS_CLIENT_ID`, `MS_CLIENT_SECRET`

---

## 🗄 5. Initialize SQLite DB (if local)

If using SQLite for prototyping:

```bash
sqlite3 device_lifecycle.db < create_schema.sql
```

Upload the DB to your EC2 instance or bundle it in your app. For production, consider switching to **Amazon RDS (PostgreSQL or MySQL)**.

---

## 🔍 6. Test the API

Access the deployed API at:

```
http://<your-env>.elasticbeanstalk.com/docs
```
