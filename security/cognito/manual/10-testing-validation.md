# Testing and Validation

Comprehensive testing guide for your Cognito User Pool setup.

## 📋 Overview

Verify your Cognito User Pool is working correctly with end-to-end testing.

**Estimated Time**: 20 minutes

## Test Checklist

### 1. Sign Up Flow
- [ ] Navigate to Hosted UI
- [ ] Click "Sign up"
- [ ] Enter email and password
- [ ] Receive verification email
- [ ] Enter verification code
- [ ] Account created successfully

### 2. Sign In Flow
- [ ] Navigate to Hosted UI
- [ ] Enter email and password
- [ ] Successfully authenticated
- [ ] Redirected to callback URL
- [ ] Receive authorization code
- [ ] Exchange code for tokens

### 3. Token Validation
- [ ] Receive ID token
- [ ] Receive access token
- [ ] Receive refresh token
- [ ] Tokens have correct expiration
- [ ] Tokens contain expected claims

### 4. Password Reset Flow
- [ ] Click "Forgot password"
- [ ] Enter email
- [ ] Receive reset code
- [ ] Enter code and new password
- [ ] Password successfully reset
- [ ] Can log in with new password

### 5. API Integration
- [ ] Include access token in API request
- [ ] API Gateway validates token
- [ ] Request reaches Lambda
- [ ] User context available in Lambda

## Testing Tools

**JWT Decoder:**
- Use jwt.io to decode and inspect tokens

**Postman/Bruno:**
- Test API calls with tokens
- Collection available in `/api/collections`

**AWS CLI:**
```bash
# Create test user
aws cognito-idp admin-create-user \
  --user-pool-id us-east-1_XXXXXXXXX \
  --username testuser@example.com

# Set permanent password
aws cognito-idp admin-set-user-password \
  --user-pool-id us-east-1_XXXXXXXXX \
  --username testuser@example.com \
  --password "TempPassword123!" \
  --permanent
```

## Verification

✅ **Success criteria:**
- Users can sign up
- Email verification works
- Users can sign in
- Tokens are issued
- API calls with tokens succeed
- Password reset works
- MFA works (if enabled)

## Common Issues

### Email not received
- Check spam folder
- Verify email configuration
- Check Cognito sending limits

### Token validation fails
- Verify User Pool ID in API Gateway
- Check token expiration
- Verify token signature

### Callback URL mismatch
- Ensure exact URL match
- Check for trailing slashes
- Verify protocol (http/https)

---

**Previous**: [Lambda Triggers](./09-triggers-lambda.md)

**Setup Complete!** Your Cognito User Pool is ready for integration with your application.
