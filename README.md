# Device Lifecycle API

A FastAPI app to manage network device models, track end-of-life (EOL) and end-of-sale (EOS) data, and handle device metadata with role-based permissions, SSO support, and CSV/image upload.


## Features

- 🔐 OAuth2 + SSO (Google, Microsoft)
- 📥 Pending device submissions and admin approvals
- 🏆 Leaderboards, scoring, and badge system
- 🖼 S3-based photo uploads
- 📎 CSV Import/Export
- 🔍 API search and filter
- 🔧 Role and user management
- 🔍 Swagger/OpenAPI docs

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

## Environment Variables

```
SECRET_KEY=your-secret-key
S3_BUCKET_NAME=your-bucket
AWS_REGION=us-east-1
S3_PHOTO_PREFIX=equipment-photos
MAX_PHOTO_MB=5
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
MS_CLIENT_ID=your-client-id
MS_CLIENT_SECRET=your-client-secret
```

## License

MIT
