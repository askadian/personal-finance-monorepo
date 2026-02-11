# Prerequisites for API Gateway Setup

Before setting up the API Gateway, ensure you have all the necessary prerequisites in place.

## 🔐 AWS Account and Permissions

### Required AWS Account
- Active AWS account with billing enabled
- Access to AWS Management Console

### Required IAM Permissions

Your IAM user/role needs permissions for:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "apigateway:*",
        "lambda:GetFunction",
        "lambda:AddPermission",
        "lambda:RemovePermission",
        "lambda:GetPolicy",
        "iam:CreateRole",
        "iam:AttachRolePolicy",
        "iam:PassRole",
        "iam:GetRole",
        "cognito-idp:DescribeUserPool",
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "cloudwatch:PutMetricAlarm",
        "cloudwatch:DeleteAlarms"
      ],
      "Resource": "*"
    }
  ]
}
```

**Simplified Option**: Use the AWS managed policy `AmazonAPIGatewayAdministrator`

## 🔧 Backend Components

### 1. Lambda Functions Deployed

Verify that the following Lambda functions are deployed and working:

#### API Lambda Function
- **Location**: `backend/api-lambda/`
- **Function Name**: `personal-finance-api-{environment}`
- **Runtime**: Python 3.12
- **Purpose**: Handles all GET endpoints

**Verification Steps**:
```bash
# Check if Lambda exists
aws lambda get-function --function-name personal-finance-api-dev

# Test Lambda function
aws lambda invoke \
  --function-name personal-finance-api-dev \
  --payload '{"path":"/transactions","httpMethod":"GET","headers":{"X-User-Id":"test_user"}}' \
  response.json

# View response
cat response.json
```

#### File Processor Lambda Function (Optional for initial setup)
- **Location**: `backend/file-processor-lambda/`
- **Function Name**: `personal-finance-file-processor-{environment}`
- **Purpose**: Handles file uploads

### 2. DynamoDB Table (Optional for Mock Data)

For production use, you need a DynamoDB table:
- **Table Name**: `personal-finance-{environment}`
- **Partition Key**: `userId` (String)
- **Sort Key**: `id` (String)

**Note**: The Lambda functions work with mock data if the table doesn't exist yet.

## 🔑 AWS Cognito User Pool

### Required for Authentication

Create or verify you have an AWS Cognito User Pool:

#### Create User Pool

1. **Go to AWS Cognito Console**
   - Navigate to: https://console.aws.amazon.com/cognito/

2. **Create User Pool**
   - Click "Create user pool"
   - Choose sign-in options: Email or Username
   - Configure password requirements
   - Enable MFA (optional but recommended)

3. **Configure App Client**
   - Add an app client
   - Enable "Username password auth (ALLOW_USER_PASSWORD_AUTH)"
   - Note the **User Pool ID** and **App Client ID**

4. **Note Important Details**
   ```
   User Pool ID: us-east-1_XXXXXXXXX
   User Pool ARN: arn:aws:cognito-idp:us-east-1:123456789012:userpool/us-east-1_XXXXXXXXX
   App Client ID: 1234567890abcdefghij
   Region: us-east-1
   ```

#### Create Test User

Create a test user for validation:

```bash
# Create test user
aws cognito-idp admin-create-user \
  --user-pool-id us-east-1_XXXXXXXXX \
  --username testuser@example.com \
  --user-attributes Name=email,Value=testuser@example.com \
  --temporary-password TempPass123! \
  --message-action SUPPRESS

# Set permanent password
aws cognito-idp admin-set-user-password \
  --user-pool-id us-east-1_XXXXXXXXX \
  --username testuser@example.com \
  --password MySecurePass123! \
  --permanent
```

#### Test Authentication

Verify you can get a token:

```bash
# Authenticate and get token
aws cognito-idp initiate-auth \
  --auth-flow USER_PASSWORD_AUTH \
  --client-id 1234567890abcdefghij \
  --auth-parameters USERNAME=testuser@example.com,PASSWORD=MySecurePass123! \
  | jq -r '.AuthenticationResult.IdToken'
```

**Save this token** - you'll use it for testing the API Gateway.

## 📋 Information Gathering Checklist

Before proceeding, gather the following information:

- [ ] **AWS Account ID**: `____________`
- [ ] **Region**: `____________` (e.g., us-east-1)
- [ ] **Lambda Function ARN (API)**: `____________`
- [ ] **Lambda Function ARN (File Processor)**: `____________`
- [ ] **Cognito User Pool ID**: `____________`
- [ ] **Cognito User Pool ARN**: `____________`
- [ ] **Cognito App Client ID**: `____________`
- [ ] **Test User JWT Token**: `____________`

### Getting Lambda ARNs

```bash
# Get API Lambda ARN
aws lambda get-function \
  --function-name personal-finance-api-dev \
  --query 'Configuration.FunctionArn' \
  --output text

# Get File Processor Lambda ARN
aws lambda get-function \
  --function-name personal-finance-file-processor-dev \
  --query 'Configuration.FunctionArn' \
  --output text
```

## 🛠️ Tools and Software

### AWS CLI (Recommended)
Install AWS CLI for command-line operations:

```bash
# For macOS
brew install awscli

# For Linux
sudo apt-get install awscli

# For Windows
# Download from: https://aws.amazon.com/cli/

# Configure AWS CLI
aws configure
```

### Optional Testing Tools
- **Postman**: For API testing (https://www.postman.com/)
- **Bruno**: Alternative API client (https://www.usebruno.com/)
- **curl**: Command-line HTTP client (usually pre-installed)
- **jq**: JSON processor for CLI (https://stedolan.github.io/jq/)

## 📖 Reference Documentation

Familiarize yourself with these AWS resources:

- [API Gateway Getting Started](https://docs.aws.amazon.com/apigateway/latest/developerguide/getting-started.html)
- [API Gateway REST API](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-rest-api.html)
- [Lambda Proxy Integration](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html)
- [Cognito User Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html)

## 📊 Architecture Review

Review the architecture you'll be building:

```
┌─────────────────┐
│   Web Client    │
│   (Frontend)    │
└────────┬────────┘
         │ HTTPS
         │ (Authorization: Bearer <JWT>)
         │
         ▼
┌──────────────────────────────────────┐
│       API Gateway REST API           │
│  ┌────────────────────────────────┐  │
│  │     Cognito Authorizer         │  │
│  │  (Validates JWT Token)         │  │
│  └────────────────────────────────┘  │
│  ┌────────────────────────────────┐  │
│  │  Routes:                       │  │
│  │  • /v1/transactions            │  │
│  │  • /v1/income                  │  │
│  │  • /v1/expenses                │  │
│  │  • /v1/networth                │  │
│  │  • /v1/files                   │  │
│  └────────────────────────────────┘  │
└────────────┬─────────────────────────┘
             │
             ▼
    ┌────────────────┐
    │ Lambda Function│
    │  (API Handler) │
    └────────┬───────┘
             │
             ▼
      ┌─────────────┐
      │  DynamoDB   │
      └─────────────┘
```

## ✅ Prerequisites Checklist

Verify all prerequisites are met:

- [ ] AWS account with appropriate permissions
- [ ] AWS CLI installed and configured
- [ ] Backend Lambda function(s) deployed and tested
- [ ] AWS Cognito User Pool created
- [ ] Test user created in Cognito
- [ ] JWT token obtained for testing
- [ ] All ARNs and IDs documented
- [ ] Understanding of API Gateway concepts
- [ ] OpenAPI specification reviewed ([../../specs/openapi.yaml](../../specs/openapi.yaml))

## 🚨 Troubleshooting

### Cannot Find Lambda Function
**Problem**: Lambda function doesn't exist
**Solution**: Deploy the Lambda function from `backend/api-lambda/` directory

```bash
cd backend/api-lambda
# Follow deployment instructions in backend/api-lambda/README.md
```

### Insufficient IAM Permissions
**Problem**: Access denied errors in AWS Console
**Solution**: 
1. Contact your AWS administrator
2. Request `AmazonAPIGatewayAdministrator` policy
3. Ensure you have Lambda read permissions

### Cannot Get Cognito Token
**Problem**: Authentication fails
**Solution**:
1. Verify User Pool ID and App Client ID
2. Check user exists and password is correct
3. Ensure app client has USER_PASSWORD_AUTH enabled

### AWS CLI Not Configured
**Problem**: CLI commands fail with credential errors
**Solution**:
```bash
aws configure
# Enter Access Key ID, Secret Access Key, Region, and output format
```

## 📝 Notes Before Proceeding

1. **Cost Consideration**: API Gateway has a free tier of 1 million API calls per month for the first 12 months. After that, charges apply. Monitor your usage.

2. **Region Consistency**: Use the same AWS region for all resources (Lambda, API Gateway, Cognito, DynamoDB) to minimize latency.

3. **Naming Convention**: Use consistent naming:
   - API Name: `personal-finance-api`
   - Stage Names: `dev`, `staging`, `prod`
   - Authorizer Name: `cognito-authorizer`

4. **Security**: Never commit AWS credentials or sensitive tokens to version control.

## ✨ Ready to Proceed?

Once all prerequisites are met, continue to the next step:

**Next Step**: [REST API Setup](./02-rest-api-setup.md) →

---

**Back to**: [Manual Setup Guide](./README.md)
