# AWS Resources Setup Guide

## Overview

This guide provides step-by-step instructions for manually setting up all AWS resources required for the Personal Finance Application frontend integration with the backend API via API Gateway.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Architecture Overview](#architecture-overview)
3. [AWS Resources Required](#aws-resources-required)
4. [Step-by-Step Setup](#step-by-step-setup)
   - [1. Cognito User Pool Setup](#1-cognito-user-pool-setup)
   - [2. DynamoDB Table Setup](#2-dynamodb-table-setup)
   - [3. Lambda Function Setup](#3-lambda-function-setup)
   - [4. API Gateway Setup](#4-api-gateway-setup)
   - [5. IAM Roles and Policies](#5-iam-roles-and-policies)
5. [Environment Configuration](#environment-configuration)
6. [Testing the Setup](#testing-the-setup)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:

- An AWS Account with appropriate permissions
- AWS CLI installed and configured (optional, but recommended)
- Basic understanding of AWS services
- Node.js and npm installed (for local testing)

## Architecture Overview

```
┌─────────────┐
│   Browser   │
│  (Frontend) │
└──────┬──────┘
       │ HTTPS (with JWT token)
       ▼
┌─────────────────────┐
│   API Gateway       │
│   - REST API        │
│   - Cognito Auth    │
│   - CORS enabled    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Lambda Function    │
│  (api-lambda)       │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│    DynamoDB         │
│  (Transactions DB)  │
└─────────────────────┘
```

## AWS Resources Required

### Summary Table

| Resource | Service | Purpose | Estimated Cost (per month) |
|----------|---------|---------|---------------------------|
| User Pool | Cognito | User authentication | Free tier: 50,000 MAUs |
| REST API | API Gateway | API endpoint management | Free tier: 1M requests |
| Lambda Function | Lambda | API business logic | Free tier: 1M requests |
| DynamoDB Table | DynamoDB | Data storage | Free tier: 25GB, 25 WCU, 25 RCU |
| IAM Role | IAM | Lambda execution permissions | Free |
| CloudWatch Logs | CloudWatch | Logging and monitoring | Free tier: 5GB ingestion |

**Note:** Most development usage will stay within AWS free tier limits.

---

## Step-by-Step Setup

### 1. Cognito User Pool Setup

**Purpose:** Manages user authentication and issues JWT tokens for API access.

#### Steps:

1. **Navigate to Cognito**
   - Open AWS Console
   - Search for "Cognito"
   - Click "User pools"

2. **Create User Pool**
   - Click "Create user pool"
   - **Step 1 - Configure sign-in experience:**
     - Sign-in options: Select `Email` and `Username`
     - Click "Next"
   
   - **Step 2 - Configure security requirements:**
     - Password policy: Use default or customize
     - Multi-factor authentication: `Optional` or `Required` (recommended: Optional for dev)
     - Click "Next"
   
   - **Step 3 - Configure sign-up experience:**
     - Self-registration: `Enable self-registration`
     - Required attributes: Select `email`, `name` (optional)
     - Click "Next"
   
   - **Step 4 - Configure message delivery:**
     - Email: Select "Send email with Cognito"
     - Click "Next"
   
   - **Step 5 - Integrate your app:**
     - User pool name: `personal-finance-users`
     - Hosted authentication pages: `Use Cognito Hosted UI`
     - Domain: Choose a unique domain prefix (e.g., `personal-finance-dev`)
     - **Initial app client:**
       - App client name: `personal-finance-web-client`
       - Client secret: `Don't generate a client secret` (important for public web apps)
       - Authentication flows: Enable `ALLOW_USER_PASSWORD_AUTH` and `ALLOW_REFRESH_TOKEN_AUTH`
     - **Advanced app client settings:**
       - OAuth 2.0 grant types: `Authorization code grant`
       - OpenID Connect scopes: `openid`, `email`, `profile`
       - Allowed callback URLs: `http://localhost:3000/`
       - Allowed sign-out URLs: `http://localhost:3000/`
     - Click "Next"
   
   - **Step 6 - Review and create:**
     - Review all settings
     - Click "Create user pool"

3. **Note Configuration Values**
   - User Pool ID (e.g., `us-east-1_abcd1234`)
   - App Client ID (e.g., `1a2b3c4d5e6f7g8h9i0j1k2l3m`)
   - Cognito Domain (e.g., `personal-finance-dev.auth.us-east-1.amazoncognito.com`)
   - Region (e.g., `us-east-1`)

4. **Create Test User** (for testing)
   - In User Pool, click "Users" tab
   - Click "Create user"
   - Username: `testuser`
   - Email: `your-email@example.com`
   - Temporary password: Generate or enter one
   - Uncheck "Send invitation"
   - Click "Create user"

---

### 2. DynamoDB Table Setup

**Purpose:** Stores transaction data (optional for initial setup, as Lambda uses mock data).

#### Steps:

1. **Navigate to DynamoDB**
   - Open AWS Console
   - Search for "DynamoDB"
   - Click "Tables"

2. **Create Table**
   - Click "Create table"
   - **Table name:** `PersonalFinanceTransactions`
   - **Partition key:** `userId` (String)
   - **Sort key:** `transactionId` (String)
   - **Table settings:** Use default settings or customize
   - Click "Create table"

3. **Add Global Secondary Index (GSI)** (optional, for date-based queries)
   - Select the table
   - Go to "Indexes" tab
   - Click "Create index"
   - **Partition key:** `userId` (String)
   - **Sort key:** `date` (String)
   - **Index name:** `UserDateIndex`
   - Click "Create index"

4. **Note Table Configuration**
   - Table name: `PersonalFinanceTransactions`
   - Region: (same as your other resources)
   - Table ARN: (copy for IAM policy)

---

### 3. Lambda Function Setup

**Purpose:** Processes API requests and returns transaction data.

#### Steps:

1. **Navigate to Lambda**
   - Open AWS Console
   - Search for "Lambda"
   - Click "Functions"

2. **Create Function**
   - Click "Create function"
   - **Option:** Author from scratch
   - **Function name:** `personal-finance-api`
   - **Runtime:** Python 3.11 or Python 3.12
   - **Architecture:** x86_64
   - **Permissions:** "Create a new role with basic Lambda permissions"
   - Click "Create function"

3. **Upload Function Code**
   - In the Code source section, copy the code from `backend/api-lambda/lambda_function.py`
   - Paste it into the inline code editor
   - Click "Deploy"

4. **Configure Environment Variables**
   - Go to "Configuration" tab
   - Click "Environment variables"
   - Click "Edit"
   - Add variable:
     - Key: `S3_BUCKET_NAME`
     - Value: `personal-finance-uploads-dev` (or your bucket name)
   - Click "Save"

5. **Configure Timeout and Memory**
   - Go to "Configuration" > "General configuration"
   - Click "Edit"
   - **Memory:** 256 MB (adjust based on needs)
   - **Timeout:** 30 seconds
   - Click "Save"

6. **Note Lambda Configuration**
   - Function ARN: (copy for API Gateway integration)
   - Function name: `personal-finance-api`

---

### 4. API Gateway Setup

**Purpose:** Provides REST API endpoint with Cognito authentication.

For detailed API Gateway setup, refer to the comprehensive guide at:
- **Manual Setup:** `api/apigateway/manual/README.md`
- **Quick Reference:** `api/apigateway/README.md`

#### Quick Steps:

1. **Navigate to API Gateway**
   - Open AWS Console
   - Search for "API Gateway"
   - Click "APIs"

2. **Create REST API**
   - Click "Create API"
   - Choose "REST API" (not Private or HTTP)
   - Click "Build"
   - **API name:** `personal-finance-api`
   - **Description:** REST API for Personal Finance Application
   - **Endpoint Type:** Regional
   - Click "Create API"

3. **Create Cognito Authorizer**
   - In the API, click "Authorizers"
   - Click "Create authorizer"
   - **Name:** `CognitoAuthorizer`
   - **Type:** Cognito
   - **Cognito User Pool:** Select your user pool
   - **Token Source:** `Authorization`
   - Click "Create authorizer"

4. **Create Resources and Methods**
   
   Create `/v1` resource:
   - Click "Create resource"
   - Resource name: `v1`
   - Click "Create resource"
   
   Create `/transactions` resource under `/v1`:
   - Select `/v1`
   - Click "Create resource"
   - Resource name: `transactions`
   - Click "Create resource"
   
   Create GET method for `/v1/transactions`:
   - Select `/v1/transactions`
   - Click "Create method"
   - Method type: `GET`
   - Integration type: `Lambda function`
   - Lambda function: Select `personal-finance-api`
   - Click "Create method"
   
   Configure method settings:
   - Click on the GET method
   - Click "Method request"
   - Authorization: Select `CognitoAuthorizer`
   - Click "Save"

5. **Enable CORS**
   - Select `/v1/transactions`
   - Click "Enable CORS"
   - Leave default settings
   - Click "Save"

6. **Deploy API**
   - Click "Deploy API"
   - **Deployment stage:** Create new stage
   - **Stage name:** `prod`
   - Click "Deploy"

7. **Note API Configuration**
   - **Invoke URL:** (e.g., `https://abc123.execute-api.us-east-1.amazonaws.com/prod`)
   - Copy this URL - you'll need it for frontend configuration

---

### 5. IAM Roles and Policies

**Purpose:** Grant Lambda function permissions to access DynamoDB and CloudWatch.

#### Lambda Execution Role Policy

1. **Navigate to IAM**
   - Open AWS Console
   - Search for "IAM"
   - Click "Roles"

2. **Find Lambda Execution Role**
   - Search for the role created with your Lambda function
   - It will be named like `personal-finance-api-role-xxxxx`
   - Click on it

3. **Add DynamoDB Policy**
   - Click "Add permissions" > "Attach policies"
   - Search for `AWSLambdaDynamoDBExecutionRole`
   - Select it and click "Attach policies"

4. **Add Custom Policy (optional, for more granular control)**
   - Click "Add permissions" > "Create inline policy"
   - Switch to JSON view
   - Paste the following policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:Query",
        "dynamodb:Scan"
      ],
      "Resource": [
        "arn:aws:dynamodb:us-east-1:YOUR_ACCOUNT_ID:table/PersonalFinanceTransactions",
        "arn:aws:dynamodb:us-east-1:YOUR_ACCOUNT_ID:table/PersonalFinanceTransactions/index/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::personal-finance-uploads-dev",
        "arn:aws:s3:::personal-finance-uploads-dev/*"
      ]
    }
  ]
}
```

   - Replace `YOUR_ACCOUNT_ID` with your AWS account ID
   - Name the policy: `PersonalFinanceLambdaPolicy`
   - Click "Create policy"

#### API Gateway Execution Role

API Gateway automatically creates an execution role for Lambda integration. No additional configuration needed.

---

## Environment Configuration

### Frontend Configuration

1. **Copy Environment Template**
   ```bash
   cd frontend
   cp .env.example .env
   ```

2. **Edit .env File**
   
   Update the following values with your AWS resources:

   ```bash
   # AWS Region
   REACT_APP_AWS_REGION=us-east-1
   
   # Cognito Configuration
   REACT_APP_COGNITO_USER_POOL_ID=us-east-1_abcd1234
   REACT_APP_COGNITO_APP_CLIENT_ID=1a2b3c4d5e6f7g8h9i0j1k2l3m
   REACT_APP_COGNITO_DOMAIN=personal-finance-dev.auth.us-east-1.amazoncognito.com
   
   # OAuth Configuration
   REACT_APP_OAUTH_REDIRECT_SIGN_IN=http://localhost:3000/
   REACT_APP_OAUTH_REDIRECT_SIGN_OUT=http://localhost:3000/
   
   # Cookie Configuration (for localhost)
   REACT_APP_COOKIE_DOMAIN=localhost
   REACT_APP_COOKIE_SECURE=false
   
   # API Gateway Endpoint
   REACT_APP_API_ENDPOINT=https://abc123.execute-api.us-east-1.amazonaws.com/prod
   
   # S3 Bucket (optional, for file uploads)
   REACT_APP_S3_BUCKET_NAME=personal-finance-uploads-dev
   ```

3. **Update aws-config.js** (if needed)
   
   The app reads from environment variables, but you can also hardcode values in `src/aws-config.js` for testing.

---

## Testing the Setup

### 1. Test Cognito Authentication

```bash
# Install AWS CLI (if not already installed)
aws --version

# Test user authentication
aws cognito-idp initiate-auth \
  --auth-flow USER_PASSWORD_AUTH \
  --client-id YOUR_APP_CLIENT_ID \
  --auth-parameters USERNAME=testuser,PASSWORD=YourPassword123!
```

Expected output: JSON with `IdToken`, `AccessToken`, and `RefreshToken`

### 2. Test Lambda Function

```bash
# Test Lambda directly
aws lambda invoke \
  --function-name personal-finance-api \
  --payload '{"httpMethod":"GET","path":"/v1/transactions","headers":{"X-User-Id":"user_123"}}' \
  response.json

# View response
cat response.json
```

Expected output: JSON with mock transaction data

### 3. Test API Gateway

```bash
# Get ID token from Cognito (from step 1)
ID_TOKEN="your_id_token_here"

# Test API Gateway endpoint
curl -X GET \
  "https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod/v1/transactions" \
  -H "Authorization: Bearer $ID_TOKEN"
```

Expected output: JSON with transaction data

### 4. Test Frontend Application

```bash
# Start the frontend application
cd frontend
npm install
npm start
```

1. Open http://localhost:3000
2. Sign in with your test user
3. Navigate to the Transactions tab
4. You should see transaction data displayed

---

## Troubleshooting

### Issue: "API endpoint not configured"

**Solution:**
- Ensure `.env` file exists in `frontend/` directory
- Verify `REACT_APP_API_ENDPOINT` is set correctly
- Restart the development server after changing `.env`

### Issue: "Not authenticated" error

**Solution:**
- Check Cognito configuration in `.env`
- Verify user pool ID and app client ID are correct
- Ensure you're signed in (check browser console for errors)
- Check that app client doesn't have a secret (public clients shouldn't)

### Issue: "403 Forbidden" from API Gateway

**Solution:**
- Verify Cognito authorizer is configured correctly
- Check that the method has authorization enabled
- Ensure the JWT token is valid (not expired)
- Verify the token is being sent in the `Authorization` header

### Issue: "502 Bad Gateway" from API Gateway

**Solution:**
- Check Lambda function logs in CloudWatch
- Verify Lambda has correct IAM permissions
- Check Lambda function code for errors
- Ensure Lambda integration is configured correctly in API Gateway

### Issue: CORS errors in browser

**Solution:**
- Enable CORS on API Gateway resources
- Deploy the API after enabling CORS
- Check that Lambda returns proper CORS headers
- Verify allowed origins in CORS configuration

### Issue: DynamoDB access denied

**Solution:**
- Check Lambda execution role has DynamoDB permissions
- Verify table name in Lambda environment variables
- Check table ARN in IAM policy matches actual table

---

## Next Steps

After completing the manual setup:

1. **Add GitHub Actions automation** for CI/CD (see `api/apigateway/automation/`)
2. **Configure custom domain** for API Gateway (optional)
3. **Set up CloudWatch alarms** for monitoring
4. **Enable AWS WAF** for enhanced security
5. **Configure DynamoDB with real data** instead of mock data

---

## Additional Resources

- [AWS API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)
- [AWS Cognito Documentation](https://docs.aws.amazon.com/cognito/)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [OpenAPI Specification](../api/specs/openapi.yaml)
- [API Gateway Manual Setup Guide](../api/apigateway/manual/README.md)

---

## Summary

You have successfully set up:

✅ Cognito User Pool for authentication  
✅ Lambda function for API logic  
✅ API Gateway for REST API endpoint  
✅ IAM roles and policies for secure access  
✅ Frontend environment configuration  
✅ CORS for cross-origin requests  

Your Personal Finance application frontend is now integrated with the backend API via API Gateway!
