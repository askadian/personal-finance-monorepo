# CORS Configuration

This guide walks through configuring Cross-Origin Resource Sharing (CORS) to enable web applications to access your API.

## 📋 Overview

In this step, you will:
1. Understand CORS requirements
2. Add OPTIONS methods for preflight requests
3. Configure CORS headers
4. Test CORS functionality

**Estimated Time**: 15-20 minutes

## 🌐 What is CORS?

Cross-Origin Resource Sharing (CORS) allows web browsers to make requests to your API from a different domain.

### Why CORS is Needed

Web browsers enforce Same-Origin Policy:
- ❌ Frontend at `https://myapp.com` cannot call API at `https://api.example.com`
- ✅ Unless API explicitly allows it via CORS headers

### CORS Workflow

```
Browser                      API Gateway
   |                              |
   |--- Preflight (OPTIONS) ----->|
   |<---- CORS Headers ----------|
   |                              |
   |--- Actual Request (GET) ---->|
   |<---- Response + CORS --------|
```

## 🚀 Step-by-Step Instructions

### Step 1: Add OPTIONS Method (Manual Approach)

For each resource that needs CORS, add an OPTIONS method:

#### Example: /v1/transactions

1. **Select /v1/transactions resource**

2. **Create Method**
   - Actions → Create Method
   - Select **OPTIONS**
   - Click checkmark ✓

3. **Setup Mock Integration**:
   - Integration type: **Mock**
   - Click **Save**

4. **Configure Method Response**:
   - Click **Method Response**
   - Expand **200** response
   - Click **Add Header**:
     - `Access-Control-Allow-Origin`
     - `Access-Control-Allow-Methods`
     - `Access-Control-Allow-Headers`

5. **Configure Integration Response**:
   - Click **Integration Response**
   - Expand **200** response
   - For each header, click **Add mapping**:
     - `Access-Control-Allow-Origin`: `'*'`
     - `Access-Control-Allow-Methods`: `'GET,OPTIONS'`
     - `Access-Control-Allow-Headers`: `'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'`

### Step 2: Enable CORS Automatically (Recommended)

API Gateway provides a shortcut to enable CORS:

#### For Each Resource:

1. **Select resource** (e.g., /v1/transactions)

2. **Actions → Enable CORS**

3. **Configure CORS**:
   - **Access-Control-Allow-Origin**: `*` or specific domain
   - **Access-Control-Allow-Headers**: 
     ```
     Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token
     ```
   - **Access-Control-Allow-Methods**: Select methods (GET, POST, OPTIONS)

4. **Click "Enable CORS and replace existing CORS headers"**

5. **Click "Yes, replace existing values"**

API Gateway will:
- Create OPTIONS method if it doesn't exist
- Add necessary response headers
- Configure mock integration

### Step 3: Configure CORS for All Resources

Enable CORS for these resources:

- [ ] /v1/transactions
- [ ] /v1/transactions/{transactionId}
- [ ] /v1/income
- [ ] /v1/income/summary
- [ ] /v1/expenses
- [ ] /v1/expenses/summary
- [ ] /v1/networth
- [ ] /v1/files
- [ ] /v1/files/upload-url

### Step 4: Ensure Lambda Returns CORS Headers

Your Lambda function must also return CORS headers in responses:

```python
def create_response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    """Create a standardized API Gateway response with CORS"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'GET,OPTIONS'
        },
        'body': json.dumps(body)
    }
```

### Step 5: Verify OPTIONS Method Configuration

For each resource with CORS enabled:

1. **Check OPTIONS method exists**
2. **Verify Authorization is NONE** (no authorizer on OPTIONS)
3. **Verify Integration Response headers** are configured

## 🧪 Testing CORS

### Test OPTIONS Request (Preflight)

1. **Select OPTIONS method** on any resource

2. **Click Test**

3. **Review Response**:
   - Status: **200**
   - Headers should include:
     - `Access-Control-Allow-Origin: *`
     - `Access-Control-Allow-Methods: GET,OPTIONS`
     - `Access-Control-Allow-Headers: ...`

### Test from Browser Console

After deploying (covered in next guide), test from browser:

```javascript
// In browser console
fetch('https://your-api-url/v1/transactions', {
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN'
  }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

### Expected Behavior:
- ✅ Browser makes OPTIONS preflight request
- ✅ API returns CORS headers
- ✅ Browser makes actual GET request
- ✅ API returns data with CORS headers

## 🔍 Understanding CORS Headers

### Access-Control-Allow-Origin

Controls which domains can access your API:

- `*`: Allow all domains (development/public APIs)
- `https://myapp.com`: Allow specific domain (production)
- Multiple domains: Requires dynamic header in Lambda

### Access-Control-Allow-Methods

Lists allowed HTTP methods:

```
GET,POST,PUT,DELETE,OPTIONS
```

### Access-Control-Allow-Headers

Lists headers the client can send:

```
Content-Type,Authorization,X-Api-Key,X-Amz-Date,X-Amz-Security-Token
```

**Must include**: `Authorization` for Cognito authentication

### Access-Control-Allow-Credentials

Required when sending cookies or authentication:

```
true
```

**Note**: Cannot use with `Access-Control-Allow-Origin: *`

## 📋 Checklist

- [ ] OPTIONS method added to all resources
- [ ] OPTIONS methods have NO authorizer
- [ ] CORS headers configured on OPTIONS methods
- [ ] Lambda returns CORS headers in all responses
- [ ] Tested OPTIONS request returns 200
- [ ] Tested CORS headers are present

## 🚨 Troubleshooting

### CORS Error in Browser
**Problem**: "CORS policy: No 'Access-Control-Allow-Origin' header"
**Solution**:
1. Verify OPTIONS method exists and returns 200
2. Check Lambda returns CORS headers
3. Ensure Authorization is NONE on OPTIONS
4. Deploy API (changes don't take effect until deployed)

### Preflight Request Fails (401)
**Problem**: OPTIONS returns 401 Unauthorized
**Solution**:
- OPTIONS method must not have authorizer
- Change Method Request Authorization to NONE

### CORS Works in Console but Not Browser
**Problem**: Test in console works, browser fails
**Solution**:
1. Deploy API to a stage
2. Test with deployed URL, not test invoke URL
3. Check browser console for specific error

### Multiple CORS Headers
**Problem**: Response has duplicate CORS headers
**Solution**:
- Remove CORS headers from Lambda response
- Or remove from API Gateway Integration Response
- Keep headers in only one place

## 💡 Best Practices

### For Development:
```
Access-Control-Allow-Origin: *
```
Simple and allows testing from any domain.

### For Production:
```python
# In Lambda function
def get_cors_origin(event):
    """Return appropriate CORS origin based on request"""
    origin = event.get('headers', {}).get('origin', '')
    
    allowed_origins = [
        'https://app.example.com',
        'https://staging.example.com'
    ]
    
    if origin in allowed_origins:
        return origin
    
    return 'https://app.example.com'  # default

def create_response(status_code, body, event):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': get_cors_origin(event),
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Headers': '...',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
        },
        'body': json.dumps(body)
    }
```

### Security Considerations

1. **Avoid `*` in Production**: Specify exact domains
2. **Use HTTPS**: Always use secure protocols
3. **Limit Methods**: Only allow necessary HTTP methods
4. **Limit Headers**: Only allow required headers

## 📚 Additional Resources

- [CORS Support in API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-cors.html)
- [CORS MDN Documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Enabling CORS for Lambda Proxy Integration](https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-cors-console.html)

## ✅ Completion

You've successfully configured CORS!

**What's Next**: Deploy your API to stages for testing and production use.

---

**Next Step**: [Deployment and Stages](./07-deployment-stages.md) →

**Previous Step**: [← Cognito Authorizer](./05-cognito-authorizer.md)

**Back to**: [Manual Setup Guide](./README.md)
