# Cognito Authorizer Setup

This guide walks through configuring AWS Cognito User Pool authorizer for API authentication.

## 📋 Overview

In this step, you will:
1. Create a Cognito authorizer in API Gateway
2. Configure JWT token validation
3. Apply authorizer to API methods
4. Test authentication

**Estimated Time**: 15-20 minutes

## 🔐 What is a Cognito Authorizer?

A Cognito authorizer validates JWT tokens from AWS Cognito User Pools:

- **Client** sends request with `Authorization: Bearer <JWT_TOKEN>`
- **API Gateway** validates token with Cognito
- **If valid**: Request proceeds to Lambda
- **If invalid**: Returns 401 Unauthorized

## 🚀 Step-by-Step Instructions

### Step 1: Navigate to Authorizers

1. **Open API Gateway Console**
   - Select your API: `personal-finance-api`

2. **Click "Authorizers"** in left sidebar

3. **Click "Create New Authorizer"**

### Step 2: Create Cognito Authorizer

Configure the authorizer:

**Name:**
```
cognito-authorizer
```

**Type:**
- Select **Cognito**

**Cognito User Pool:**
- Select your Cognito User Pool from dropdown
- Or enter User Pool ID: `us-east-1_XXXXXXXXX`

**Token Source:**
```
Authorization
```

> This tells API Gateway to look for the token in the `Authorization` header

**Token Validation:**
- Leave as default (validates signature, expiration, etc.)

**Authorization Caching:**
- **Enable** (recommended for performance)
- **TTL**: 300 seconds (5 minutes)

**Click "Create"**

### Step 3: Test the Authorizer

Before applying to methods, test the authorizer:

1. **Click "Test" on your authorizer**

2. **Enter Test Token**:
   - Use the JWT token from your test user (from Prerequisites)
   - Format: `Bearer eyJhbGc...`
   - Or just the token without "Bearer" prefix

3. **Click "Test"**

4. **Verify Response**:
   - **Response Code**: 200
   - **Claims**: Shows user details from token
   - **Principal ID**: User's sub (unique ID)

Example response:
```json
{
  "principalId": "a1b2c3d4-5678-90ab-cdef-EXAMPLE11111",
  "policyDocument": {...},
  "context": {
    "sub": "a1b2c3d4-5678-90ab-cdef-EXAMPLE11111",
    "email": "testuser@example.com",
    "cognito:username": "testuser"
  }
}
```

### Step 4: Apply Authorizer to Methods

Now apply the authorizer to all protected endpoints:

#### Method 1: Apply to Individual Methods

1. **Select a Method** (e.g., GET /v1/transactions)

2. **Click "Method Request"**

3. **Click Edit**

4. **Authorization**:
   - Change from **NONE** to **cognito-authorizer**

5. **Click Save** (checkmark)

6. **Repeat** for all methods that need authentication

#### Method 2: Apply to All Methods at Once (Faster)

1. **Select Root Resource** (`/v1`)

2. **Click Actions** dropdown

3. **Select "Apply Authorizer to Resources"**
   - Not available in all consoles; if not, use Method 1

4. **Select** your authorizer and resources

5. **Apply**

### Step 5: Configure Methods with Authorizer

Apply the authorizer to these endpoints:

- [ ] GET /v1/transactions
- [ ] GET /v1/transactions/{transactionId}
- [ ] GET /v1/income
- [ ] GET /v1/income/summary
- [ ] GET /v1/expenses
- [ ] GET /v1/expenses/summary
- [ ] GET /v1/networth
- [ ] GET /v1/files
- [ ] POST /v1/files/upload-url

> **Note**: OPTIONS methods should NOT have authorizers (needed for CORS preflight)

## 🧪 Testing Authentication

### Test with Valid Token

1. **Get a Fresh Token**:
```bash
aws cognito-idp initiate-auth \
  --auth-flow USER_PASSWORD_AUTH \
  --client-id YOUR_CLIENT_ID \
  --auth-parameters USERNAME=testuser@example.com,PASSWORD=MyPassword123! \
  --query 'AuthenticationResult.IdToken' \
  --output text
```

2. **Test in API Gateway Console**:
   - Select a method (e.g., GET /v1/transactions)
   - Click **Test**
   - Add Header:
     - Name: `Authorization`
     - Value: `Bearer YOUR_TOKEN_HERE`
   - Click **Test**
   - Should return 200 with data

### Test with Invalid Token

1. **Test in Console**:
   - Select a method
   - Click **Test**
   - Don't add Authorization header
   - Click **Test**
   - Should return **401 Unauthorized**

2. **Or add invalid token**:
   - Authorization: `Bearer invalid_token`
   - Should return **401 Unauthorized**

## 🔍 Understanding Token Flow

### Request Flow with Authorizer:

```
Client Request
    ↓
    + Authorization: Bearer <token>
    ↓
API Gateway
    ↓
Cognito Authorizer
    ↓
Validates Token:
  - Signature valid?
  - Not expired?
  - From correct User Pool?
    ↓
  [Valid] ────→ Lambda Function
    ↓            ↓
  [Invalid] → 401 Unauthorized
```

### Lambda Receives User Context

With Cognito authorizer, Lambda receives user information:

```python
def lambda_handler(event, context):
    # User info from Cognito
    user_id = event['requestContext']['authorizer']['claims']['sub']
    email = event['requestContext']['authorizer']['claims']['email']
    username = event['requestContext']['authorizer']['claims']['cognito:username']
    
    # Use user_id for data filtering
    # ...
```

## 📝 Update Lambda to Use Cognito User

Update your Lambda function to extract user from Cognito instead of header:

```python
def get_user_id(event: Dict[str, Any]) -> Optional[str]:
    """Extract user ID from Cognito authorizer context"""
    try:
        # Get from Cognito claims
        authorizer = event.get('requestContext', {}).get('authorizer', {})
        user_id = authorizer.get('claims', {}).get('sub')
        
        # Fallback to header for testing without Cognito
        if not user_id:
            user_id = event.get('headers', {}).get('X-User-Id')
        
        return user_id
    except Exception:
        return None
```

## 📋 Checklist

- [ ] Cognito authorizer created
- [ ] Authorizer tested with valid token
- [ ] Authorizer applied to all protected methods
- [ ] OPTIONS methods do NOT have authorizer
- [ ] Test with valid token succeeds (200)
- [ ] Test without token fails (401)
- [ ] Lambda function updated to use Cognito claims

## 🚨 Troubleshooting

### 401 Unauthorized with Valid Token
**Problem**: Valid token returns 401
**Solution**:
1. Verify authorizer Token Source is "Authorization"
2. Check token format: `Bearer <token>` or just `<token>`
3. Ensure token is not expired (tokens expire after 1 hour)
4. Verify User Pool ID is correct
5. Check CloudWatch logs for specific error

### Authorizer Test Fails
**Problem**: Test authorizer returns error
**Solution**:
1. Get a fresh token from Cognito
2. Verify User Pool ID is correct
3. Check that user exists in User Pool
4. Ensure App Client has authentication enabled

### Lambda Still Uses X-User-Id Header
**Problem**: Lambda doesn't recognize Cognito user
**Solution**:
1. Update Lambda code to extract from requestContext
2. Deploy Lambda function changes
3. Test again in API Gateway console

### Token Works in Console but Not from App
**Problem**: Console test works, but real requests fail
**Solution**:
1. Check CORS headers (next guide)
2. Verify frontend sends Authorization header
3. Check browser console for CORS errors
4. Ensure token is passed correctly from frontend

## 💡 Best Practices

1. **Token Caching**: Enable caching to reduce Cognito calls
2. **Cache TTL**: 5 minutes balances performance and security
3. **Token Expiration**: Cognito tokens expire after 1 hour
4. **Refresh Tokens**: Implement token refresh in frontend
5. **Error Messages**: Generic error messages prevent information leakage

## 🔒 Security Considerations

### Token Security
- ✅ Always use HTTPS (enforced by API Gateway)
- ✅ Store tokens securely (httpOnly cookies or secure storage)
- ✅ Never log or expose tokens
- ✅ Implement token refresh before expiration
- ✅ Use short-lived access tokens

### User Data
- ✅ Extract user ID from Cognito claims (not client-provided)
- ✅ Validate user has permission to access requested resources
- ✅ Filter data by authenticated user ID

## 📚 Additional Resources

- [Cognito User Pool Authorizers](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-integrate-with-cognito.html)
- [Cognito JWT Tokens](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-with-identity-providers.html)
- [API Gateway Authorization](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-control-access-to-api.html)

## ✅ Completion

You've successfully configured Cognito authentication!

**What's Next**: Configure CORS to enable browser-based applications.

---

**Next Step**: [CORS Configuration](./06-cors-configuration.md) →

**Previous Step**: [← Lambda Integration](./04-lambda-integration.md)

**Back to**: [Manual Setup Guide](./README.md)
