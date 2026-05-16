# FlowBrief AI — Deployment Guide

This guide covers deploying FlowBrief AI from
scratch. The system has two independent deployments:
backend on Railway and frontend on AWS Amplify.

---

## Prerequisites

- GitHub account with flowbrief-ai repo access
- AWS account with DynamoDB and S3 access
- Railway account connected to GitHub
- AWS Amplify connected to GitHub
- Groq API key from console.groq.com

---

## 1. AWS Infrastructure Setup

### DynamoDB Table

Create the table using AWS CLI or the console.

Via CLI:

  aws dynamodb create-table \
    --table-name flowbrief-cases \
    --attribute-definitions \
      AttributeName=case_id,AttributeType=S \
      AttributeName=created_at,AttributeType=S \
    --key-schema \
      AttributeName=case_id,KeyType=HASH \
      AttributeName=created_at,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1

Wait for status ACTIVE before proceeding.

### S3 Bucket

  aws s3api create-bucket \
    --bucket YOUR-BUCKET-NAME \
    --region us-east-1

  aws s3api put-public-access-block \
    --bucket YOUR-BUCKET-NAME \
    --public-access-block-configuration \
    "BlockPublicAcls=true,IgnorePublicAcls=true,
    BlockPublicPolicy=true,RestrictPublicBuckets=true"

### IAM User

Create an IAM user with programmatic access and
attach these policies:
  AmazonDynamoDBFullAccess
  AmazonS3FullAccess

Save the access key ID and secret access key.

---

## 2. Backend Deployment (Railway)

1. Go to railway.app and create a new project
2. Select Deploy from GitHub repo
3. Select the flowbrief-ai repository
4. In the service Settings, set Root Directory
   to: backend
5. Railway will detect the Dockerfile automatically
6. Add these environment variables in the
   Variables tab:

  GROQ_API_KEY=your_groq_api_key
  AWS_REGION=us-east-1
  AWS_ACCESS_KEY_ID=your_access_key_id
  AWS_SECRET_ACCESS_KEY=your_secret_key
  DYNAMODB_TABLE_NAME=flowbrief-cases
  S3_BUCKET_NAME=your_bucket_name
  ALLOWED_ORIGINS=https://your-amplify-url.amplifyapp.com,http://localhost:5173

7. Click Deploy
8. Wait for the deployment to show as Active
9. Copy the public Railway URL shown in the
   service settings

Verify the backend is live:

  curl https://your-railway-url.up.railway.app/

Expected response:
  {"status":"ok","service":"FlowBrief AI"}

---

## 3. Frontend Deployment (AWS Amplify)

1. Go to console.aws.amazon.com/amplify
2. Click New app > Host web app
3. Connect to GitHub and select flowbrief-ai
4. Select the main branch
5. Click Edit YML file and replace the content
   with:

  version: 1
  frontend:
    phases:
      preBuild:
        commands:
          - cd frontend
          - npm ci
      build:
        commands:
          - npm run build
    artifacts:
      baseDirectory: frontend/dist
      files:
        - '**/*'
    cache:
      paths:
        - frontend/node_modules/**/*

6. Add this environment variable before deploying:

  VITE_API_URL=https://your-railway-url.up.railway.app

7. Click Save and deploy
8. Wait for the build to complete
9. Copy the Amplify URL shown on the app overview

### React Router Redirect Rule

After deployment, confirm this redirect rule
exists under Rewrites and redirects:

  Source:  /<*>
  Target:  /index.html
  Type:    404 (Rewrite)

If it does not exist, add it manually.

---

## 4. Post-Deployment CORS Update

After Amplify assigns a URL, update the
ALLOWED_ORIGINS variable on Railway to include it:

  https://your-amplify-url.amplifyapp.com,http://localhost:5173

Railway will redeploy automatically after saving.

---

## 5. Environment Variables Reference

### Backend (Railway)

| Variable | Description |
|---|---|
| GROQ_API_KEY | Groq API key from console.groq.com |
| AWS_REGION | AWS region (e.g. us-east-1) |
| AWS_ACCESS_KEY_ID | IAM user access key |
| AWS_SECRET_ACCESS_KEY | IAM user secret key |
| DYNAMODB_TABLE_NAME | DynamoDB table name |
| S3_BUCKET_NAME | S3 bucket name |
| ALLOWED_ORIGINS | Comma-separated allowed CORS origins |

### Frontend (Amplify)

| Variable | Description |
|---|---|
| VITE_API_URL | Full backend URL, no trailing slash |

---

## 6. Verifying the Full System

After both deployments are live:

1. Open the Amplify URL in a browser
2. Confirm the sidebar and FlowBrief AI brand
   are visible
3. Navigate to the Dashboard — confirm stat
   cards load from the backend
4. Submit a test document on the New Case page
5. Confirm a case report is generated and
   navigates to the Report View
6. Confirm the case appears in Case History