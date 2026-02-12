# SECRET_HASH Error - Quick Fix Guide

## Problem

Users getting error when trying to login:
```
Client <id> is configured with secret but SECRET_HASH was not received
```

## Root Cause

The Cognito App Client is configured with a **client secret**. This is incorrect for frontend applications:

- ❌ **Confidential Client** (with secret): For backend/server applications
- ✅ **Public Client** (no secret): For frontend/mobile applications

## Why This Matters

Frontend applications run in the browser where code can be inspected. Having a client secret in frontend code:
- Provides no actual security (anyone can extract it)
- Causes authentication to fail with modern AWS Amplify versions
- Violates OAuth 2.0 best practices for public clients

## Solution

### Recommended: Reconfigure App Client (5 minutes)

This is the proper fix that addresses the root cause:

**Step 1: Create a new public App Client**

1. Go to AWS Console > Amazon Cognito
2. Select your User Pool
3. Click **App integration** tab
4. Scroll to **App client list**
5. Click **Create app client**

**Step 2: Configure the new client**

```
App client name: personal-finance-app-public
App type: ✓ Public client (no secret)

Authentication flows:
✓ ALLOW_USER_PASSWORD_AUTH
✓ ALLOW_REFRESH_TOKEN_AUTH

OAuth 2.0 grant types:
✓ Authorization code grant

OAuth scopes:
✓ openid
✓ email  
✓ profile

Callback URLs:
http://localhost:3000/
http://localhost:3000/callback
https://your-production-domain.com/ (for production)

Sign-out URLs:
http://localhost:3000/
https://your-production-domain.com/ (for production)
```

6. Click **Create app client**
7. **Copy the new App client ID**

**Step 3: Update your frontend configuration**

Edit `frontend/src/aws-config.js`:

```javascript
userPoolClientId: 'your_new_public_client_id', // Replace with new client ID
// Remove or comment out userPoolClientSecret line
```

**Step 4: Test**

```bash
cd frontend
npm start
```

Try logging in - the error should be resolved!

**Step 5: Clean up (Optional)**

You can delete the old app client with the secret:
1. Go to App integration > App client list
2. Select the old client
3. Click **Delete**

### Alternative: Add Client Secret (NOT RECOMMENDED)

⚠️ **Warning**: This approach has security implications and should only be used temporarily.

If you cannot reconfigure the App Client immediately, you can add the secret to your configuration:

1. Get your client secret from AWS Console:
   - Cognito > User Pools > [Your Pool] > App integration
   - Click on your app client
   - Click **Show client secret**
   - Copy the value

2. Add to `frontend/src/aws-config.js`:

```javascript
userPoolClientId: 'your_client_id',
userPoolClientSecret: 'your_client_secret', // Add this line
```

**Better: Use environment variables**

Create `frontend/.env.local`:
```bash
REACT_APP_COGNITO_APP_CLIENT_SECRET=your_actual_client_secret
```

Update `frontend/src/aws-config.js`:
```javascript
userPoolClientSecret: process.env.REACT_APP_COGNITO_APP_CLIENT_SECRET,
```

**Why this is not recommended:**
- The secret will be visible in your JavaScript bundle
- Anyone can extract it from browser DevTools
- It provides no actual security benefit
- It's against OAuth 2.0 best practices

## How to Verify Your Fix

### Check if your App Client has a secret:

1. AWS Console > Cognito > User Pools > [Your Pool]
2. App integration > App client list
3. Click on your app client
4. Look for "Client secret" field:
   - ✅ If it says "No client secret", you're using a public client (correct!)
   - ❌ If it shows a secret value, you need to reconfigure (or use the workaround)

### Test authentication:

1. Start your app: `npm start`
2. Navigate to login page
3. Enter valid credentials
4. Click "Sign In"
5. Expected: Successful login and redirect to dashboard
6. If you see the SECRET_HASH error again, verify:
   - You're using the correct App Client ID
   - The App Client is truly a public client (no secret)
   - You've restarted your development server

## Key Takeaways

1. **Frontend apps must use public clients** (no secret)
2. **Backend apps use confidential clients** (with secret)
3. **Never commit secrets to version control** (use .env files)
4. **Client secrets in frontend code are insecure** (anyone can see them)

## Additional Help

For more details, see:
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) - Comprehensive troubleshooting guide
- [COGNITO_SETUP.md](./COGNITO_SETUP.md) - Full Cognito setup instructions
- [AWS Cognito Documentation](https://docs.aws.amazon.com/cognito/)

## Quick Decision Tree

```
Is your App Client configured with a secret?
│
├─ YES → Need to fix this
│   │
│   ├─ Can you reconfigure? → YES
│   │   └─ ✓ Create new public client (RECOMMENDED)
│   │
│   └─ Can you reconfigure? → NO
│       └─ ⚠ Add secret to config (TEMPORARY)
│
└─ NO → Good! Your configuration is correct
    └─ Check other authentication issues
```

## Reference Links

- [OAuth 2.0 for Public Clients](https://datatracker.ietf.org/doc/html/rfc6749#section-2.1)
- [AWS Amplify Authentication](https://docs.amplify.aws/lib/auth/getting-started/q/platform/js/)
- [Cognito App Client Settings](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-client-apps.html)
