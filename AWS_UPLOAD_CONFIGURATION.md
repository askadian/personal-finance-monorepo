# AWS Configuration Guide for Upload Feature

This document outlines the manual AWS console configuration steps required to enable the file upload feature. These steps cannot be automated via code and must be performed in the AWS Console.

## Prerequisites

- AWS Account with appropriate permissions
- API Gateway ID: `ffcijer5wl`
- S3 Bucket: `personal-finance-uploads-dev`
- Lambda Function: `PersonalFinanceUploadUrl`
- Region: `us-east-1`
- Stage: `dev`

## 1. AWS API Gateway Configuration

### A. Remove Duplicate OPTIONS Method

1. Navigate to [AWS API Gateway Console](https://console.aws.amazon.com/apigateway/)
2. Select API with ID: `ffcijer5wl`
3. Go to **Resources** in the left sidebar
4. Locate the `/v1` resource (parent resource)
5. **If there is an OPTIONS method under `/v1` (parent)**, select it and click **Delete**
6. **Keep the OPTIONS method under `/v1/upload-url`** (child resource) - DO NOT DELETE THIS ONE

> **Important**: Only the `/v1/upload-url` resource should have an OPTIONS method. The parent `/v1` resource should NOT have an OPTIONS method to avoid conflicts.

### B. Configure OPTIONS Method for CORS

1. Click on the **OPTIONS** method under `/v1/upload-url`
2. Verify the configuration:

#### Integration Request
- **Integration Type**: Mock (not Lambda)
- **Authorization**: NONE

#### Method Response
1. Click on **Method Response**
2. Expand the **200** response
3. Add the following **Response Headers** (if not already present):
   - `Access-Control-Allow-Origin`
   - `Access-Control-Allow-Headers`
   - `Access-Control-Allow-Methods`

#### Integration Response
1. Click on **Integration Response**
2. Expand the **200** response
3. Configure **Header Mappings**:
   - `Access-Control-Allow-Origin` → `'*'`
   - `Access-Control-Allow-Headers` → `'Content-Type,Authorization'`
   - `Access-Control-Allow-Methods` → `'OPTIONS,POST'`

> **Note**: The single quotes around the values are important. Use exactly: `'*'`, `'Content-Type,Authorization'`, and `'OPTIONS,POST'`

### C. Deploy API to Dev Stage

1. Click on **Actions** dropdown in the Resources view
2. Select **Deploy API**
3. Configure deployment:
   - **Deployment stage**: `dev`
   - **Deployment description**: "Fix CORS and configure OPTIONS method for upload endpoint"
4. Click **Deploy**

> **Verification**: After deployment, test the endpoint at:
> ```
> https://ffcijer5wl.execute-api.us-east-1.amazonaws.com/dev/v1/upload-url
> ```

## 2. S3 Bucket CORS Configuration

### Configure CORS for S3 Bucket

1. Navigate to [AWS S3 Console](https://console.aws.amazon.com/s3/)
2. Select bucket: `personal-finance-uploads-dev`
3. Go to **Permissions** tab
4. Scroll down to **Cross-origin resource sharing (CORS)**
5. Click **Edit**
6. Replace the CORS configuration with the following JSON:

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
            "http://localhost:3001"
        ],
        "ExposeHeaders": [
            "ETag",
            "x-amz-server-side-encryption"
        ],
        "MaxAgeSeconds": 3000
    }
]
```

7. Click **Save changes**

> **Important Notes**:
> - The `PUT` method is critical for direct file uploads to S3
> - Add your production domain to `AllowedOrigins` when deploying to production
> - `MaxAgeSeconds` sets the browser cache duration for preflight responses (50 minutes)

## 3. Lambda Function Verification

### Verify PersonalFinanceUploadUrl Lambda Configuration

1. Navigate to [AWS Lambda Console](https://console.aws.amazon.com/lambda/)
2. Select function: `PersonalFinanceUploadUrl`
3. Verify the Lambda code includes proper CORS headers and accepts `fileName` parameter

#### Required CORS Headers in Lambda Response

The Lambda function should include these headers in ALL responses:

```python
headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    'Access-Control-Allow-Methods': 'POST,OPTIONS'
}
```

#### Handle OPTIONS Preflight Requests

The Lambda should handle OPTIONS requests:

```python
# Handle OPTIONS request
if event.get('httpMethod') == 'OPTIONS':
    return {
        'statusCode': 200,
        'headers': headers,
        'body': ''
    }
```

#### Accept fileName in Request Body

The Lambda should accept and use the `fileName` parameter:

```python
body = json.loads(event.get('body', '{}'))
file_key = body.get('fileKey')
content_type = body.get('contentType', 'application/octet-stream')
file_name = body.get('fileName', 'unknown')  # New parameter
```

> **Note**: The `fileName` parameter is used for logging and tracking purposes. The actual S3 key is still determined by the `fileKey` parameter.

## 4. Testing the Configuration

After completing all configuration steps:

### A. Test CORS Preflight (OPTIONS Request)

Use curl or browser DevTools:

```bash
curl -X OPTIONS https://ffcijer5wl.execute-api.us-east-1.amazonaws.com/dev/v1/upload-url \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type,Authorization" \
  -v
```

**Expected Response:**
- Status: `200 OK`
- Headers should include:
  - `Access-Control-Allow-Origin: *`
  - `Access-Control-Allow-Headers: Content-Type,Authorization`
  - `Access-Control-Allow-Methods: OPTIONS,POST`

### B. Test Upload Flow in Application

1. Start the frontend development server:
   ```bash
   cd frontend
   npm start
   ```

2. Log in to the application
3. Navigate to the file upload feature
4. Select a test file (PDF, CSV, or Excel)
5. Choose a file type from the dropdown
6. Click **Upload**

**Expected Behavior:**
- ✅ OPTIONS preflight request returns `200 OK`
- ✅ POST request to `/v1/upload-url` returns `200 OK` with presigned URL
- ✅ PUT request to S3 presigned URL uploads file successfully
- ✅ File appears in S3 bucket under: `users/{userId}/{file-type}/{timestamp}-{filename}`

### C. Browser DevTools Verification

1. Open Browser DevTools (F12)
2. Go to **Network** tab
3. Perform a file upload
4. Verify the request sequence:

   **Request 1: OPTIONS (Preflight)**
   - URL: `https://ffcijer5wl.execute-api.us-east-1.amazonaws.com/dev/v1/upload-url`
   - Status: `200`
   - Response Headers: Contains CORS headers

   **Request 2: POST (Get Presigned URL)**
   - URL: `https://ffcijer5wl.execute-api.us-east-1.amazonaws.com/dev/v1/upload-url`
   - Status: `200`
   - Request Headers: Contains `Authorization: Bearer {token}`
   - Request Body: Contains `fileKey`, `contentType`, and `fileName`
   - Response Body: Contains `uploadUrl`, `fileId`, `expiresAt`

   **Request 3: PUT (Upload to S3)**
   - URL: S3 presigned URL
   - Status: `200`
   - Request Headers: Contains `Content-Type: {file-mime-type}`
   - Request Body: File binary data

5. Check **Console** tab for no errors

## 5. Troubleshooting

### Issue: CORS Error on OPTIONS Request

**Symptoms:**
```
Access to fetch at 'https://...' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution:**
1. Verify OPTIONS method exists on `/v1/upload-url` resource
2. Ensure OPTIONS method integration type is **Mock**, not Lambda
3. Verify OPTIONS method authorization is set to **NONE**
4. Check that header mappings use single quotes: `'*'`, `'Content-Type,Authorization'`
5. Redeploy API to `dev` stage

### Issue: 403 Forbidden on POST Request

**Symptoms:**
- POST request to `/v1/upload-url` returns `403 Forbidden`

**Solution:**
1. Verify Cognito authentication is working (check if `Authorization` header contains valid JWT)
2. Ensure API Gateway method has Cognito Authorizer configured
3. Check that the JWT token is from the correct Cognito User Pool: `us-east-1_ypJY5Q49F`
4. Verify the App Client ID matches: `26g1835ki3plirj0dsfab38vqb`

### Issue: S3 Upload Fails with CORS Error

**Symptoms:**
```
Access to XMLHttpRequest at 'https://personal-finance-uploads-dev.s3.amazonaws.com/...' 
from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution:**
1. Verify S3 bucket CORS configuration includes `PUT` method
2. Ensure `http://localhost:3000` is in `AllowedOrigins`
3. Check that Lambda generates presigned URLs with correct bucket name
4. Wait a few minutes for CORS configuration to propagate

### Issue: Lambda Returns 500 Error

**Symptoms:**
- POST request returns `500 Internal Server Error`

**Solution:**
1. Check Lambda CloudWatch Logs for error details
2. Verify Lambda has IAM permissions for `s3:PutObject`
3. Ensure `S3_BUCKET_NAME` environment variable is set in Lambda
4. Verify request body contains required fields: `fileKey`, `contentType`, `fileName`

## 6. Security Considerations

### CORS Configuration
- Current configuration uses `Access-Control-Allow-Origin: *` which allows any origin
- For production, restrict to specific domains:
  ```python
  'Access-Control-Allow-Origin': 'https://yourdomain.com'
  ```

### S3 CORS
- Update `AllowedOrigins` to include only production domains
- Remove `localhost` origins in production:
  ```json
  "AllowedOrigins": [
      "https://yourdomain.com",
      "https://www.yourdomain.com"
  ]
  ```

### Presigned URL Expiration
- Current expiration: 5 minutes (300 seconds)
- Adjust in Lambda if needed for large files or slow connections

### File Type Validation
- Frontend validates: PDF, CSV, XLS, XLSX
- Lambda should also validate file extensions to prevent malicious uploads
- Consider adding virus scanning for uploaded files

## 7. AWS Resources Summary

| Resource | Value |
|----------|-------|
| **API Gateway ID** | `ffcijer5wl` |
| **API Stage** | `dev` |
| **Region** | `us-east-1` |
| **Full Invoke URL** | `https://ffcijer5wl.execute-api.us-east-1.amazonaws.com/dev` |
| **Resource Path** | `/v1/upload-url` |
| **S3 Bucket** | `personal-finance-uploads-dev` |
| **Lambda Function** | `PersonalFinanceUploadUrl` |
| **Cognito User Pool** | `us-east-1_ypJY5Q49F` |
| **Cognito App Client** | `26g1835ki3plirj0dsfab38vqb` |

## 8. Next Steps

After completing the AWS configuration:

1. ✅ Restart the frontend development server
2. ✅ Test the upload flow end-to-end
3. ✅ Verify files appear in S3 bucket
4. ✅ Check CloudWatch Logs for any errors
5. ✅ Update CORS origins for production deployment
6. ✅ Consider implementing server-side file validation
7. ✅ Set up S3 lifecycle policies for old files (optional)
8. ✅ Configure S3 bucket versioning (optional)

---

**Document Version:** 1.0  
**Last Updated:** 2024-02-15  
**Maintained by:** Personal Finance Team
