/**
 * AWS Cognito Configuration
 * 
 * This file contains AWS Cognito User Pool configuration for authentication.
 * Replace the placeholder values with your actual AWS Cognito User Pool details.
 * 
 * Setup Instructions:
 * 1. Create an AWS Cognito User Pool in your AWS Console
 * 2. Create an App Client for the User Pool
 * 3. Configure the Hosted UI with callback URLs
 * 4. Update the values below with your User Pool details
 * 
 * For detailed setup instructions, see: /security/cognito/README.md
 */

const awsConfig = {
  Auth: {
    Cognito: {
      // REQUIRED - Amazon Cognito Region
      // Example: 'us-east-1', 'us-west-2', 'eu-west-1'
      region: 'YOUR_AWS_REGION',

      // REQUIRED - Amazon Cognito User Pool ID
      // Example: 'us-east-1_abcd1234'
      // Found in: AWS Console > Cognito > User Pools > [Your Pool] > General Settings > Pool Id
      userPoolId: 'YOUR_USER_POOL_ID',

      // REQUIRED - Amazon Cognito App Client ID
      // Example: '1a2b3c4d5e6f7g8h9i0j1k2l3m'
      // Found in: AWS Console > Cognito > User Pools > [Your Pool] > App clients > Client ID
      userPoolClientId: 'YOUR_APP_CLIENT_ID',

      // OPTIONAL - Enforce user authentication prior to accessing AWS resources
      // Default: false
      mandatorySignIn: false,

      // OPTIONAL - Configuration for cookie storage
      // Note: Required if using OAuth flow with a custom domain
      cookieStorage: {
        // REQUIRED - Cookie domain (only required if using a custom domain)
        // Example: '.example.com' (with leading dot for subdomains)
        domain: 'localhost',
        
        // OPTIONAL - Cookie path
        path: '/',
        
        // OPTIONAL - Cookie expiration in days
        expires: 7,
        
        // OPTIONAL - Cookie secure flag
        // When on HTTPS, set to true
        secure: false
      },

      // OPTIONAL - Hosted UI configuration
      loginWith: {
        oauth: {
          // REQUIRED - Hosted UI domain
          // Example: 'your-domain.auth.us-east-1.amazoncognito.com'
          // Found in: AWS Console > Cognito > User Pools > [Your Pool] > App integration > Domain
          domain: 'YOUR_COGNITO_DOMAIN.auth.YOUR_AWS_REGION.amazoncognito.com',

          // REQUIRED - OAuth scopes
          // Common scopes: 'phone', 'email', 'profile', 'openid', 'aws.cognito.signin.user.admin'
          scopes: ['openid', 'email', 'profile'],

          // REQUIRED - Redirect sign in URI(s)
          // These must match what you configured in the Cognito App Client
          // For local development: 'http://localhost:3000/'
          // For production: 'https://yourdomain.com/'
          redirectSignIn: ['http://localhost:3000/'],

          // REQUIRED - Redirect sign out URI(s)
          // These must match what you configured in the Cognito App Client
          redirectSignOut: ['http://localhost:3000/'],

          // REQUIRED - OAuth response type
          // Options: 'code' (recommended for security), 'token'
          responseType: 'code'
        }
      }
    }
  }
};

export default awsConfig;
