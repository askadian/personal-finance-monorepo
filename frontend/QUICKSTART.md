# Quick Start Guide - AWS Cognito Integration

Get up and running with AWS Cognito authentication in 10 minutes!

## Prerequisites Checklist
- [ ] AWS Account created
- [ ] Node.js and npm installed
- [ ] Repository cloned
- [ ] Dependencies installed (`npm install` in frontend directory)

## Step 1: Create Cognito User Pool (5 minutes)

1. **Open AWS Console**: https://console.aws.amazon.com/cognito
2. **Click**: "Create user pool"
3. **Sign-in options**: Select "Email" or "Username"
4. **Password policy**: Use defaults or customize
5. **MFA**: Choose "Optional" for now
6. **Email**: Use "Send email with Cognito" for testing
7. **User pool name**: Enter `personal-finance-users`
8. **App client name**: Enter `personal-finance-app`
9. **Click**: "Create user pool"
10. **Copy these values**:
    - User Pool ID (e.g., `us-east-1_abc123`)
    - Region (e.g., `us-east-1`)

## Step 2: Configure App Client (2 minutes)

1. **In your User Pool**, go to "App integration" tab
2. **Click** your app client name
3. **Scroll to**: "Hosted UI settings" → Edit
4. **Allowed callback URLs**: Add `http://localhost:3000/`
5. **Allowed sign-out URLs**: Add `http://localhost:3000/`
6. **OAuth 2.0 grant types**: Check "Authorization code grant"
7. **OAuth scopes**: Check "email", "openid", "profile"
8. **Save changes**
9. **Copy**: App client ID (e.g., `1a2b3c4d5e6f7g8h9i0j1k2l3m`)

## Step 3: Create Test User (1 minute)

1. **In your User Pool**, go to "Users" tab
2. **Click**: "Create user"
3. **Username**: `testuser`
4. **Email**: Your email address
5. **Temporary password**: Create a password (min 8 chars)
6. **Uncheck**: "Send an email invitation"
7. **Click**: "Create user"

## Step 4: Update Configuration (2 minutes)

1. **Open**: `frontend/src/aws-config.js`
2. **Find and replace**:
   ```javascript
   region: 'YOUR_AWS_REGION',           // Replace with: us-east-1
   userPoolId: 'YOUR_USER_POOL_ID',     // Replace with: us-east-1_abc123
   userPoolClientId: 'YOUR_APP_CLIENT_ID', // Replace with: 1a2b3c...
   ```
3. **Save** the file

### Example Configuration
```javascript
const awsConfig = {
  Auth: {
    Cognito: {
      region: 'us-east-1',
      userPoolId: 'us-east-1_abc123XYZ',
      userPoolClientId: '1a2b3c4d5e6f7g8h9i0j1k2l3m',
      // ... rest stays the same
    }
  }
};
```

## Step 5: Test the Application (1 minute)

1. **Start the app**:
   ```bash
   cd frontend
   npm start
   ```

2. **Open**: http://localhost:3000

3. **Sign in** with:
   - Username: `testuser`
   - Password: Your temporary password

4. **First login**: You may be prompted to change password

5. **Success**: You should see the Dashboard!

6. **Test logout**: Click the "Logout" button

## Troubleshooting

### "User does not exist"
- Double-check User Pool ID in aws-config.js
- Verify user was created in Cognito

### "Incorrect username or password"
- Check username is correct
- Verify password (case-sensitive)
- Check user is "Confirmed" in Cognito

### "Network error"
- Verify AWS region is correct
- Check internet connection
- Ensure User Pool exists

### App won't start
- Run `npm install` in frontend directory
- Delete `node_modules` and reinstall
- Check for port 3000 conflicts

## Next Steps

Once authentication works:
- [ ] Change temporary password
- [ ] Test logout functionality
- [ ] Create additional test users
- [ ] Configure production settings
- [ ] Set up API integration
- [ ] Enable MFA (recommended)

## Full Documentation

For complete details, see:
- [COGNITO_SETUP.md](./COGNITO_SETUP.md) - Complete setup guide
- [COGNITO_CONFIG_REFERENCE.md](./COGNITO_CONFIG_REFERENCE.md) - Configuration reference
- [ENV_VARIABLES_GUIDE.md](./ENV_VARIABLES_GUIDE.md) - Environment variables
- [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md) - Implementation details

## Need Help?

Common issues and solutions:
1. Check browser console for errors
2. Review CloudWatch logs in AWS Console
3. Verify all configuration values
4. Ensure Cognito User Pool is in same region
5. Check AWS service health status

## Success Criteria

You've successfully set up Cognito when:
- ✅ User can sign in with credentials
- ✅ User is redirected to Dashboard
- ✅ Dashboard shows user is authenticated
- ✅ Logout works and redirects to sign-in
- ✅ Accessing /dashboard without login redirects to sign-in

Congratulations! Your authentication is now powered by AWS Cognito! 🎉
