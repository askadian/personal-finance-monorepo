# User Pool Setup

This guide walks through creating your AWS Cognito User Pool for the Personal Finance application.

## 📋 Overview

In this step, you will:
1. Create a new Cognito User Pool
2. Configure sign-in options
3. Set basic security settings
4. Configure user attributes

**Estimated Time**: 15-20 minutes

## 🚀 Step-by-Step Instructions

### Step 1: Navigate to Cognito

1. **Open AWS Management Console**
   - Navigate to https://console.aws.amazon.com/cognito/

2. **Select Region**
   - Choose your preferred region (e.g., `us-east-1`)
   - Note: Choose the same region as your other AWS resources

3. **Click "User Pools"** in the left sidebar

4. **Click "Create user pool"**

### Step 2: Configure Sign-in Experience

**Sign-in options:**
- ☑️ **Email** (Recommended)
- ☐ Username
- ☐ Phone number
- ☐ Preferred username

**Provider types:**
- ☑️ **Cognito user pool** (Selected by default)
- ☐ Federated identity providers (Optional - for social sign-in)

**User name requirements:**
- ☐ Make user name case sensitive (Not recommended)

Click **Next**

### Step 3: Configure Security Requirements

**Password policy:**
- **Password policy mode**: 
  - ☑️ **Cognito defaults** (Recommended for most apps)
  - ☐ Custom (If you need specific requirements)

**Cognito defaults include:**
- Minimum length: 8 characters
- Contains uppercase letters
- Contains lowercase letters
- Contains numbers
- Contains special characters

**Multi-factor authentication:**
- ☑️ **Optional MFA** (Recommended - users can enable if desired)
- ☐ Require MFA (Only if security is critical)
- ☐ No MFA

**MFA methods:**
- ☑️ **Authenticator apps** (TOTP - Recommended)
- ☑️ SMS message (Optional - incurs SMS costs)

**User account recovery:**
- ☑️ **Enable self-service account recovery** (Recommended)
- Recovery method: **Email only** (SMS optional)

Click **Next**

### Step 4: Configure Sign-up Experience

**Self-service sign-up:**
- ☑️ **Enable self-registration** (Users can sign up themselves)

**Cognito-assisted verification and confirmation:**
- **Allow Cognito to automatically send messages to verify and confirm:**
  - ☑️ **Send email message, verify email address** (Recommended)
  - ☐ Send SMS message, verify phone number (Optional)

**Verifying attribute changes:**
- ☑️ **Keep original attribute value active when an update is pending**
- This allows users to keep using their old email until new one is verified

**Required attributes:**
- ☑️ **email** (Already required due to sign-in option)
- ☐ name (Optional - recommended to keep optional)
- ☐ Other attributes (Add only if absolutely necessary)

**Custom attributes:**
- Leave empty for now (can add later if needed)
- ⚠️ Remember: Custom attributes are immutable once created

Click **Next**

### Step 5: Configure Message Delivery

**Email provider:**
- For Development/Testing:
  - ☑️ **Send email with Cognito** (Free, 50 emails/day limit)
- For Production:
  - ☐ Send email with Amazon SES (Unlimited, requires SES setup)

**SES Region:** (If using SES)
- Select same region as User Pool

**FROM email address:**
- If using Cognito: Will use `no-reply@verificationemail.com`
- If using SES: Enter your verified email (e.g., `noreply@yourdomain.com`)

**FROM sender name:**
- Optional: Enter a friendly name (e.g., "Personal Finance App")

**REPLY-TO email address:**
- Optional: Enter support email (e.g., `support@yourdomain.com`)

**SMS configuration:** (If using SMS MFA)
- Create new IAM role (AWS will do this automatically)
- Or select existing SNS role

Click **Next**

### Step 6: Integrate Your App

**User pool name:**
```
personal-finance-user-pool
```

**Hosted authentication pages:**
- ☑️ **Use the Cognito Hosted UI** (Recommended)

**Domain:**
Choose domain type:
- ☑️ **Use a Cognito domain** (For development/testing)
  - Enter prefix: `personal-finance-[your-unique-id]`
  - Full domain will be: `personal-finance-[your-unique-id].auth.us-east-1.amazoncognito.com`
- ☐ Use your own domain (For production)

**Initial app client:**
- **App client name:**
  ```
  personal-finance-app-client
  ```

- **Client secret:**
  - ☐ **Don't generate a client secret** (Recommended for frontend apps)
  - ⚠️ Frontend apps should use public clients without secrets

- **Authentication flows:**
  - ☑️ **ALLOW_USER_PASSWORD_AUTH** (Username/password auth)
  - ☑️ **ALLOW_REFRESH_TOKEN_AUTH** (Token refresh)
  - ☐ ALLOW_USER_SRP_AUTH (Secure Remote Password - optional)

Click **Next**

### Step 7: Review and Create

**Review all settings:**
1. Sign-in options: Email
2. Password policy: Cognito defaults
3. MFA: Optional (TOTP)
4. Self-registration: Enabled
5. Email verification: Enabled
6. Email provider: Cognito (or SES)
7. User pool name: personal-finance-user-pool
8. Hosted UI: Enabled
9. App client: personal-finance-app-client

**Create User Pool:**
- Click **"Create user pool"**
- Wait for creation to complete (~30 seconds)

### Step 8: Save Important Information

After creation, save these values:

**User Pool ID:**
```
us-east-1_XXXXXXXXX
```
- Find in: User Pool Overview page
- Needed for: Frontend and API Gateway configuration

**User Pool ARN:**
```
arn:aws:cognito-idp:us-east-1:123456789012:userpool/us-east-1_XXXXXXXXX
```
- Find in: User Pool Overview page
- Needed for: IAM policies

**Cognito Domain:**
```
https://personal-finance-[your-id].auth.us-east-1.amazoncognito.com
```
- Find in: App integration tab > Domain
- Needed for: Frontend login/signup redirects

**Save these in a secure location** (you'll need them for API Gateway and frontend setup)

## ✅ Verification Steps

After creating the User Pool:

1. **Verify User Pool Created:**
   ```
   AWS Console > Cognito > User pools
   Should see: personal-finance-user-pool
   Status: Active
   ```

2. **Check Domain Configuration:**
   ```
   User Pool > App integration tab > Domain
   Domain should be active and accessible
   ```

3. **Verify App Client:**
   ```
   User Pool > App integration tab > App client list
   Should see: personal-finance-app-client
   ```

## 📝 Configuration Summary

Your User Pool now has:
- ✅ Email-based sign-in
- ✅ Strong password policy
- ✅ Optional MFA with TOTP
- ✅ Self-service registration enabled
- ✅ Email verification required
- ✅ Hosted UI configured
- ✅ Basic app client created

## 🔍 Understanding User Pool Settings

### Sign-in Options
- **Email**: Users sign in with email address (user-friendly)
- Verification required to prevent fake accounts
- Can be used for password recovery

### Password Policy
- **Cognito defaults**: Good balance of security and usability
- Requires: 8+ chars, uppercase, lowercase, numbers, symbols
- Can be customized later if needed

### MFA Options
- **Optional**: Users can enable MFA for added security
- **TOTP**: Authenticator apps (Google Authenticator, Authy)
- **SMS**: Backup option (additional cost per SMS)

### Self-Service Registration
- **Enabled**: Users can create their own accounts
- **Email verification**: Prevents fake accounts
- **Admin approval**: Can be added later if needed

## 🔒 Security Features

Your User Pool includes:
1. **Email Verification**: Confirms valid email addresses
2. **Password Complexity**: Strong passwords required
3. **Account Recovery**: Users can reset passwords via email
4. **MFA Support**: Optional two-factor authentication
5. **Token-Based Auth**: Secure JWT tokens
6. **Session Management**: Configurable token expiration

## 🆘 Troubleshooting

### Domain Already Exists
- Error: "Domain prefix already taken"
- Solution: Try a different prefix (add random numbers)
- Example: `personal-finance-12345`

### Email Sending Limit
- Cognito free tier: 50 emails/day
- For production: Set up Amazon SES
- For testing: 50/day is usually sufficient

### User Pool Creation Fails
- Check IAM permissions for Cognito
- Verify region selection
- Try refreshing AWS Console
- Check AWS service health dashboard

### Cannot Find User Pool ID
- User Pool > Overview tab
- Look for "User pool ID" field
- Format: us-east-1_XXXXXXXXX

## 📋 Next Steps

You've successfully created your User Pool! Next, you'll:
1. Configure the app client with OAuth settings
2. Set up callback URLs
3. Configure token expiration

**Continue to**: [App Client Setup](./03-app-client-setup.md) →

## 📚 Additional Resources

- [User Pool Attributes](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-attributes.html)
- [Password Policies](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-policies.html)
- [Email Configuration](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-email.html)
- [MFA Configuration](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-mfa.html)

---

**Previous**: [Prerequisites](./01-prerequisites.md) | **Next**: [App Client Setup](./03-app-client-setup.md)
