# Using Environment Variables for AWS Cognito Configuration (Optional)

This guide explains how to use environment variables instead of directly modifying `aws-config.js`. This approach is recommended for teams or when you need to manage multiple environments.

## Why Use Environment Variables?

- **Security**: Prevents accidentally committing sensitive credentials
- **Flexibility**: Easy to switch between development, staging, and production
- **Team Collaboration**: Each developer can have their own configuration
- **CI/CD**: Easier to configure different environments in deployment pipelines

## Setup Instructions

### Step 1: Create Environment File

1. Copy the example environment file:
   ```bash
   cp .env.example .env.local
   ```

2. Open `.env.local` and add your actual AWS Cognito values:
   ```bash
   REACT_APP_AWS_REGION=us-east-1
   REACT_APP_COGNITO_USER_POOL_ID=us-east-1_YourPoolId
   REACT_APP_COGNITO_APP_CLIENT_ID=YourAppClientId
   REACT_APP_COGNITO_DOMAIN=your-app-name.auth.us-east-1.amazoncognito.com
   ```

### Step 2: Update aws-config.js to Use Environment Variables

Replace the hardcoded values in `src/aws-config.js` with environment variables:

```javascript
const awsConfig = {
  Auth: {
    Cognito: {
      region: process.env.REACT_APP_AWS_REGION || 'YOUR_AWS_REGION',
      userPoolId: process.env.REACT_APP_COGNITO_USER_POOL_ID || 'YOUR_USER_POOL_ID',
      userPoolClientId: process.env.REACT_APP_COGNITO_APP_CLIENT_ID || 'YOUR_APP_CLIENT_ID',
      mandatorySignIn: false,
      cookieStorage: {
        domain: process.env.REACT_APP_COOKIE_DOMAIN || 'localhost',
        path: '/',
        expires: 7,
        secure: process.env.REACT_APP_COOKIE_SECURE === 'true'
      },
      loginWith: {
        oauth: {
          domain: process.env.REACT_APP_COGNITO_DOMAIN || 
                  'YOUR_COGNITO_DOMAIN.auth.YOUR_AWS_REGION.amazoncognito.com',
          scopes: ['openid', 'email', 'profile'],
          redirectSignIn: [process.env.REACT_APP_OAUTH_REDIRECT_SIGN_IN || 'http://localhost:3000/'],
          redirectSignOut: [process.env.REACT_APP_OAUTH_REDIRECT_SIGN_OUT || 'http://localhost:3000/'],
          responseType: 'code'
        }
      }
    }
  }
};

export default awsConfig;
```

### Step 3: Restart the Application

After creating or modifying `.env.local`, restart your development server:
```bash
npm start
```

## Environment Files

### Available Environment Files

Create-React-App supports multiple environment files:

| File | Purpose | Committed? |
|------|---------|------------|
| `.env` | Default values for all environments | ✅ Yes (with placeholders only) |
| `.env.local` | Local overrides (not committed) | ❌ No |
| `.env.development` | Development-specific values | ✅ Yes (with placeholders) |
| `.env.development.local` | Local development overrides | ❌ No |
| `.env.production` | Production-specific values | ✅ Yes (without secrets) |
| `.env.production.local` | Local production overrides | ❌ No |

### Priority Order

Environment files are loaded in this order (higher priority = loaded later):
1. `.env`
2. `.env.local`
3. `.env.[mode]` (`.env.development` or `.env.production`)
4. `.env.[mode].local`

## Multiple Environments

### Development Environment

Create `.env.development.local`:
```bash
REACT_APP_AWS_REGION=us-east-1
REACT_APP_COGNITO_USER_POOL_ID=us-east-1_DevPoolId
REACT_APP_COGNITO_APP_CLIENT_ID=DevAppClientId
REACT_APP_COOKIE_DOMAIN=localhost
REACT_APP_COOKIE_SECURE=false
REACT_APP_OAUTH_REDIRECT_SIGN_IN=http://localhost:3000/
REACT_APP_OAUTH_REDIRECT_SIGN_OUT=http://localhost:3000/
```

### Production Environment

Create `.env.production.local` (for local production builds):
```bash
REACT_APP_AWS_REGION=us-west-2
REACT_APP_COGNITO_USER_POOL_ID=us-west-2_ProdPoolId
REACT_APP_COGNITO_APP_CLIENT_ID=ProdAppClientId
REACT_APP_COOKIE_DOMAIN=.yourdomain.com
REACT_APP_COOKIE_SECURE=true
REACT_APP_OAUTH_REDIRECT_SIGN_IN=https://yourdomain.com/
REACT_APP_OAUTH_REDIRECT_SIGN_OUT=https://yourdomain.com/
```

## CI/CD Integration

### GitHub Actions Example

```yaml
- name: Build React App
  env:
    REACT_APP_AWS_REGION: ${{ secrets.AWS_REGION }}
    REACT_APP_COGNITO_USER_POOL_ID: ${{ secrets.COGNITO_USER_POOL_ID }}
    REACT_APP_COGNITO_APP_CLIENT_ID: ${{ secrets.COGNITO_APP_CLIENT_ID }}
    REACT_APP_COGNITO_DOMAIN: ${{ secrets.COGNITO_DOMAIN }}
  run: npm run build
```

### AWS Amplify Console

In Amplify Console, add environment variables:
1. Go to App Settings → Environment variables
2. Add each variable (e.g., `REACT_APP_AWS_REGION`)
3. Deploy

## Security Best Practices

### Do's ✅
- Use `.env.local` for sensitive values
- Add `.env.local` to `.gitignore` (already done)
- Use environment variables in CI/CD pipelines
- Document required environment variables
- Provide `.env.example` with placeholder values

### Don'ts ❌
- Never commit `.env.local` files
- Don't hardcode credentials in source code
- Don't commit User Pool IDs or App Client IDs
- Don't share `.env.local` files via insecure channels
- Don't use same credentials for dev and production

## Verification

To verify your environment variables are loaded:

1. Add this temporarily to your component:
   ```javascript
   console.log('AWS Region:', process.env.REACT_APP_AWS_REGION);
   console.log('User Pool ID:', process.env.REACT_APP_COGNITO_USER_POOL_ID);
   ```

2. Check the browser console
3. Remove the console logs after verification

## Troubleshooting

### Environment Variables Not Loading

**Problem**: Environment variables show as `undefined`

**Solutions**:
- Ensure variable names start with `REACT_APP_`
- Restart the development server after changes
- Check for typos in variable names
- Verify `.env.local` is in the `frontend/` directory

### Wrong Values Being Used

**Problem**: Application uses wrong configuration

**Solutions**:
- Check the environment file priority order
- Clear browser cache and local storage
- Verify you're running the correct environment (dev vs prod)
- Check for conflicting environment files

### Build Errors

**Problem**: Build fails with undefined values

**Solutions**:
- Ensure all required variables are set
- Check that variables are available during build
- Verify fallback values in `aws-config.js`

## Current Approach vs Environment Variables

The current implementation uses **hardcoded values with placeholders** in `aws-config.js`. This approach:

### Pros
- Simple and straightforward
- Easy for single developers
- No additional configuration needed
- Clear what values need to be replaced

### Cons
- Risk of committing credentials
- Harder to manage multiple environments
- Manual changes needed for different configs
- Not ideal for teams

### Environment Variables Approach

To switch to environment variables:
1. Follow the setup instructions above
2. Update `aws-config.js` to read from environment variables
3. Create `.env.local` with your values
4. Restart the application

Both approaches work - choose based on your needs!

## Additional Resources

- [Create React App: Environment Variables](https://create-react-app.dev/docs/adding-custom-environment-variables/)
- [AWS Best Practices for Managing Credentials](https://docs.aws.amazon.com/general/latest/gr/aws-access-keys-best-practices.html)
- [Environment Variable Security](https://12factor.net/config)
