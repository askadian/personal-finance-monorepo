# AWS Cognito Configuration Quick Reference

This is a quick reference for updating the AWS Cognito configuration in `src/aws-config.js`.

## Configuration File Location
```
frontend/src/aws-config.js
```

## Required Configuration Values

### 1. AWS Region
**Field:** `region`  
**Location:** AWS Console → Top right corner  
**Example:** `us-east-1`, `us-west-2`, `eu-west-1`  
**Replace:** `YOUR_AWS_REGION`

### 2. User Pool ID
**Field:** `userPoolId`  
**Location:** AWS Console → Cognito → User Pools → [Your Pool] → General settings → Pool Id  
**Format:** `{region}_{alphanumeric}`  
**Example:** `us-east-1_abcd1234`  
**Replace:** `YOUR_USER_POOL_ID`

### 3. App Client ID
**Field:** `userPoolClientId`  
**Location:** AWS Console → Cognito → User Pools → [Your Pool] → App integration → App clients → Client ID  
**Format:** Alphanumeric string  
**Example:** `1a2b3c4d5e6f7g8h9i0j1k2l3m`  
**Replace:** `YOUR_APP_CLIENT_ID`

### 4. Cognito Domain (Optional - for Hosted UI)
**Field:** `loginWith.oauth.domain`  
**Location:** AWS Console → Cognito → User Pools → [Your Pool] → App integration → Domain  
**Format:** `{your-domain}.auth.{region}.amazoncognito.com`  
**Example:** `personal-finance.auth.us-east-1.amazoncognito.com`  
**Replace:** `YOUR_COGNITO_DOMAIN.auth.YOUR_AWS_REGION.amazoncognito.com`

## Environment-Specific Values

### Local Development
```javascript
cookieStorage: {
  domain: 'localhost',
  secure: false
},
loginWith: {
  oauth: {
    redirectSignIn: ['http://localhost:3000/'],
    redirectSignOut: ['http://localhost:3000/']
  }
}
```

### Production
```javascript
cookieStorage: {
  domain: '.yourdomain.com',  // Note: include leading dot for subdomains
  secure: true  // MUST be true for HTTPS
},
loginWith: {
  oauth: {
    redirectSignIn: ['https://yourdomain.com/'],
    redirectSignOut: ['https://yourdomain.com/']
  }
}
```

## Step-by-Step Update Process

1. Open `frontend/src/aws-config.js` in your editor
2. Find the placeholder values (marked with `YOUR_`)
3. Replace each placeholder with your actual values
4. Save the file
5. Restart the development server if running

## Verification Checklist

- [ ] Updated `region` with your AWS region
- [ ] Updated `userPoolId` with your User Pool ID
- [ ] Updated `userPoolClientId` with your App Client ID
- [ ] Updated `domain` with your Cognito domain (if using Hosted UI)
- [ ] Updated redirect URLs for your environment (localhost or production)
- [ ] Set `secure: true` if using HTTPS in production
- [ ] Saved the file
- [ ] Restarted the application

## Common Issues

### Issue: "User does not exist"
**Cause:** User Pool ID is incorrect  
**Solution:** Verify User Pool ID in AWS Console

### Issue: "Invalid client id"
**Cause:** App Client ID is incorrect  
**Solution:** Verify App Client ID in AWS Console

### Issue: "Redirect mismatch"
**Cause:** Redirect URLs don't match Cognito configuration  
**Solution:** Update redirect URLs in both aws-config.js and Cognito App Client settings

### Issue: Network errors
**Cause:** Incorrect region or User Pool doesn't exist  
**Solution:** Verify region and User Pool ID are correct

## Example Configuration

Here's a complete example with actual values (for reference):

```javascript
const awsConfig = {
  Auth: {
    Cognito: {
      region: 'us-east-1',
      userPoolId: 'us-east-1_Abc123XYZ',
      userPoolClientId: '1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p',
      mandatorySignIn: false,
      cookieStorage: {
        domain: 'localhost',
        path: '/',
        expires: 7,
        secure: false
      },
      loginWith: {
        oauth: {
          domain: 'personal-finance-app.auth.us-east-1.amazoncognito.com',
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

## Next Steps

After updating the configuration:
1. Create a test user in your Cognito User Pool
2. Start the application: `npm start`
3. Try signing in with your test user credentials
4. Verify successful authentication and redirect to dashboard

## Additional Resources

- [Full Setup Guide](./COGNITO_SETUP.md)
- [AWS Cognito Documentation](https://docs.aws.amazon.com/cognito/)
- [AWS Amplify Documentation](https://docs.amplify.aws/)
