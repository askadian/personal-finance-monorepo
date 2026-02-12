# AWS Setup Guide for File Upload Feature

This guide provides step-by-step instructions for setting up AWS resources required for the file upload feature.

## Overview

The file upload feature uses the following AWS services:
- **Amazon S3**: Storage for uploaded financial documents
- **AWS Lambda**: Backend function to generate presigned URLs (optional but recommended)
- **Amazon API Gateway**: REST API endpoint for presigned URL generation (optional but recommended)
- **AWS IAM**: Roles and policies for secure access

## Architecture

```
User Browser → API Gateway → Lambda Function → Generates Presigned URL
     ↓                                              ↓
     └──────────────→ S3 (Direct Upload) ←──────────┘
```

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI installed (optional but recommended)
- Existing Cognito User Pool (for authentication)

---

## Part 1: S3 Bucket Setup

### Step 1: Create S3 Bucket

1. **Navigate to S3 Console**
   - Go to [AWS S3 Console](https://console.aws.amazon.com/s3/)
   - Click "Create bucket"

2. **Configure Bucket Settings**
   
   **Bucket Name**: Follow the naming convention already used in this repository:
   ```
   personal-finance-uploads-{environment}
   ```
   Examples:
   - `personal-finance-uploads-dev` (for development)
   - `personal-finance-uploads-staging` (for staging)
   - `personal-finance-uploads-prod` (for production)

   **AWS Region**: Choose the same region as your other AWS resources (e.g., `us-east-1`)

3. **Configure Options**
   - **Block Public Access**: Keep all public access blocked (recommended)
   - **Bucket Versioning**: Enable (optional but recommended)
   - **Tags**: Add tags for organization (optional)
     - Key: `Environment`, Value: `dev` (or `staging`, `prod`)
     - Key: `Project`, Value: `personal-finance`

4. **Configure Encryption**
   - **Default encryption**: Enable
   - **Encryption type**: Choose "SSE-S3" (Server-Side Encryption with Amazon S3 managed keys)
   
   Alternatively, for enhanced security:
   - Choose "SSE-KMS" (AWS Key Management Service)
   - Select or create a KMS key

5. **Click "Create bucket"**

### Step 2: Configure CORS

The bucket needs CORS (Cross-Origin Resource Sharing) configuration to allow uploads from your web application.

1. **Navigate to Your Bucket**
   - Click on your newly created bucket

2. **Go to Permissions Tab**
   - Scroll down to "Cross-origin resource sharing (CORS)"
   - Click "Edit"

3. **Add CORS Configuration**
   
   ```json
   [
       {
           "AllowedHeaders": [
               "*"
           ],
           "AllowedMethods": [
               "GET",
               "PUT",
               "POST",
               "DELETE",
               "HEAD"
           ],
           "AllowedOrigins": [
               "http://localhost:3000",
               "https://your-production-domain.com"
           ],
           "ExposeHeaders": [
               "ETag",
               "x-amz-server-side-encryption",
               "x-amz-request-id",
               "x-amz-id-2"
           ],
           "MaxAgeSeconds": 3000
       }
   ]
   ```

   **Important**: Replace `https://your-production-domain.com` with your actual production domain(s).

4. **Click "Save changes"**

### Step 3: Configure S3 Event Notifications

Set up S3 to trigger the file processor Lambda when files are uploaded.

1. **Go to Properties Tab**
   - Scroll down to "Event notifications"
   - Click "Create event notification"

2. **Configure Event**
   - **Event name**: `file-upload-trigger`
   - **Event types**: Select "All object create events" (or specifically `s3:ObjectCreated:Put` and `s3:ObjectCreated:Post`)
   - **Prefix**: `users/` (to only trigger for files in the users folder)
   - **Suffix**: Leave empty or specify `.csv`, `.pdf` (one notification per suffix)

3. **Destination**
   - **Destination type**: Lambda function
   - **Lambda function**: Select your `FileProcessorLambda` function
   - If you haven't created the Lambda function yet, see the backend documentation: `/backend/file-processor-lambda/README.md`

4. **Click "Save changes"**

---

## Part 2: IAM Roles and Policies

### Option A: Lambda Function with Presigned URLs (Recommended)

This approach generates presigned URLs through an API endpoint, which is more secure.

#### Step 1: Create IAM Role for Lambda Function

1. **Navigate to IAM Console**
   - Go to [AWS IAM Console](https://console.aws.amazon.com/iam/)
   - Click "Roles" in the left sidebar
   - Click "Create role"

2. **Select Trusted Entity**
   - **Trusted entity type**: AWS service
   - **Use case**: Lambda
   - Click "Next"

3. **Attach Permissions Policies**
   - Search and select: `AWSLambdaBasicExecutionRole`
   - Click "Next"

4. **Name the Role**
   - **Role name**: `PersonalFinanceUploadLambdaRole`
   - Click "Create role"

5. **Add Inline Policy for S3**
   - Click on the newly created role
   - Click "Add permissions" → "Create inline policy"
   - Click "JSON" tab
   - Add the following policy:

   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                   "s3:PutObject",
                   "s3:PutObjectAcl",
                   "s3:GetObject"
               ],
               "Resource": "arn:aws:s3:::personal-finance-uploads-dev/*"
           },
           {
               "Effect": "Allow",
               "Action": [
                   "s3:ListBucket"
               ],
               "Resource": "arn:aws:s3:::personal-finance-uploads-dev"
           }
       ]
   }
   ```

   **Important**: Replace `personal-finance-uploads-dev` with your actual bucket name.

6. **Name the Policy**
   - **Policy name**: `S3UploadAccess`
   - Click "Create policy"

### Option B: Direct Upload with IAM User (Not Recommended for Production)

This approach requires embedding AWS credentials in the frontend, which is a security risk.

**⚠️ WARNING**: This method is only suitable for development/testing. Do NOT use in production.

#### Step 1: Create IAM User

1. **Navigate to IAM Console**
   - Click "Users" in the left sidebar
   - Click "Add users"

2. **Configure User**
   - **User name**: `personal-finance-upload-user`
   - **Access type**: Programmatic access
   - Click "Next: Permissions"

3. **Attach Policy**
   - Click "Attach existing policies directly"
   - Click "Create policy"
   - Use the same S3 policy from Option A above
   - Name it: `PersonalFinanceUploadPolicy`
   - Go back and attach it to the user

4. **Download Credentials**
   - Save the Access Key ID and Secret Access Key
   - **IMPORTANT**: Never commit these to version control

---

## Part 3: Lambda Function for Presigned URLs

### Step 1: Create Lambda Function

1. **Navigate to Lambda Console**
   - Go to [AWS Lambda Console](https://console.aws.amazon.com/lambda/)
   - Click "Create function"

2. **Configure Function**
   - **Function name**: `PersonalFinanceUploadUrl`
   - **Runtime**: Python 3.12 (or latest)
   - **Architecture**: x86_64
   - **Execution role**: Use the role created earlier (`PersonalFinanceUploadLambdaRole`)
   - Click "Create function"

3. **Add Function Code**

   Replace the default code with:

   ```python
   import json
   import boto3
   import os
   from datetime import datetime, timedelta
   import uuid

   s3_client = boto3.client('s3')
   BUCKET_NAME = os.environ.get('BUCKET_NAME', 'personal-finance-uploads-dev')
   URL_EXPIRATION = 300  # 5 minutes

   def lambda_handler(event, context):
       """
       Generate presigned URL for S3 upload
       """
       try:
           # Parse request body
           body = json.loads(event.get('body', '{}'))
           file_key = body.get('fileKey')
           content_type = body.get('contentType', 'application/octet-stream')
           
           if not file_key:
               return {
                   'statusCode': 400,
                   'headers': {
                       'Content-Type': 'application/json',
                       'Access-Control-Allow-Origin': '*'
                   },
                   'body': json.dumps({
                       'error': {
                           'message': 'fileKey is required',
                           'statusCode': 400
                       }
                   })
               }
           
           # Validate file key format (should start with users/)
           if not file_key.startswith('users/'):
               return {
                   'statusCode': 400,
                   'headers': {
                       'Content-Type': 'application/json',
                       'Access-Control-Allow-Origin': '*'
                   },
                   'body': json.dumps({
                       'error': {
                           'message': 'Invalid fileKey format. Must start with users/',
                           'statusCode': 400
                       }
                   })
               }
           
           # Get user ID from Cognito authorizer
           user_id = None
           try:
               authorizer = event.get('requestContext', {}).get('authorizer', {})
               user_id = authorizer.get('claims', {}).get('sub')
           except Exception as e:
               print(f"Error extracting user ID: {e}")
           
           # Verify that the file key belongs to the authenticated user
           if user_id and not file_key.startswith(f'users/{user_id}/'):
               return {
                   'statusCode': 403,
                   'headers': {
                       'Content-Type': 'application/json',
                       'Access-Control-Allow-Origin': '*'
                   },
                   'body': json.dumps({
                       'error': {
                           'message': 'Unauthorized: Cannot upload to another user\'s folder',
                           'statusCode': 403
                       }
                   })
               }
           
           # Generate presigned URL
           presigned_url = s3_client.generate_presigned_url(
               'put_object',
               Params={
                   'Bucket': BUCKET_NAME,
                   'Key': file_key,
                   'ContentType': content_type
               },
               ExpiresIn=URL_EXPIRATION
           )
           
           # Generate file ID
           file_id = str(uuid.uuid4())
           
           # Calculate expiration time
           expires_at = (datetime.utcnow() + timedelta(seconds=URL_EXPIRATION)).isoformat() + 'Z'
           
           return {
               'statusCode': 200,
               'headers': {
                   'Content-Type': 'application/json',
                   'Access-Control-Allow-Origin': '*'
               },
               'body': json.dumps({
                   'uploadUrl': presigned_url,
                   'fileId': file_id,
                   'expiresAt': expires_at
               })
           }
           
       except Exception as e:
           print(f"Error generating presigned URL: {str(e)}")
           return {
               'statusCode': 500,
               'headers': {
                   'Content-Type': 'application/json',
                   'Access-Control-Allow-Origin': '*'
               },
               'body': json.dumps({
                   'error': {
                       'message': 'Internal server error',
                       'statusCode': 500
                   }
               })
           }
   ```

4. **Configure Environment Variables**
   - Scroll down to "Configuration" → "Environment variables"
   - Click "Edit"
   - Add the following:
     - Key: `BUCKET_NAME`, Value: `personal-finance-uploads-dev` (your bucket name)
   - Click "Save"

5. **Click "Deploy"**

### Step 2: Test Lambda Function

1. **Create Test Event**
   - Click "Test" tab
   - **Event name**: `test-upload-url`
   - **Event JSON**:

   ```json
   {
       "body": "{\"fileKey\": \"users/test-user/bank-statement/1234567890-test.pdf\", \"contentType\": \"application/pdf\"}",
       "requestContext": {
           "authorizer": {
               "claims": {
                   "sub": "test-user"
               }
           }
       }
   }
   ```

2. **Click "Test"**
   - Verify that the function returns a 200 status code
   - Check that the response contains `uploadUrl`, `fileId`, and `expiresAt`

---

## Part 4: API Gateway Setup

### Step 1: Create REST API

1. **Navigate to API Gateway Console**
   - Go to [AWS API Gateway Console](https://console.aws.amazon.com/apigateway/)
   - Click "Create API"
   - Choose "REST API" (not Private)
   - Click "Build"

2. **Configure API**
   - **API name**: `PersonalFinanceAPI` (or use existing API)
   - **Description**: API for personal finance application
   - **Endpoint Type**: Regional
   - Click "Create API"

### Step 2: Create Resource and Method

1. **Create Resource**
   - Click "Actions" → "Create Resource"
   - **Resource Name**: `upload-url`
   - **Resource Path**: `/upload-url`
   - **Enable API Gateway CORS**: Check this box
   - Click "Create Resource"

2. **Create POST Method**
   - Select the `/upload-url` resource
   - Click "Actions" → "Create Method"
   - Select "POST" from the dropdown
   - Click the checkmark

3. **Configure Method**
   - **Integration type**: Lambda Function
   - **Use Lambda Proxy integration**: Check this box
   - **Lambda Region**: Select your region
   - **Lambda Function**: `PersonalFinanceUploadUrl`
   - Click "Save"
   - Click "OK" to give API Gateway permission to invoke the Lambda

### Step 3: Configure Cognito Authorizer

1. **Create Authorizer**
   - In the left sidebar, click "Authorizers"
   - Click "Create New Authorizer"
   - **Name**: `CognitoAuthorizer`
   - **Type**: Cognito
   - **Cognito User Pool**: Select your Cognito User Pool
   - **Token Source**: `Authorization`
   - Click "Create"

2. **Attach Authorizer to Method**
   - Go back to "Resources"
   - Click on the POST method under `/upload-url`
   - Click "Method Request"
   - Under "Authorization", select `CognitoAuthorizer`
   - Click the checkmark to save

### Step 4: Enable CORS

1. **Select Resource**
   - Select the `/upload-url` resource

2. **Enable CORS**
   - Click "Actions" → "Enable CORS"
   - Verify the CORS headers
   - Click "Enable CORS and replace existing CORS headers"
   - Click "Yes, replace existing values"

### Step 5: Deploy API

1. **Create Deployment**
   - Click "Actions" → "Deploy API"
   - **Deployment stage**: [New Stage]
   - **Stage name**: `prod` (or `dev`, `staging`)
   - Click "Deploy"

2. **Note the Invoke URL**
   - After deployment, you'll see the "Invoke URL" at the top
   - Example: `https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod`
   - Copy this URL - you'll need it for the frontend configuration

---

## Part 5: Frontend Configuration

### Step 1: Update Environment Variables

1. **Create `.env.local` file**
   - In the `/frontend` directory, create a file named `.env.local`
   - Copy the contents from `.env.example`

2. **Configure S3 and API Settings**
   
   ```bash
   # AWS Region
   REACT_APP_AWS_REGION=us-east-1
   
   # S3 Bucket Name
   REACT_APP_S3_BUCKET_NAME=personal-finance-uploads-dev
   
   # API Gateway Endpoint (from Part 4, Step 5)
   REACT_APP_API_ENDPOINT=https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod
   
   # Cognito Configuration (if not already set)
   REACT_APP_COGNITO_USER_POOL_ID=us-east-1_abcd1234
   REACT_APP_COGNITO_APP_CLIENT_ID=1a2b3c4d5e6f7g8h9i0j1k2l3m
   REACT_APP_COGNITO_DOMAIN=your-app-name.auth.us-east-1.amazoncognito.com
   ```

3. **Replace Placeholder Values**
   - Replace all placeholder values with your actual AWS resource IDs

### Step 2: Restart Development Server

```bash
cd frontend
npm start
```

---

## Part 6: Testing

### Test 1: File Selection

1. Log in to the application
2. Click "Upload File" button
3. Select a file (PDF, CSV, or Excel)
4. Select a file type from the dropdown
5. Verify that file size is shown correctly

### Test 2: File Upload

1. Click "Upload" button
2. Verify that progress bar appears
3. Verify that upload completes successfully
4. Check for success message

### Test 3: S3 Verification

1. Go to AWS S3 Console
2. Navigate to your bucket
3. Check the `users/{user-id}/` folder
4. Verify that the file was uploaded

### Test 4: Lambda Trigger

1. Go to AWS CloudWatch Console
2. Check logs for `FileProcessorLambda` function
3. Verify that the function was triggered by the S3 upload
4. Check for successful processing logs

### Test 5: Error Handling

1. Try uploading a file larger than 10MB
2. Verify error message appears
3. Try uploading an unsupported file type
4. Verify appropriate error message

---

## Troubleshooting

### Issue: CORS Errors

**Symptoms**: Browser console shows CORS-related errors

**Solutions**:
1. Verify S3 CORS configuration includes your domain
2. Verify API Gateway CORS is enabled
3. Check that API Gateway returns proper CORS headers
4. Clear browser cache and try again

### Issue: Upload Fails with 403 Forbidden

**Symptoms**: Upload fails with "Access Denied" error

**Solutions**:
1. Verify IAM role has correct S3 permissions
2. Check that S3 bucket policy allows uploads
3. Verify file key format starts with `users/`
4. Check Cognito token is valid

### Issue: Presigned URL Generation Fails

**Symptoms**: API returns error when requesting upload URL

**Solutions**:
1. Check Lambda function logs in CloudWatch
2. Verify Lambda has S3 permissions
3. Verify BUCKET_NAME environment variable is set correctly
4. Check that Cognito authorizer is configured correctly

### Issue: File Not Processing After Upload

**Symptoms**: File uploads but doesn't trigger Lambda

**Solutions**:
1. Verify S3 event notification is configured
2. Check that file is uploaded to correct prefix (`users/`)
3. Verify Lambda has permission to be invoked by S3
4. Check CloudWatch logs for Lambda errors

---

## Security Best Practices

### 1. Use Presigned URLs
- Always generate presigned URLs server-side
- Never embed AWS credentials in frontend code
- Set short expiration times (5-15 minutes)

### 2. Validate File Uploads
- Implement file type validation
- Set maximum file size limits
- Scan uploaded files for viruses (optional)

### 3. User Isolation
- Always upload to user-specific folders: `users/{user-id}/`
- Verify user ID from Cognito token matches upload path
- Never allow users to access other users' files

### 4. Encryption
- Enable S3 bucket encryption
- Use HTTPS for all API calls
- Consider using KMS for enhanced encryption

### 5. Access Control
- Keep S3 bucket private (block all public access)
- Use IAM roles with least privilege
- Regularly audit access logs

---

## Next Steps

After completing this setup:

1. **Test thoroughly** in development environment
2. **Create separate resources** for staging and production
3. **Set up monitoring** with CloudWatch alarms
4. **Configure backup** and retention policies
5. **Document** your specific configuration for your team

---

## Additional Resources

- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Presigned URLs Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html)

---

## Support

For issues or questions:
- Check the troubleshooting section above
- Review AWS CloudWatch logs
- Check the repository's issue tracker
- Consult AWS Support (if you have a support plan)
