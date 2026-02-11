# Lambda Integration Setup

This guide walks through connecting your API Gateway endpoints to Lambda functions using Lambda Proxy Integration.

## 📋 Overview

In this step, you will:
1. Configure Lambda Proxy Integration for all endpoints
2. Set up Lambda function permissions
3. Test the integration
4. Configure integration responses

**Estimated Time**: 20-30 minutes

## 🎯 What is Lambda Proxy Integration?

Lambda Proxy Integration passes the entire HTTP request to Lambda and expects a formatted response.

### Benefits:
- ✅ Lambda receives full request context (headers, query params, body)
- ✅ Lambda controls response format and status codes
- ✅ Simpler configuration in API Gateway
- ✅ More flexibility in Lambda function

### Request Format Received by Lambda:
```json
{
  "resource": "/v1/transactions",
  "path": "/v1/transactions",
  "httpMethod": "GET",
  "headers": {...},
  "queryStringParameters": {...},
  "pathParameters": {...},
  "body": null,
  "isBase64Encoded": false
}
```

### Expected Response Format from Lambda:
```json
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"data\": [...]}"
}
```

## 🚀 Step-by-Step Instructions

### Step 1: Get Lambda Function ARN

Before starting, get your Lambda function ARN:

```bash
# Get API Lambda ARN
aws lambda get-function \
  --function-name personal-finance-api-dev \
  --query 'Configuration.FunctionArn' \
  --output text
```

Example ARN:
```
arn:aws:lambda:us-east-1:123456789012:function:personal-finance-api-dev
```

### Step 2: Configure Integration for GET /v1/transactions

1. **Navigate to API Gateway Console**
   - Select your API: `personal-finance-api`
   - Click **Resources** in left sidebar

2. **Select GET Method**
   - Expand `/v1/transactions`
   - Click on **GET** method

3. **Change Integration Type**
   - Click on **Integration Request**
   - Click **Edit**
   
4. **Configure Lambda Integration**:
   - **Integration type**: Select **Lambda Function**
   - **Use Lambda Proxy integration**: **Check this box** ✓
   - **Lambda Region**: Select your region (e.g., `us-east-1`)
   - **Lambda Function**: Enter your function name or ARN
     ```
     personal-finance-api-dev
     ```
   - Click **Save**

5. **Add Permission Prompt**
   - A popup will appear: "Add Permission to Lambda Function"
   - Click **OK** to grant API Gateway permission to invoke Lambda

   > This creates a resource policy on the Lambda function allowing API Gateway to invoke it

### Step 3: Verify Integration

After saving, you should see:

- Integration Type: **Lambda Function**
- Lambda Region: **us-east-1** (or your region)
- Lambda Function: **personal-finance-api-dev**
- Use Lambda Proxy integration: **Yes**

### Step 4: Configure Remaining GET Endpoints

Repeat Step 2 for all GET methods:

#### List of GET Endpoints to Configure:

1. **GET /v1/transactions/{transactionId}**
   - Select the method
   - Integration Request → Edit
   - Lambda Proxy integration: personal-finance-api-dev
   - Save → OK to add permission

2. **GET /v1/income**
   - Same Lambda function: personal-finance-api-dev

3. **GET /v1/income/summary**
   - Same Lambda function: personal-finance-api-dev

4. **GET /v1/expenses**
   - Same Lambda function: personal-finance-api-dev

5. **GET /v1/expenses/summary**
   - Same Lambda function: personal-finance-api-dev

6. **GET /v1/networth**
   - Same Lambda function: personal-finance-api-dev

7. **GET /v1/files**
   - Same Lambda function: personal-finance-api-dev

> **Tip**: Click OK each time the permission prompt appears. API Gateway creates a unique permission for each method.

### Step 5: Configure POST Endpoint (Files Upload)

The file upload endpoint may use a different Lambda function:

1. **Select POST /v1/files/upload-url**

2. **Configure Integration**:
   - Integration type: Lambda Function
   - Use Lambda Proxy integration: ✓
   - Lambda Function: `personal-finance-file-processor-dev`
   - Or use same `personal-finance-api-dev` if file handling is in same function
   - Save → OK

## 🔧 Understanding Lambda Permissions

### What Happens When You Click OK?

API Gateway adds a resource-based policy to your Lambda function:

```json
{
  "Sid": "apigateway-invoke-permission",
  "Effect": "Allow",
  "Principal": {
    "Service": "apigateway.amazonaws.com"
  },
  "Action": "lambda:InvokeFunction",
  "Resource": "arn:aws:lambda:region:account:function:function-name",
  "Condition": {
    "ArnLike": {
      "AWS:SourceArn": "arn:aws:execute-api:region:account:api-id/*"
    }
  }
}
```

### Verify Permissions (Optional)

Check Lambda function policy:

```bash
aws lambda get-policy \
  --function-name personal-finance-api-dev \
  | jq -r '.Policy' | jq
```

You should see statements allowing API Gateway to invoke the function.

## 🧪 Testing the Integration

### Test Individual Endpoint

1. **Select GET Method** (e.g., `/v1/transactions`)

2. **Click "Test"** (lightning bolt icon)

3. **Configure Test**:
   - Headers (optional):
     ```
     X-User-Id: test_user_123
     ```
   - Query Strings (optional):
     ```
     limit=10&startDate=2024-01-01
     ```

4. **Click "Test" Button**

5. **Review Response**:
   - **Status**: Should be 200
   - **Response Body**: JSON data from Lambda
   - **Logs**: Shows Lambda execution logs

### Expected Response Example:

```json
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"data\":[{\"id\":\"txn_001\",\"amount\":-45.67,...}]}"
}
```

### Test with Path Parameter

1. **Select GET /v1/transactions/{transactionId}**

2. **Click "Test"**

3. **Path** section:
   - Enter: `txn_001` (or any transaction ID)

4. **Click "Test"**

5. **Verify**: Response includes the specific transaction

## 📊 Method Execution Flow

After integration, each method shows this execution flow:

```
Method Request
    ↓
Integration Request
    ↓
Lambda Function
    ↓
Integration Response
    ↓
Method Response
```

### What Each Part Does:

- **Method Request**: Validates incoming request (auth, parameters)
- **Integration Request**: Transforms request for Lambda
- **Lambda Function**: Executes business logic
- **Integration Response**: Transforms Lambda response
- **Method Response**: Returns formatted response to client

With Lambda Proxy Integration:
- Integration Request/Response transformations are skipped
- Lambda receives raw request and returns formatted response

## 📋 Checklist

Verify Lambda integration for all endpoints:

- [ ] GET /v1/transactions → personal-finance-api-dev
- [ ] GET /v1/transactions/{transactionId} → personal-finance-api-dev
- [ ] GET /v1/income → personal-finance-api-dev
- [ ] GET /v1/income/summary → personal-finance-api-dev
- [ ] GET /v1/expenses → personal-finance-api-dev
- [ ] GET /v1/expenses/summary → personal-finance-api-dev
- [ ] GET /v1/networth → personal-finance-api-dev
- [ ] GET /v1/files → personal-finance-api-dev
- [ ] POST /v1/files/upload-url → file-processor Lambda
- [ ] All permissions granted (clicked OK for each)
- [ ] At least one endpoint tested successfully

## 🚨 Troubleshooting

### "Internal Server Error" (502)
**Problem**: Lambda returns 502 Bad Gateway
**Solution**:
1. Check Lambda function logs in CloudWatch
2. Verify Lambda response format (must have statusCode, headers, body)
3. Ensure Lambda has correct permissions

### "Execution failed due to configuration error"
**Problem**: API Gateway can't invoke Lambda
**Solution**:
1. Verify Lambda function exists and is in same region
2. Check that you clicked OK to add permissions
3. Run: `aws lambda get-policy --function-name personal-finance-api-dev`

### Test Shows "Missing Authentication Token"
**Problem**: Endpoint requires authorizer but none configured
**Solution**:
- We'll configure Cognito authorizer in the next step
- For now, ensure Method Request Authorization is set to NONE

### Lambda Response Not Parsing
**Problem**: Response body is double-encoded JSON
**Solution**:
- In Lambda, ensure body is a JSON string: `json.dumps(data)`
- Don't JSON-encode the entire response object

### Cannot Add Permission
**Problem**: Permission already exists error
**Solution**:
- Permission was already added
- Continue to next endpoint
- Or remove old permission and re-add:
  ```bash
  aws lambda remove-permission \
    --function-name personal-finance-api-dev \
    --statement-id apigateway-test-1
  ```

## 💡 Best Practices

1. **Use Lambda Proxy Integration**: Simplifies configuration
2. **Consistent Lambda Response**: Always return statusCode, headers, body
3. **Error Handling**: Return appropriate HTTP status codes from Lambda
4. **Logging**: Use structured logging in Lambda for debugging
5. **Test Each Endpoint**: Verify integration after configuration

## 🔄 Updating Lambda Function

After configuring integration:

1. **Code Changes**: Update Lambda function code as needed
2. **No API Gateway Changes**: Integration automatically uses latest code
3. **Lambda Versions**: Use versions/aliases for stage-specific deployments

## 📚 Additional Resources

- [Lambda Proxy Integration](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html)
- [Lambda Function Response Format](https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-output-format)
- [Testing API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-test-method.html)

## ✅ Completion

You've successfully integrated all API endpoints with Lambda functions!

**What's Next**: Configure Cognito authorizer for authentication.

---

**Next Step**: [Cognito Authorizer](./05-cognito-authorizer.md) →

**Previous Step**: [← Resources and Methods](./03-resources-methods.md)

**Back to**: [Manual Setup Guide](./README.md)
