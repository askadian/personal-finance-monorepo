# Troubleshooting Guide

This guide helps resolve common issues with the Personal Finance Tracker frontend application.

## Authentication Issues

### Error: "Client is configured with secret but SECRET_HASH was not received"

**Symptom**: When trying to login, you see this error in the console or as an error message.

**Root Cause**: Your AWS Cognito App Client is configured with a client secret. AWS Amplify detects this and requires a SECRET_HASH parameter, but frontend applications (public clients) should not have client secrets.

**Solution Options**:

#### Option 1: Reconfigure App Client (RECOMMENDED)

This is the best practice approach:

1. **Go to AWS Console > Cognito > User Pools**
2. Select your User Pool
3. Go to **App integration** tab
4. Under **App client list**, you have two options:

   **Option A: Create a new public client (Recommended)**
   - Click **Create app client**
   - Name: `personal-finance-app-public`
   - App type: **Public client** (no client secret)
   - Authentication flows: Enable `ALLOW_USER_PASSWORD_AUTH`, `ALLOW_REFRESH_TOKEN_AUTH`
   - OAuth 2.0 grant types: `Authorization code grant`
   - OAuth scopes: `email`, `openid`, `profile`
   - Configure callback and sign-out URLs (same as before)
   - Click **Create**
   - Update `aws-config.js` with the new App Client ID

   **Option B: Modify existing client**
   - Click on your existing app client
   - Unfortunately, you cannot remove a client secret once created
   - You must delete and recreate the client (Option A)

2. **Update your frontend configuration**:
   - Open `frontend/src/aws-config.js`
   - Update `userPoolClientId` with the new public client ID
   - Remove or comment out `userPoolClientSecret` field

3. **Test the login**:
   - Restart your application
   - Try logging in again
   - The error should be resolved

#### Option 2: Add Client Secret to Configuration (NOT RECOMMENDED)

⚠️ **Warning**: This is not recommended for production applications as it exposes the client secret in frontend code, which is a security risk.

Use this only if:
- You cannot reconfigure the App Client immediately
- You need a quick temporary workaround
- You understand the security implications

**Steps**:

1. **Get your App Client Secret**:
   - AWS Console > Cognito > User Pools > [Your Pool]
   - App integration > App client list
   - Click on your app client
   - Click "Show client secret"
   - Copy the secret value

2. **Add to configuration**:
   
   In `aws-config.js`:
   ```javascript
   userPoolClientId: 'your_actual_client_id',
   userPoolClientSecret: 'your_actual_client_secret', // Add this line
   ```

   Or use environment variables (better):
   
   Create `.env.local`:
   ```
   REACT_APP_COGNITO_APP_CLIENT_SECRET=your_actual_client_secret
   ```

   Update `aws-config.js`:
   ```javascript
   userPoolClientSecret: process.env.REACT_APP_COGNITO_APP_CLIENT_SECRET,
   ```

3. **Security considerations**:
   - The secret will be visible in your frontend bundle
   - Anyone can extract it from the browser
   - This defeats the purpose of having a secret
   - Only use for development/testing
   - **NEVER commit actual secrets to version control**

**Why is this a security issue?**

- Client secrets are meant for backend/server applications
- Frontend code runs in the browser and can be inspected
- Anyone can extract the secret from your JavaScript bundle
- The secret provides no actual security in a public client
- It's a false sense of security

### Error: "User does not exist"

**Cause**: The user hasn't been created in the Cognito User Pool yet.

**Solution**:
1. Go to AWS Console > Cognito > User Pools > [Your Pool] > Users
2. Click "Create user"
3. Enter username and temporary password
4. The user will need to change their password on first login

### Error: "Incorrect username or password"

**Possible Causes**:
- Wrong credentials
- User hasn't changed temporary password yet
- User account is not confirmed

**Solutions**:
1. Verify the username/email is correct
2. Check if it's a new user with temporary password - they may need to reset it
3. Check user status in AWS Console - ensure it's "CONFIRMED"

### Error: "Network error" or "Unable to resolve host"

**Possible Causes**:
- Incorrect AWS region
- Invalid User Pool ID
- No internet connectivity
- CORS issues

**Solutions**:
1. Verify AWS region matches your User Pool region
2. Double-check User Pool ID in `aws-config.js`
3. Check internet connectivity
4. Check browser console for specific error details

### Sign in works but immediately redirects to login

**Cause**: Authentication state not being properly maintained.

**Solutions**:
1. Check that Amplify is configured in `index.js`
2. Verify `ProtectedRoute` component is working correctly
3. Check browser console for errors
4. Clear browser cache and cookies
5. Try in incognito mode to rule out cache issues

## Configuration Issues

### Environment variables not loading

**Symptom**: Configuration values showing as `undefined` or using placeholder values.

**Solution**:
1. Ensure you have a `.env.local` file (not `.env.example`)
2. Restart the development server after creating/modifying `.env.local`
3. Verify variable names start with `REACT_APP_`
4. Check for typos in variable names

### "Invalid configuration" errors

**Cause**: Missing or incorrect required configuration values.

**Solution**:
1. Review `aws-config.js` and ensure all required fields are filled:
   - `region`
   - `userPoolId`
   - `userPoolClientId`
2. Make sure values don't contain placeholder text like `YOUR_*`
3. Verify format matches AWS standards (e.g., region: `us-east-1`, User Pool ID: `us-east-1_abcd1234`)

## Build and Development Issues

### "Module not found: Can't resolve 'aws-amplify'"

**Cause**: AWS Amplify dependencies not installed.

**Solution**:
```bash
cd frontend
npm install
```

### Port 3000 already in use

**Solution**:
```bash
# Find and kill the process using port 3000
lsof -ti:3000 | xargs kill -9

# Or use a different port
PORT=3001 npm start
```

## Best Practices

### Secure Configuration Management

1. **Never commit secrets to version control**
   - Use `.env.local` for sensitive values
   - Add `.env.local` to `.gitignore`
   - Use `.env.example` as a template only

2. **Use environment variables**
   - Store all configuration in environment variables
   - Document required variables in `.env.example`
   - Different values for dev/staging/prod

3. **Regular security audits**
   - Review AWS Console security settings
   - Enable MFA for production
   - Use AWS CloudWatch for monitoring
   - Regular dependency updates

### Development Workflow

1. **Keep dependencies updated**
   ```bash
   npm outdated
   npm update
   ```

2. **Use proper git workflow**
   - Create feature branches
   - Review changes before committing
   - Test locally before pushing

3. **Monitor console for errors**
   - Open browser DevTools
   - Check Console and Network tabs
   - Look for authentication errors

## Getting Help

If you're still experiencing issues:

1. **Check browser console**
   - Open DevTools (F12)
   - Look for error messages
   - Check Network tab for failed requests

2. **Check AWS CloudWatch Logs**
   - Go to AWS Console > CloudWatch
   - Look for Cognito-related log groups
   - Review error messages

3. **Verify AWS Configuration**
   - User Pool exists and is active
   - App Client is properly configured
   - Callback URLs match your application URL
   - Authentication flows are enabled

4. **Common misconfigurations**
   - Client ID/Secret mismatch
   - Wrong region
   - Callback URL mismatch
   - Missing authentication flows

## Additional Resources

- [AWS Amplify Documentation](https://docs.amplify.aws/)
- [AWS Cognito Documentation](https://docs.aws.amazon.com/cognito/)
- [COGNITO_SETUP.md](./COGNITO_SETUP.md) - Initial setup guide
- [Security Documentation](../security/cognito/README.md)
