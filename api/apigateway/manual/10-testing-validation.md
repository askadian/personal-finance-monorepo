# Testing and Validation

This guide provides comprehensive testing procedures to validate your API Gateway setup.

## 📋 Overview

In this final step, you will:
1. Test all endpoints systematically
2. Validate authentication and authorization
3. Test CORS functionality
4. Verify error handling
5. Conduct performance testing
6. Document test results

**Estimated Time**: 30-45 minutes

## 🧪 Testing Checklist

### Authentication Testing

- [ ] Request without token returns 401
- [ ] Request with invalid token returns 401
- [ ] Request with expired token returns 401
- [ ] Request with valid token returns 200
- [ ] Token is validated by Cognito authorizer

### Endpoint Testing

Test each endpoint with valid authentication:

- [ ] GET /v1/transactions
- [ ] GET /v1/transactions/{transactionId}
- [ ] GET /v1/income
- [ ] GET /v1/income/summary
- [ ] GET /v1/expenses
- [ ] GET /v1/expenses/summary
- [ ] GET /v1/networth
- [ ] GET /v1/files
- [ ] POST /v1/files/upload-url

### CORS Testing

- [ ] OPTIONS requests return 200
- [ ] CORS headers present in responses
- [ ] Browser requests work without CORS errors

### Error Handling

- [ ] 400 Bad Request for invalid parameters
- [ ] 401 Unauthorized for missing/invalid auth
- [ ] 404 Not Found for non-existent resources
- [ ] 500 Internal Server Error handled gracefully

## 🚀 Testing Methods

### Method 1: AWS Console Test Feature

1. **Navigate to API Gateway**

2. **Select Resource and Method** (e.g., GET /v1/transactions)

3. **Click Test** (lightning bolt icon)

4. **Add Headers**:
   ```
   Authorization: Bearer YOUR_JWT_TOKEN
   ```

5. **Add Query Strings** (if applicable):
   ```
   limit=10
   startDate=2024-01-01
   ```

6. **Click Test**

7. **Verify Response**:
   - Status: 200
   - Headers include CORS
   - Body contains expected data

### Method 2: curl Command Line

#### Get JWT Token

```bash
# Authenticate with Cognito
TOKEN=$(aws cognito-idp initiate-auth \
  --auth-flow USER_PASSWORD_AUTH \
  --client-id YOUR_CLIENT_ID \
  --auth-parameters USERNAME=test@example.com,PASSWORD=YourPassword123! \
  --query 'AuthenticationResult.IdToken' \
  --output text)

echo $TOKEN
```

#### Test Endpoints

```bash
# Base URL
BASE_URL="https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/dev"

# Test GET /v1/transactions
curl -i "$BASE_URL/v1/transactions" \
  -H "Authorization: Bearer $TOKEN"

# Test with query parameters
curl -i "$BASE_URL/v1/transactions?limit=5&startDate=2024-01-01" \
  -H "Authorization: Bearer $TOKEN"

# Test specific transaction
curl -i "$BASE_URL/v1/transactions/txn_001" \
  -H "Authorization: Bearer $TOKEN"

# Test income
curl -i "$BASE_URL/v1/income" \
  -H "Authorization: Bearer $TOKEN"

# Test income summary
curl -i "$BASE_URL/v1/income/summary" \
  -H "Authorization: Bearer $TOKEN"

# Test expenses
curl -i "$BASE_URL/v1/expenses" \
  -H "Authorization: Bearer $TOKEN"

# Test expenses summary
curl -i "$BASE_URL/v1/expenses/summary" \
  -H "Authorization: Bearer $TOKEN"

# Test net worth
curl -i "$BASE_URL/v1/networth" \
  -H "Authorization: Bearer $TOKEN"

# Test files
curl -i "$BASE_URL/v1/files" \
  -H "Authorization: Bearer $TOKEN"

# Test file upload URL
curl -i -X POST "$BASE_URL/v1/files/upload-url" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fileName":"test.pdf","fileType":"application/pdf"}'
```

#### Test Authentication

```bash
# Test without token (should return 401)
curl -i "$BASE_URL/v1/transactions"

# Test with invalid token (should return 401)
curl -i "$BASE_URL/v1/transactions" \
  -H "Authorization: Bearer invalid_token_here"
```

#### Test CORS

```bash
# Test OPTIONS preflight
curl -i -X OPTIONS "$BASE_URL/v1/transactions" \
  -H "Origin: https://example.com" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: Authorization"

# Should return CORS headers:
# Access-Control-Allow-Origin: *
# Access-Control-Allow-Methods: GET,OPTIONS
# Access-Control-Allow-Headers: ...
```

### Method 3: Postman Collection

1. **Import Collection**:
   - Open Postman
   - Import from `api/collections/postman/personal-finance-api.postman_collection.json`

2. **Import Environment**:
   - Import staging or dev environment
   - Update `base_url` with your API Gateway URL
   - Update `access_token` with your JWT token

3. **Run Collection**:
   - Select collection
   - Click **Run** button
   - Select environment
   - Run entire collection or individual requests

4. **Review Results**:
   - All tests should pass
   - Check response times
   - Verify response structure

### Method 4: Bruno Collection

1. **Open Bruno**

2. **Open Collection**:
   - Navigate to `api/collections/bruno/personal-finance-api`

3. **Configure Environment**:
   - Select environment (dev/staging/prod)
   - Update `base_url`
   - Update `access_token`

4. **Test Endpoints**:
   - Run individual requests
   - View responses and test results

### Method 5: Browser Testing

Create a simple HTML file to test from browser:

```html
<!DOCTYPE html>
<html>
<head>
    <title>API Gateway Test</title>
</head>
<body>
    <h1>Personal Finance API Test</h1>
    <button onclick="testAPI()">Test API</button>
    <pre id="output"></pre>

    <script>
        const API_URL = 'https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/dev';
        const TOKEN = 'YOUR_JWT_TOKEN';

        async function testAPI() {
            const output = document.getElementById('output');
            output.textContent = 'Testing...';

            try {
                const response = await fetch(`${API_URL}/v1/transactions`, {
                    headers: {
                        'Authorization': `Bearer ${TOKEN}`
                    }
                });

                const data = await response.json();
                output.textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                output.textContent = `Error: ${error.message}`;
            }
        }
    </script>
</body>
</html>
```

## 📊 Validation Tests

### Test Request Flow

```bash
# 1. Test authentication flow
echo "Testing: No auth token (expect 401)"
curl -s -o /dev/null -w "%{http_code}\n" "$BASE_URL/v1/transactions"

echo "Testing: Valid auth token (expect 200)"
curl -s -o /dev/null -w "%{http_code}\n" "$BASE_URL/v1/transactions" \
  -H "Authorization: Bearer $TOKEN"

# 2. Test query parameters
echo "Testing: With query parameters"
curl -s "$BASE_URL/v1/transactions?limit=5" \
  -H "Authorization: Bearer $TOKEN" | jq '.data | length'

# 3. Test path parameters
echo "Testing: Specific transaction ID"
curl -s "$BASE_URL/v1/transactions/txn_001" \
  -H "Authorization: Bearer $TOKEN" | jq '.data.id'

# 4. Test error handling
echo "Testing: Non-existent resource (expect 404)"
curl -s -o /dev/null -w "%{http_code}\n" "$BASE_URL/v1/transactions/invalid_id" \
  -H "Authorization: Bearer $TOKEN"
```

### Performance Testing

```bash
# Test latency
for i in {1..10}; do
  curl -s -o /dev/null -w "Request $i: %{time_total}s\n" \
    "$BASE_URL/v1/transactions" \
    -H "Authorization: Bearer $TOKEN"
done

# Load testing (using apache bench if installed)
ab -n 100 -c 10 \
  -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/v1/transactions"
```

## 🔍 Monitoring During Tests

While testing, monitor:

### CloudWatch Logs

1. **Open CloudWatch Console**

2. **Navigate to Log Groups**:
   - `/aws/apigateway/personal-finance-api`
   - `/aws/lambda/personal-finance-api-dev`

3. **View Real-time Logs**:
   - Watch for errors
   - Verify request flow
   - Check response times

### CloudWatch Metrics

1. **Dashboard**: View API Gateway dashboard

2. **Monitor**:
   - Request count increasing
   - Low error rate (< 1%)
   - Acceptable latency (< 1s average)

### X-Ray Traces

1. **Open X-Ray Console**

2. **View Service Map**:
   - API Gateway → Lambda → DynamoDB
   - Check for errors or high latency

3. **Analyze Traces**:
   - View individual request traces
   - Identify bottlenecks

## 📋 Test Results Documentation

Create a test results summary:

```markdown
# API Gateway Test Results

**Date**: 2024-XX-XX
**Tester**: Your Name
**Environment**: Development

## Test Results

### Authentication Tests
- ✅ Unauthorized access (no token) returns 401
- ✅ Invalid token returns 401
- ✅ Valid token returns 200

### Endpoint Tests
- ✅ GET /v1/transactions - Response time: 245ms
- ✅ GET /v1/transactions/{id} - Response time: 189ms
- ✅ GET /v1/income - Response time: 203ms
- ✅ GET /v1/income/summary - Response time: 312ms
- ✅ GET /v1/expenses - Response time: 198ms
- ✅ GET /v1/expenses/summary - Response time: 287ms
- ✅ GET /v1/networth - Response time: 334ms
- ✅ GET /v1/files - Response time: 176ms
- ✅ POST /v1/files/upload-url - Response time: 423ms

### CORS Tests
- ✅ OPTIONS preflight returns 200
- ✅ CORS headers present in responses
- ✅ Browser requests work without errors

### Performance
- Average latency: 254ms
- P99 latency: 450ms
- Error rate: 0%

## Issues Found
None

## Recommendations
- Consider enabling caching for frequently accessed endpoints
- Monitor performance in production
```

## 🚨 Troubleshooting Failed Tests

### 401 Unauthorized with Valid Token
**Check**:
1. Token not expired (tokens expire after 1 hour)
2. Cognito authorizer configured correctly
3. Token source header is "Authorization"

### 502 Bad Gateway
**Check**:
1. Lambda function logs in CloudWatch
2. Lambda returns proper response format
3. Lambda has correct permissions

### CORS Errors in Browser
**Check**:
1. OPTIONS method exists and returns 200
2. OPTIONS method has no authorizer
3. CORS headers configured correctly
4. API is deployed

### Slow Response Times
**Check**:
1. Lambda cold start times
2. DynamoDB performance
3. Consider Lambda provisioned concurrency
4. Enable API caching

## ✅ Final Validation

Before considering setup complete:

- [ ] All endpoints return expected responses
- [ ] Authentication works correctly
- [ ] CORS configured and working
- [ ] Error handling appropriate
- [ ] Performance acceptable (< 1s average)
- [ ] CloudWatch logs working
- [ ] CloudWatch metrics showing data
- [ ] X-Ray traces visible
- [ ] Alarms configured and tested
- [ ] Documentation updated

## 📚 Additional Resources

- [API Gateway Testing](https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-test-method.html)
- [API Testing Best Practices](https://aws.amazon.com/blogs/compute/best-practices-for-organizing-larger-serverless-applications/)
- [Performance Testing](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)

## 🎉 Congratulations!

You've successfully set up, configured, and tested your API Gateway!

Your API is now ready for:
- Frontend integration
- Further development
- Production deployment

---

**Previous Step**: [← Monitoring and Logging](./09-monitoring-logging.md)

**Back to**: [Manual Setup Guide](./README.md)

**Main Documentation**: [API Gateway README](../README.md)
