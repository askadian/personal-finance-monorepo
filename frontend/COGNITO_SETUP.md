# AWS Cognito Integration Setup Guide

This guide provides step-by-step instructions for integrating AWS Cognito authentication with the Personal Finance Tracker frontend application.

## Overview

The frontend application now uses AWS Amplify and Amazon Cognito for user authentication. This integration provides:
- Secure user sign-in and sign-out
- JWT token-based authentication
- Protected routes that require authentication
- Session management

## Prerequisites

Before you begin, ensure you have:
- An AWS account
- AWS Cognito User Pool created (see [Security Documentation](../security/cognito/README.md))
- App Client configured in the User Pool
- Node.js and npm installed

## Setup Instructions

### Step 1: Create AWS Cognito User Pool

If you haven't already created a Cognito User Pool, follow these steps:

1. **Log in to AWS Console**
   - Go to https://console.aws.amazon.com/
   - Navigate to Amazon Cognito service

2. **Create User Pool**
   - Click "Create user pool"
   - Choose sign-in options (email or username)
   - Configure password policies
   - Enable email verification
   - Complete the wizard

3. **Note the User Pool ID**
   - After creation, copy the User Pool ID (e.g., `us-east-1_abcd1234`)
   - You can find this in the "User pool overview" section

### Step 2: Create App Client

1. **In your User Pool, go to "App integration"**
   - Click "App client list"
   - Click "Create app client"

2. **Configure App Client**
   - App client name: `personal-finance-app`
   - Authentication flows: Enable `ALLOW_USER_PASSWORD_AUTH`
   - OAuth 2.0 grant types: Select `Authorization code grant`
   - OAuth scopes: Select `email`, `openid`, `profile`

3. **Configure Callback URLs**
   - For local development: `http://localhost:3000/`
   - For production: `https://your-domain.com/`
   - Sign-out URLs: Same as callback URLs

4. **Note the App Client ID**
   - Copy the App client ID (e.g., `1a2b3c4d5e6f7g8h9i0j1k2l3m`)

### Step 3: Configure Hosted UI Domain (Optional)

1. **In "App integration", go to "Domain"**
   - Click "Create Cognito domain" or "Create custom domain"
   - For testing, use a Cognito domain: `your-app-name.auth.us-east-1.amazoncognito.com`
   - Note the domain for later use

### Step 4: Create Test User

1. **Go to "Users" in your User Pool**
   - Click "Create user"
   - Enter username and temporary password
   - Uncheck "Send an email invitation" for testing
   - User will need to change password on first login

### Step 5: Update Frontend Configuration

1. **Open the configuration file**
   ```bash
   cd frontend/src
   nano aws-config.js  # or use your preferred editor
   ```

2. **Update the following values:**

   ```javascript
   const awsConfig = {
     Auth: {
       Cognito: {
         // Replace with your AWS region
         region: 'us-east-1',  // Example: 'us-west-2', 'eu-west-1'

         // Replace with your User Pool ID
         userPoolId: 'us-east-1_abcd1234',

         // Replace with your App Client ID
         userPoolClientId: '1a2b3c4d5e6f7g8h9i0j1k2l3m',

         // Keep these as-is for basic integration
         mandatorySignIn: false,
         
         cookieStorage: {
           domain: 'localhost',
           path: '/',
           expires: 7,
           secure: false  // Set to true in production with HTTPS
         },

         // Optional: If using Hosted UI
         loginWith: {
           oauth: {
             // Replace with your Cognito domain
             domain: 'your-app-name.auth.us-east-1.amazoncognito.com',
             scopes: ['openid', 'email', 'profile'],
             redirectSignIn: ['http://localhost:3000/'],
             redirectSignOut: ['http://localhost:3000/'],
             responseType: 'code'
           }
         }
       }
     }
   };
   ```

3. **Configuration Values Guide:**

   | Field | Where to Find | Example |
   |-------|--------------|---------|
   | `region` | AWS Console > Top right corner | `us-east-1` |
   | `userPoolId` | Cognito > User Pools > [Your Pool] > General settings | `us-east-1_abcd1234` |
   | `userPoolClientId` | Cognito > User Pools > [Your Pool] > App integration > App clients | `1a2b3c4d5e6f7g8h9i0j1k2l3m` |
   | `domain` | Cognito > User Pools > [Your Pool] > App integration > Domain | `your-app.auth.us-east-1.amazoncognito.com` |

### Step 6: Install Dependencies

The AWS Amplify libraries should already be installed, but if you need to reinstall:

```bash
cd frontend
npm install aws-amplify @aws-amplify/ui-react
```

### Step 7: Run the Application

1. **Start the development server:**
   ```bash
   npm start
   ```

2. **Open your browser:**
   - Navigate to http://localhost:3000

3. **Test the authentication:**
   - Enter your test user credentials
   - Click "Sign In"
   - You should be redirected to the Dashboard
   - Click "Logout" to sign out

## Testing the Integration

### Test Sign In

1. Open the application at http://localhost:3000
2. Enter your Cognito user credentials
3. Click "Sign In"
4. Verify you're redirected to the Dashboard

### Test Protected Routes

1. Try accessing http://localhost:3000/dashboard directly without signing in
2. You should be redirected to the sign-in page

### Test Logout

1. After signing in, click the "Logout" button
2. You should be redirected to the sign-in page
3. Try accessing the dashboard again - you should be redirected to sign-in

## Troubleshooting

### Error: "User does not exist"
- Verify the username/email is correct
- Check that the user exists in your Cognito User Pool
- Ensure the User Pool ID is correct in aws-config.js

### Error: "Incorrect username or password"
- Verify the password is correct
- If using a temporary password, you may need to reset it
- Check that the user is confirmed in Cognito

### Error: "Network error" or "Unable to resolve host"
- Verify your AWS region is correct
- Check that your User Pool ID is correct
- Ensure you have internet connectivity

### Sign in works but redirects immediately
- Check the ProtectedRoute component is working correctly
- Verify Amplify is configured in index.js
- Check browser console for errors

### "UserNotFoundException" in console
- The configured User Pool doesn't exist or ID is incorrect
- Verify the User Pool ID in aws-config.js
- Check that you're using the correct AWS region

### CORS errors
- If you see CORS errors, it's likely an issue with API Gateway configuration
- For now, the app only uses Cognito for authentication, so CORS shouldn't be an issue
- CORS will need to be configured when integrating with API Gateway

## Production Deployment

When deploying to production, update the following:

1. **Update aws-config.js:**
   - Change `cookieStorage.domain` to your production domain
   - Set `cookieStorage.secure` to `true`
   - Update OAuth redirect URLs to production URLs

2. **Environment Variables (Recommended):**
   - Consider using environment variables for sensitive configuration
   - Create `.env` file with configuration values
   - Update aws-config.js to read from environment variables

3. **Security Considerations:**
   - Always use HTTPS in production
   - Enable MFA for additional security
   - Configure password policies
   - Set up CloudWatch logging for monitoring

## Next Steps

- Configure password reset functionality
- Implement MFA (Multi-Factor Authentication)
- Add user registration flow
- Integrate with API Gateway for backend calls
- Add token refresh logic
- Implement remember me functionality

## Additional Resources

- [AWS Amplify Authentication Documentation](https://docs.amplify.aws/lib/auth/getting-started/q/platform/js/)
- [Amazon Cognito User Pools](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html)
- [Security Documentation](../security/cognito/README.md)
- [AWS Amplify UI Components](https://ui.docs.amplify.aws/)

## Support

If you encounter issues:
1. Check the browser console for detailed error messages
2. Review CloudWatch logs in AWS Console
3. Verify all configuration values in aws-config.js
4. Ensure your Cognito User Pool and App Client are configured correctly
5. Open an issue in the repository if problems persist
