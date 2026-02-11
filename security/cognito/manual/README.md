# Manual Amazon Cognito User Pool Setup Guide

This guide provides step-by-step instructions for manually setting up AWS Cognito User Pool for the Personal Finance application using the AWS Web Console.

## 📖 Overview

This manual setup guide will walk you through creating a Cognito User Pool with proper authentication, user management, and integration with your API Gateway and frontend application.

**Estimated Time**: 45-60 minutes

## 📚 Guide Structure

Follow these guides in order:

### 1. [Prerequisites](./01-prerequisites.md)
- AWS account setup
- Required permissions
- Understanding Cognito concepts
- Planning your user pool configuration

### 2. [User Pool Setup](./02-user-pool-setup.md)
- Creating a new User Pool
- Configuring sign-in options
- Setting pool name and basic settings
- Understanding User Pool settings

### 3. [App Client Setup](./03-app-client-setup.md)
- Creating app client for frontend
- Configuring OAuth 2.0 settings
- Setting callback URLs
- Generating client credentials

### 4. [Hosted UI Setup](./04-hosted-ui-setup.md)
- Configuring Hosted UI domain
- Customizing login/signup pages
- Setting up OAuth flows
- Branding and localization

### 5. [User Attributes](./05-user-attributes.md)
- Configuring required attributes
- Setting up custom attributes
- Understanding attribute permissions
- Attribute verification settings

### 6. [Password Policies](./06-password-policies.md)
- Setting password requirements
- Configuring password expiration
- Account recovery settings
- Temporary password policies

### 7. [MFA Setup](./07-mfa-setup.md) *(Optional but Recommended)*
- Enabling multi-factor authentication
- Configuring TOTP (Time-based OTP)
- SMS configuration
- MFA enforcement policies

### 8. [Email and SMS Configuration](./08-email-sms-config.md)
- Configuring email delivery
- Setting up Amazon SES (production)
- Configuring SMS delivery (for MFA)
- Customizing email templates

### 9. [Lambda Triggers](./09-triggers-lambda.md) *(Optional)*
- Pre-signup validation
- Post-confirmation actions
- Pre-authentication logic
- Custom message triggers

### 10. [Testing and Validation](./10-testing-validation.md)
- Creating test users
- Testing sign-up flow
- Testing sign-in flow
- Validating JWT tokens
- Integration testing with API Gateway

## 🎯 What You'll Build

By the end of this guide, you'll have:

- ✅ A fully configured Cognito User Pool
- ✅ Hosted UI for login and registration
- ✅ Secure authentication with JWT tokens
- ✅ Password policies and security settings
- ✅ Email verification for new users
- ✅ Multi-factor authentication (optional)
- ✅ Integration with API Gateway
- ✅ Tested and validated authentication flow

## 📋 User Pool Configuration Overview

The User Pool will support:

```
User Pool: personal-finance-user-pool
├── Sign-in options: Email
├── Password policy: Strong (8+ chars, mixed case, numbers, symbols)
├── MFA: Optional (TOTP recommended)
├── Email verification: Required
├── User attributes:
│   ├── email (required)
│   ├── name (optional)
│   └── custom attributes (as needed)
├── App client: personal-finance-app-client
│   ├── OAuth 2.0 flows: Authorization code grant
│   ├── Callback URLs: Frontend URLs
│   └── Token expiration: 1 hour (access), 30 days (refresh)
└── Hosted UI: auth.yourdomain.com (or Cognito domain)
    ├── Branding: Custom logo and CSS
    └── Flows: Sign up, Sign in, Password reset
```

## 🏗️ Authentication Flow

Understanding the authentication flow:

```
1. User Access
   ↓
   Frontend App
   ↓
2. Redirect to Hosted UI
   ↓
   Cognito Hosted UI (Login/Signup)
   ↓
3. User enters credentials
   ↓
   Cognito validates credentials
   ↓
4. Cognito issues tokens
   ↓
   - ID Token (user identity)
   - Access Token (API authorization)
   - Refresh Token (token renewal)
   ↓
5. Redirect back to frontend
   ↓
   Frontend stores tokens securely
   ↓
6. API requests include Access Token
   ↓
   API Gateway validates token
   ↓
7. Lambda receives validated user context
   ↓
   Process request with user info
```

## 🔑 Key Concepts

Before starting, understand these Cognito concepts:

### User Pools vs Identity Pools
- **User Pool**: User directory and authentication service (we'll use this)
- **Identity Pool**: AWS credentials for authenticated users (not needed for this project)

### Tokens
- **ID Token**: Contains user claims (username, email, custom attributes)
- **Access Token**: Used for API authorization and resource access
- **Refresh Token**: Long-lived token to obtain new access/ID tokens

### App Client
- Configuration for your application to interact with User Pool
- Contains OAuth settings, callback URLs, token expiration
- Can be public (frontend) or confidential (backend)

### Hosted UI
- Pre-built, customizable login/signup pages hosted by AWS
- Handles OAuth 2.0 flows automatically
- Can be customized with logo, CSS, and domain

### Sign-in Options
- **Username**: Traditional username-based sign-in
- **Email**: Email-based sign-in (recommended for this project)
- **Phone**: Phone number-based sign-in
- **Preferred username**: Alias for username

## ⚠️ Important Notes

### Before You Begin
1. **Plan your sign-in method** - Email is recommended for personal finance apps
2. **Decide on required attributes** - These cannot be changed after pool creation
3. **Plan custom attributes** - These are immutable after creation
4. **Choose MFA strategy** - Optional vs required, TOTP vs SMS
5. **Prepare email service** - Use SES for production, Cognito default for testing

### Best Practices
- ✅ Use email as sign-in option (users prefer email over username)
- ✅ Require email verification to prevent fake accounts
- ✅ Enable optional MFA (users can enable for enhanced security)
- ✅ Set strong password policies (8+ characters, complexity)
- ✅ Use short-lived access tokens (1 hour)
- ✅ Use longer refresh tokens (30 days)
- ✅ Enable CloudWatch logging for monitoring

### Common Pitfalls to Avoid
- ❌ Don't make attributes required unless absolutely necessary
- ❌ Don't set password policies too strict (causes user frustration)
- ❌ Don't forget to verify email configuration (test email delivery)
- ❌ Don't use default Cognito domain in production (use custom domain)
- ❌ Don't forget to whitelist callback URLs (causes OAuth errors)
- ❌ Don't expose app client secret in frontend code

## 🔒 Security Considerations

### Token Storage (Frontend)
- Store tokens securely (HttpOnly cookies or secure storage)
- Never store tokens in localStorage (XSS vulnerability)
- Implement token refresh logic
- Clear tokens on logout

### App Client Configuration
- Use public client type for frontend (no client secret)
- Use confidential client for backend services
- Restrict callback URLs to your domains only
- Enable token revocation

### API Gateway Integration
- Always validate JWT tokens
- Use Cognito authorizer (don't validate tokens manually)
- Check token expiration
- Verify token audience (client ID)

## 🚀 Getting Started

Ready to begin? Start with [Prerequisites](./01-prerequisites.md) to ensure you have everything needed.

## 📊 Cost Considerations

AWS Cognito pricing (as of 2024):
- **Free Tier**: 50,000 MAU (Monthly Active Users)
- **After Free Tier**: $0.0055 per MAU
- **Advanced Security**: Additional $0.05 per MAU (optional)
- **SMS MFA**: Standard SMS pricing (varies by region)

For a personal finance app:
- Development: Free (within free tier)
- Production (1,000 users): ~$5.50/month
- Production (10,000 users): ~$55/month

## 📞 Need Help?

If you encounter issues:
1. Check the troubleshooting section in each guide
2. Review CloudWatch logs for error messages
3. Verify all prerequisites are met
4. Consult AWS Cognito documentation
5. Open an issue in the repository

## 🔄 Alternative: Automated Setup

If you prefer automated setup using Infrastructure as Code:
- See [../automation/README.md](../automation/README.md) for CloudFormation/Terraform options

## 📚 Additional Resources

- [AWS Cognito User Pools Documentation](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-identity-pools.html)
- [AWS Amplify with Cognito](https://docs.amplify.aws/lib/auth/getting-started/q/platform/js/)
- [OAuth 2.0 and OpenID Connect](https://oauth.net/2/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)

---

**Next Step**: Continue to [Prerequisites](./01-prerequisites.md) →
