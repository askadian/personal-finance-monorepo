# Amazon Cognito User Pool Setup for Personal Finance App

This directory contains instructions and automation scripts for setting up AWS Cognito User Pools to provide authentication and authorization for the Personal Finance application.

## 📁 Directory Structure

```
security/cognito/
├── README.md                           # This file - Overview and quick start
├── manual/                             # Step-by-step manual setup instructions
│   ├── README.md                       # Manual setup guide
│   ├── 01-prerequisites.md             # Prerequisites and requirements
│   ├── 02-user-pool-setup.md          # Creating User Pool
│   ├── 03-app-client-setup.md         # Configuring App Client
│   ├── 04-hosted-ui-setup.md          # Setting up Hosted UI
│   ├── 05-user-attributes.md          # Configuring user attributes
│   ├── 06-password-policies.md        # Setting password policies
│   ├── 07-mfa-setup.md                # Multi-factor authentication
│   ├── 08-email-sms-config.md         # Email and SMS configuration
│   ├── 09-triggers-lambda.md          # Lambda triggers (optional)
│   └── 10-testing-validation.md       # Testing and validating the setup
└── automation/                         # Automation scripts and IaC
    ├── README.md                       # Automation guide
    ├── cloudformation/                 # CloudFormation templates (planned)
    ├── terraform/                      # Terraform scripts (planned)
    └── scripts/                        # Helper scripts (planned)
```

## 🎯 Overview

AWS Cognito User Pools provide a complete user directory and authentication service for the Personal Finance application. It enables:

- **User Registration**: Self-service sign-up with email verification
- **User Authentication**: Secure login with JWT tokens
- **Password Management**: Password reset and recovery
- **Multi-Factor Authentication (MFA)**: Enhanced security with TOTP or SMS
- **Hosted UI**: Pre-built, customizable login/signup pages
- **OAuth 2.0 / OIDC**: Standard protocol support for integration
- **User Attributes**: Custom and standard user profile fields
- **Social Sign-In**: Integration with Google, Facebook, Amazon (optional)

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend      │ (React App)
│   (CloudFront)  │
└────────┬────────┘
         │
         │ HTTPS
         │
         ▼
┌─────────────────────────────────┐
│   AWS Cognito User Pool         │
│                                  │
│  ┌───────────────────────────┐  │
│  │  Hosted UI                │  │
│  │  (Login/Signup Pages)     │  │
│  └───────────────────────────┘  │
│                                  │
│  ┌───────────────────────────┐  │
│  │  User Directory           │  │
│  │  (User accounts & attrs)  │  │
│  └───────────────────────────┘  │
│                                  │
│  ┌───────────────────────────┐  │
│  │  JWT Token Generation     │  │
│  │  (ID, Access, Refresh)    │  │
│  └───────────────────────────┘  │
└────────────┬────────────────────┘
             │
             │ JWT Token
             │
             ▼
┌─────────────────────────────────┐
│     API Gateway                  │
│  ┌───────────────────────────┐  │
│  │  Cognito Authorizer       │  │
│  │  (JWT Validation)         │  │
│  └───────────────────────────┘  │
└────────────┬────────────────────┘
             │
             ▼
      ┌─────────────┐
      │   Lambda    │
      │  Functions  │
      └─────────────┘
```

## 🔑 Key Features

### Authentication Flow
1. User navigates to the application
2. Redirected to Cognito Hosted UI for login
3. User enters credentials
4. Cognito validates and issues JWT tokens
5. Frontend stores tokens securely
6. Frontend includes JWT in API requests
7. API Gateway validates JWT with Cognito
8. Lambda processes authenticated requests

### Token Types
- **ID Token**: Contains user identity claims (username, email, etc.)
- **Access Token**: Used for API authorization
- **Refresh Token**: Used to obtain new tokens when expired

### Security Features
- Password complexity requirements
- Account lockout after failed attempts
- Email/phone verification
- Multi-factor authentication (MFA)
- Session management
- Token expiration and rotation

## 📋 Integration Points

### Frontend Integration
The React frontend integrates with Cognito through:
- **AWS Amplify**: Simplifies authentication flow
- **Hosted UI**: Pre-built login/signup pages
- **JWT Storage**: Secure token management
- **Auto Refresh**: Automatic token renewal

### API Gateway Integration
API Gateway uses Cognito for:
- **JWT Validation**: Verifies token signature and claims
- **Authorization**: Controls access to API resources
- **User Context**: Passes user information to Lambda

### Lambda Integration
Lambda functions can:
- **Access User Context**: Retrieve user info from API Gateway
- **Custom Authorization**: Implement additional business logic
- **User Management**: Programmatically manage users via AWS SDK

## 🚀 Quick Start

### For Manual Setup
Follow the comprehensive step-by-step guide in the [manual](./manual/) directory:

```bash
cd security/cognito/manual
# Start with README.md and follow the numbered guides
```

### For Automated Setup
Use the automation scripts (coming soon):

```bash
cd security/cognito/automation
# Follow instructions in automation/README.md
```

## 🔐 Security Best Practices

1. **Password Policy**
   - Minimum 8 characters
   - Require uppercase, lowercase, numbers, special characters
   - Password expiration (optional)

2. **MFA Configuration**
   - Enable optional MFA for all users
   - Require MFA for admin users
   - Use TOTP apps (Google Authenticator, Authy)

3. **Token Configuration**
   - Short-lived access tokens (1 hour)
   - Longer refresh tokens (30 days)
   - Secure token storage in frontend

4. **Email/SMS Verification**
   - Verify email addresses on signup
   - Optional phone verification
   - Use Amazon SES for production emails

5. **Monitoring**
   - Enable CloudWatch logs
   - Monitor failed login attempts
   - Set up alerts for suspicious activity

## 📝 Prerequisites

Before setting up Cognito User Pool:

- ✅ AWS Account with appropriate permissions
- ✅ Understanding of OAuth 2.0 / OIDC concepts
- ✅ Domain for custom hosted UI (optional)
- ✅ Email sending service configured (SES or Cognito default)
- ✅ Frontend application ready for integration

## 🎓 Documentation References

- **AWS Cognito Documentation**: https://docs.aws.amazon.com/cognito/
- **AWS Amplify Documentation**: https://docs.amplify.aws/
- **Frontend Integration**: [../../frontend/README.md](../../frontend/README.md)
- **API Gateway Integration**: [../../api/apigateway/README.md](../../api/apigateway/README.md)

## 🔄 Configuration Options

### User Attributes
Standard attributes available:
- email (required)
- name
- phone_number
- birthdate
- address
- custom attributes (e.g., custom:membershipLevel)

### Authentication Methods
- Username and password
- Email and password
- Phone and password
- Social identity providers (Google, Facebook, Amazon)

### Hosted UI Customization
- Custom logo
- Custom CSS
- Custom domain
- Localization support

## 🧪 Testing

After setup, test your Cognito User Pool:

1. **Sign Up Flow**: Create a test user account
2. **Email Verification**: Verify email confirmation works
3. **Sign In Flow**: Test successful and failed logins
4. **Password Reset**: Test forgot password flow
5. **Token Generation**: Verify JWT tokens are issued
6. **API Integration**: Test API calls with tokens
7. **MFA**: Test multi-factor authentication (if enabled)

## 🆘 Troubleshooting

Common issues and solutions:

### User Registration Fails
- Check password policy requirements
- Verify email/SMS delivery configuration
- Check user pool quota limits

### Token Validation Fails
- Verify token hasn't expired
- Check token signature
- Ensure correct User Pool ID in API Gateway

### Email/SMS Not Delivered
- Verify SES configuration (for production)
- Check Cognito service limits
- Verify email/phone format

### Hosted UI Not Loading
- Check domain configuration
- Verify app client settings
- Check callback URLs

## 🔄 Updates and Maintenance

When updating Cognito configuration:

1. Test changes in development User Pool first
2. Update app client settings
3. Update frontend configuration
4. Update API Gateway authorizer (if needed)
5. Test authentication flow end-to-end
6. Deploy to production User Pool

## 🤝 Contributing

When adding new authentication features:

1. Update Cognito User Pool configuration
2. Update frontend integration code
3. Update API Gateway authorizer
4. Update this documentation
5. Add testing instructions

## 📞 Support

For questions or issues:
- Review the detailed manual setup guide
- Check AWS Cognito documentation
- Open an issue in the repository
- Contact the Personal Finance team

## 🗺️ Roadmap

Future enhancements:

- [ ] Social identity provider integration
- [ ] Advanced security features (risk-based authentication)
- [ ] Custom authentication flows
- [ ] User migration from existing systems
- [ ] Advanced MFA options
- [ ] Account recovery workflows
- [ ] User impersonation for support
- [ ] Custom email templates
- [ ] Multi-region user pools
- [ ] Identity federation

---

**Next Steps**: Start with the [manual setup guide](./manual/README.md) or explore the [automation options](./automation/README.md).
