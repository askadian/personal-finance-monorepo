# Implementation Guide: Fixing the SECRET_HASH Error

## For Users Experiencing the Login Error

If you're seeing the error: **"Client is configured with secret but SECRET_HASH was not received"**

This guide will help you fix it in **5 minutes**.

---

## Quick Start

### Step 1: Identify Your Situation

Check your AWS Cognito App Client configuration:

1. Go to **AWS Console** → **Amazon Cognito** → **User Pools**
2. Select your User Pool
3. Go to **App integration** tab → **App client list**
4. Click on your app client
5. Look for **"Client secret"** field

**If you see a secret**: You need to fix this (follow steps below)  
**If it says "No client secret"**: Your configuration is correct; look for other issues in [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)

---

## Solution: Create a Public Client (Recommended)

This is the **correct** solution that follows AWS best practices.

### Time Required: ~5 minutes

### Steps:

1. **Create New Public Client**
   ```
   AWS Console → Cognito → User Pools → [Your Pool] → App integration
   → Click "Create app client"
   ```

2. **Configure as follows:**
   ```
   App client name: personal-finance-app-public
   App type: ✓ Public client
   
   Authentication flows:
   ✓ ALLOW_USER_PASSWORD_AUTH
   ✓ ALLOW_REFRESH_TOKEN_AUTH
   
   OAuth 2.0 grant types:
   ✓ Authorization code grant
   
   OAuth scopes:
   ✓ openid
   ✓ email
   ✓ profile
   
   Callback URLs:
   http://localhost:3000/
   http://localhost:3000/callback
   https://your-domain.com/ (for production)
   
   Sign-out URLs:
   http://localhost:3000/
   https://your-domain.com/ (for production)
   ```

3. **Update Your Configuration**
   
   Edit `frontend/src/aws-config.js`:
   ```javascript
   userPoolClientId: 'YOUR_NEW_CLIENT_ID', // Replace with new client ID
   ```
   
   Make sure this line looks like:
   ```javascript
   userPoolClientSecret: process.env.REACT_APP_COGNITO_APP_CLIENT_SECRET || undefined,
   ```

4. **Test**
   ```bash
   cd frontend
   npm start
   ```
   
   Try logging in → Error should be gone! ✅

5. **Clean Up** (Optional)
   - You can now delete the old app client with the secret
   - AWS Console → App integration → App client list → Select old client → Delete

---

## Alternative: Use Client Secret (Not Recommended)

⚠️ **Warning**: This approach has security implications and should only be used temporarily.

### Why Not Recommended?

- Client secrets in frontend code provide **no security**
- Anyone can view your JavaScript and extract the secret
- Goes against OAuth 2.0 best practices
- The secret will be visible in your browser's DevTools

### If You Must Use It Temporarily:

1. **Get Your Client Secret**
   ```
   AWS Console → Cognito → User Pools → [Your Pool] 
   → App integration → App client list → [Your client]
   → "Show client secret" → Copy
   ```

2. **Create `.env.local`** (NOT committed to git)
   ```bash
   cd frontend
   touch .env.local
   ```

3. **Add Secret to `.env.local`**
   ```
   REACT_APP_COGNITO_APP_CLIENT_SECRET=your_actual_secret_here
   ```

4. **Verify Configuration**
   
   Check `frontend/src/aws-config.js` has:
   ```javascript
   userPoolClientSecret: process.env.REACT_APP_COGNITO_APP_CLIENT_SECRET || undefined,
   ```

5. **Test**
   ```bash
   npm start
   ```

6. **Plan to Migrate**
   - This is a temporary workaround
   - Plan to create a public client soon
   - Never commit `.env.local` to git

---

## Verification

### How to Verify It's Fixed

1. **Start the app**
   ```bash
   cd frontend
   npm start
   ```

2. **Open browser**: http://localhost:3000

3. **Try to log in** with valid credentials

4. **Expected Results**:
   - ✅ Login succeeds
   - ✅ Redirected to dashboard
   - ✅ No SECRET_HASH error in console

5. **If still seeing errors**: Check [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)

---

## Understanding the Fix

### Why This Happens

AWS Cognito has two types of app clients:

| Type | Has Secret? | Used For | Example |
|------|-------------|----------|---------|
| **Public** | ❌ No | Frontend apps, mobile apps | React app, iOS app |
| **Confidential** | ✅ Yes | Backend services, servers | Node.js API, Python backend |

**The Problem**: Your app client was created as "Confidential" (with secret), but it's used by a frontend app.

**The Solution**: Use a "Public" client (no secret) for frontend apps.

### What Changed in This PR

This PR adds:

1. **Configuration Support**: Can now optionally specify client secret via environment variables
2. **Documentation**: Comprehensive guides on how to fix the issue
3. **Tests**: Validates configuration structure
4. **Default Behavior**: Secret defaults to `undefined` (not used unless explicitly set)

**But the real fix is**: Reconfigure your Cognito App Client as a public client!

---

## For Different Environments

### Development
```
Use: Public client
Callback URL: http://localhost:3000/
```

### Staging
```
Use: Public client (same as dev)
Callback URL: https://staging.your-domain.com/
```

### Production
```
Use: Public client (same as dev)
Callback URL: https://your-domain.com/
Enable: MFA, advanced security features
```

**Important**: All environments should use public clients (no secret)!

---

## FAQ

**Q: Can I just add the secret to my code?**  
A: Technically yes, but it's not secure and defeats the purpose of having a secret. The secret will be visible to anyone.

**Q: What if I can't access AWS Console?**  
A: You'll need to contact your AWS administrator to create a public client for you.

**Q: Will this break anything?**  
A: No! Creating a new public client doesn't affect existing users or data. You're just changing how the app authenticates.

**Q: Do I need to update my backend?**  
A: No, this is a frontend-only change. Your backend/API doesn't need any updates.

**Q: What about existing users?**  
A: They can continue to login normally. Changing the app client doesn't affect user accounts.

**Q: Can I have multiple app clients?**  
A: Yes! You can have multiple app clients for the same User Pool (e.g., one for web, one for mobile).

---

## Next Steps

After fixing the SECRET_HASH error:

1. ✅ Test login/logout flow
2. ✅ Test on different browsers
3. ✅ Update production configuration
4. ✅ Document your setup for your team
5. ✅ Consider enabling MFA for production

---

## Need Help?

1. **Check the guides**:
   - [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) - Full troubleshooting guide
   - [SECRET_HASH_FIX.md](./SECRET_HASH_FIX.md) - Quick reference
   - [COGNITO_SETUP.md](./COGNITO_SETUP.md) - Complete setup guide

2. **Check AWS documentation**:
   - [Cognito App Client Settings](https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-client-apps.html)
   - [AWS Amplify Auth](https://docs.amplify.aws/lib/auth/getting-started/q/platform/js/)

3. **Check browser console**:
   - Open DevTools (F12)
   - Look for specific error messages
   - Check Network tab for failed requests

---

## Summary

✅ **Recommended**: Create a new public client (no secret)  
⚠️ **Workaround**: Add secret to `.env.local` (temporary only)  
❌ **Never**: Commit secrets to git  
📚 **Always**: Follow AWS best practices

**Estimated time to fix**: 5-10 minutes  
**Difficulty**: Easy (just AWS Console configuration)

Good luck! 🚀
