# App Client Setup

This guide walks through configuring the app client for OAuth 2.0 integration with your frontend application.

## 📋 Overview

In this step, you will:
1. Configure OAuth 2.0 settings for your app client
2. Set up callback and logout URLs
3. Configure token expiration
4. Enable proper OAuth flows

**Estimated Time**: 15 minutes

## 🔑 What is an App Client?

An app client is a configuration that allows your application to interact with the Cognito User Pool:
- Contains OAuth 2.0 settings
- Defines allowed callback URLs
- Specifies token expiration times
- Can be public (frontend) or confidential (backend)

## 🚀 Step-by-Step Instructions

### Step 1: Access App Client Settings

1. **Navigate to your User Pool**
   - AWS Console > Cognito > User pools
   - Click on `personal-finance-user-pool`

2. **Go to App Integration Tab**
   - Click "App integration" tab at the top

3. **Find Your App Client**
   - Scroll to "App client list"
   - Click on `personal-finance-app-client`

### Step 2: Configure Hosted UI Settings

**Allowed callback URLs:**
Add URLs where users will be redirected after authentication:

```
Development:
http://localhost:3000/callback
http://localhost:3000/

Staging:
https://staging.yourdomain.com/callback
https://staging.yourdomain.com/

Production:
https://app.yourdomain.com/callback
https://app.yourdomain.com/
```

**Allowed sign-out URLs:**
Add URLs where users will be redirected after logout:

```
Development:
http://localhost:3000/
http://localhost:3000/login

Staging:
https://staging.yourdomain.com/
https://staging.yourdomain.com/login

Production:
https://app.yourdomain.com/
https://app.yourdomain.com/login
```

⚠️ **Important**: 
- URLs must match exactly (including trailing slashes)
- Only add HTTPS URLs for production
- HTTP allowed only for localhost

Click **Save changes**

### Step 3: Configure OAuth 2.0 Settings

**Identity providers:**
- ☑️ **Cognito user pool** (Should be selected by default)
- ☐ Google, Facebook, etc. (Optional - for social sign-in)

**OAuth 2.0 grant types:**
- ☑️ **Authorization code grant** (Recommended - most secure)
- ☐ Implicit grant (Not recommended - being deprecated)

**Allowed scopes:**
Select the following scopes:

- ☑️ **openid** (Required for OpenID Connect)
- ☑️ **email** (Access to email address)
- ☑️ **profile** (Access to user profile)
- ☐ phone (Only if using phone authentication)
- ☐ aws.cognito.signin.user.admin (Only if needed)

Click **Save changes**

### Step 4: Configure Advanced Settings

Navigate to **Advanced app client settings**:

**Authentication flows:**
Enable the following flows:

- ☑️ **ALLOW_USER_PASSWORD_AUTH**
  - For username/password authentication
  - Used by Hosted UI

- ☑️ **ALLOW_REFRESH_TOKEN_AUTH**
  - For refreshing access tokens
  - Required for long-term sessions

- ☑️ **ALLOW_USER_SRP_AUTH** (Optional)
  - Secure Remote Password protocol
  - Enhanced security for password authentication

- ☐ ALLOW_CUSTOM_AUTH
  - Only if implementing custom authentication challenges

**Token expiration:**
Configure token lifetimes:

```
Refresh token expiration: 30 days
Access token expiration: 60 minutes
ID token expiration: 60 minutes
```

**Recommended settings:**
- **Access tokens**: 1 hour (balance between security and UX)
- **ID tokens**: 1 hour (same as access tokens)
- **Refresh tokens**: 30 days (long-term sessions)

**Prevent user existence errors:**
- ☑️ **Enabled (Recommended)**
- Returns same error for non-existent users (prevents user enumeration)

Click **Save changes**

### Step 5: Configure Advanced Security (Optional)

**Advanced security features:**
- ☐ Enable advanced security (Additional cost: $0.05 per MAU)

Features included with advanced security:
- Adaptive authentication (risk-based authentication)
- Compromised credentials detection
- Account takeover protection

**Recommendation**: 
- Start without advanced security
- Enable later if needed for production

### Step 6: Save App Client Information

After configuration, save these important values:

**App client ID:**
```
1234567890abcdefghijklmnop
```
- Find in: App client overview
- Needed for: Frontend authentication code

**App client secret:**
```
Should be: (none) - public client
```
- ⚠️ If you see a secret, you might need to recreate the client
- Frontend apps should NOT have client secrets

**Hosted UI URL:**
```
https://personal-finance-[your-id].auth.us-east-1.amazoncognito.com/login?client_id=1234567890abcdefghijklmnop&response_type=code&scope=email+openid+profile&redirect_uri=http://localhost:3000/callback
```

To construct the hosted UI URL:
```
https://[DOMAIN]/login?
  client_id=[CLIENT_ID]&
  response_type=code&
  scope=email+openid+profile&
  redirect_uri=[CALLBACK_URL]
```

## ✅ Verification Steps

### 1. Test the Hosted UI URL

**Create test URL:**
Replace placeholders with your actual values:

```
https://[YOUR-COGNITO-DOMAIN]/login?client_id=[YOUR-CLIENT-ID]&response_type=code&scope=email+openid+profile&redirect_uri=http://localhost:3000/callback
```

**Open in browser:**
- You should see the Cognito login page
- Should have "Sign up" and "Sign in" options
- Should look like a standard login form

**What you should see:**
- Cognito branded login page
- Email and password fields
- "Sign up" link
- "Forgot password?" link

### 2. Verify OAuth Configuration

Check your configuration:
- ✅ Callback URLs added (at least localhost for testing)
- ✅ Sign-out URLs added
- ✅ Authorization code grant enabled
- ✅ Required scopes (openid, email, profile) selected
- ✅ Token expirations configured
- ✅ Refresh token auth enabled

### 3. Check App Client Type

Verify public client (for frontend):
- ❌ No client secret (should not exist)
- ✅ Authorization code grant enabled
- ✅ Callback URLs configured

## 📝 Configuration Summary

Your app client now has:
- ✅ OAuth 2.0 authorization code grant
- ✅ Callback and sign-out URLs configured
- ✅ Proper scopes (openid, email, profile)
- ✅ Reasonable token expiration (1 hour / 30 days)
- ✅ Public client (no secret)
- ✅ Refresh token support

## 🔍 Understanding OAuth Settings

### OAuth 2.0 Grant Types

**Authorization Code Grant:**
- Most secure for web applications
- Uses code exchange for tokens
- Tokens never exposed in URL
- Supports PKCE for public clients
- **Recommended for this project**

**Implicit Grant:**
- Simpler but less secure
- Tokens returned in URL fragment
- No refresh token support
- Being deprecated by OAuth 2.0 spec
- **Not recommended**

### OAuth Scopes

**openid:**
- Required for OpenID Connect
- Enables ID token issuance
- Provides basic user identification

**email:**
- Grants access to user's email address
- Email included in ID token
- Required if using email-based features

**profile:**
- Grants access to user profile attributes
- Includes name, picture, etc.
- Useful for personalization

### Token Types and Usage

**ID Token:**
- Contains user identity claims
- Used by frontend to display user info
- Should not be sent to APIs
- Parse to get user email, name, etc.

**Access Token:**
- Used for API authorization
- Send in Authorization header to API Gateway
- Short-lived for security
- Contains scopes and permissions

**Refresh Token:**
- Used to get new access/ID tokens
- Long-lived
- Should be stored securely
- Can be revoked

## 🔒 Security Best Practices

### Client Secret Handling
- ✅ **No secret for frontend apps** (public clients)
- ✅ Use PKCE for authorization code flow
- ❌ Never expose secrets in frontend code
- ❌ Never commit secrets to version control

### URL Whitelisting
- ✅ Only add your actual application URLs
- ✅ Use HTTPS for all production URLs
- ✅ Keep callback URLs specific (avoid wildcards)
- ❌ Don't use `*` or overly broad patterns

### Token Storage
- ✅ Store tokens securely (HttpOnly cookies or secure storage)
- ✅ Implement token refresh logic
- ✅ Clear tokens on logout
- ❌ Never store tokens in localStorage (XSS vulnerability)

## 🆘 Troubleshooting

### "redirect_uri_mismatch" Error
- **Cause**: Callback URL not whitelisted
- **Solution**: Add exact URL to "Allowed callback URLs"
- **Remember**: URLs are case-sensitive and must match exactly

### Hosted UI Not Loading
- **Cause**: Incorrect domain or client ID
- **Solution**: Verify domain is active and client ID is correct
- **Check**: User Pool > App integration > Domain

### No Tokens Received
- **Cause**: Response type or grant type misconfigured
- **Solution**: Ensure "Authorization code grant" is enabled
- **Check**: response_type=code in URL

### Token Immediately Expires
- **Cause**: Token expiration too short
- **Solution**: Increase token expiration to at least 1 hour
- **Check**: App client settings > Token expiration

### Cannot Sign Up
- **Cause**: Scopes not properly configured
- **Solution**: Ensure openid, email, profile scopes are selected
- **Check**: OAuth 2.0 grant types and scopes

## 📋 Next Steps

Your app client is now configured! Next steps:

1. **Set up the Hosted UI** - Customize login page appearance
2. **Configure user attributes** - Define required and optional fields
3. **Test authentication flow** - Create test user and verify login

**Continue to**: [Hosted UI Setup](./04-hosted-ui-setup.md) →

## 📚 Additional Resources

- [App Client Settings](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-client-apps.html)
- [OAuth 2.0 Authorization Code Grant](https://oauth.net/2/grant-types/authorization-code/)
- [OpenID Connect Scopes](https://openid.net/specs/openid-connect-core-1_0.html#ScopeClaims)
- [Token Expiration Best Practices](https://auth0.com/docs/tokens/token-best-practices)

---

**Previous**: [User Pool Setup](./02-user-pool-setup.md) | **Next**: [Hosted UI Setup](./04-hosted-ui-setup.md)
