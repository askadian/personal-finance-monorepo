# Hosted UI Setup

This guide walks through customizing the Cognito Hosted UI for your application's branding.

## 📋 Overview

In this step, you will:
1. Customize the Hosted UI appearance
2. Configure branding elements
3. Test the customized login page
4. Understand customization options

**Estimated Time**: 10-15 minutes

## 🎨 What is Hosted UI?

The Hosted UI is a pre-built, OAuth 2.0-compliant login interface provided by AWS Cognito:
- Handles authentication flow automatically
- Provides login, signup, and password reset pages
- Can be customized with your branding
- Supports internationalization
- Mobile-responsive design

## 🚀 Step-by-Step Instructions

### Step 1: Access Hosted UI Settings

1. **Navigate to your User Pool**
   - AWS Console > Cognito > User pools
   - Click on `personal-finance-user-pool`

2. **Go to App Integration Tab**
   - Click "App integration" tab

3. **Find Hosted UI Section**
   - Scroll to "Hosted UI customization"

### Step 2: Configure Basic Branding

**App logo:**
- Upload your application logo
- Recommended size: 300x300 pixels or similar square aspect ratio
- Formats: PNG, JPG, SVG
- Max file size: 100KB
- Will display at top of login page

**Logo placement:**
- Automatically centered above login form
- Maintains aspect ratio

**App name:**
```
Personal Finance
```
- Displays as page title and in email templates

### Step 3: Customize CSS (Optional)

**Custom CSS:**
You can override default styles using custom CSS:

```css
/* Example customizations */
.banner-customizable {
  background-color: #1a73e8;
}

.submitButton-customizable {
  background-color: #1a73e8;
  border-color: #1a73e8;
}

.submitButton-customizable:hover {
  background-color: #1557b0;
}

.textDescription-customizable {
  color: #5f6368;
}

.inputField-customizable {
  border-radius: 4px;
  border: 1px solid #dadce0;
}

.inputField-customizable:focus {
  border-color: #1a73e8;
  box-shadow: 0 0 0 1px #1a73e8;
}

.errorMessage-customizable {
  color: #d93025;
}
```

**Available CSS classes:**
- `.banner-customizable` - Top banner area
- `.label-customizable` - Input labels
- `.textDescription-customizable` - Description text
- `.inputField-customizable` - Input fields
- `.submitButton-customizable` - Submit buttons
- `.errorMessage-customizable` - Error messages
- `.linkStyle-customizable` - Links (signup, forgot password)

### Step 4: Preview and Test

**Test the Hosted UI:**

1. **Get your Hosted UI URL:**
   ```
   https://[YOUR-DOMAIN].auth.[REGION].amazoncognito.com/login?client_id=[CLIENT-ID]&response_type=code&scope=email+openid+profile&redirect_uri=[CALLBACK-URL]
   ```

2. **Open in browser** to see:
   - Your custom logo
   - Custom CSS styling
   - Login form
   - Sign up link
   - Forgot password link

3. **Test on mobile** - Verify responsive design

### Step 5: Configure Domain (If Not Done)

If you haven't set up a domain yet:

**Using Cognito Domain:**
1. Go to App integration > Domain
2. Click "Create Cognito domain"
3. Enter prefix: `personal-finance-[unique-id]`
4. Click "Create"
5. Domain will be: `personal-finance-[unique-id].auth.us-east-1.amazoncognito.com`

**Using Custom Domain** (Production):
1. Go to App integration > Domain
2. Click "Create custom domain"
3. Enter your domain: `auth.yourdomain.com`
4. Select ACM certificate (must be in us-east-1)
5. Click "Create"
6. Update DNS with provided values

## ✅ Verification Steps

### Test Authentication Flow

1. **Navigate to Hosted UI URL**
2. **Try to sign up** (will test in detail later)
3. **Verify UI appearance:**
   - Logo displays correctly
   - Colors match your brand
   - Text is readable
   - Buttons are styled properly
   - Mobile responsive

### Check All Pages

The Hosted UI includes multiple pages:

**Login page:**
- Email and password fields
- Sign in button
- Links to sign up and forgot password

**Sign up page:**
- Email field
- Password field (with requirements shown)
- Confirm password field
- Sign up button

**Forgot password page:**
- Email field
- Send code button
- Enter code and new password fields

**Email verification page:**
- Verification code input
- Resend code option

## 📝 Customization Options

### Logo Guidelines

**Recommended specifications:**
- Dimensions: 300x300px (or similar square)
- Format: PNG with transparency
- File size: < 100KB
- Style: Simple, recognizable icon or wordmark

**Best practices:**
- Use high contrast against white background
- Ensure logo is clear at small sizes
- Test on both desktop and mobile

### Color Scheme

**Match your brand:**
```css
/* Primary color */
.submitButton-customizable {
  background-color: #YOUR-PRIMARY-COLOR;
}

/* Accent color */
.inputField-customizable:focus {
  border-color: #YOUR-ACCENT-COLOR;
}

/* Error color */
.errorMessage-customizable {
  color: #YOUR-ERROR-COLOR;
}
```

### Typography

**Custom fonts (via CSS):**
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

.label-customizable,
.textDescription-customizable,
.inputField-customizable {
  font-family: 'Inter', sans-serif;
}
```

## 🔍 Understanding Hosted UI Features

### Built-in Pages

**Login Page:**
- Standard email/password login
- "Remember me" option (optional)
- Error messages for invalid credentials
- Links to sign up and password reset

**Sign-up Page:**
- Email input
- Password input with strength indicator
- Confirm password
- Required attributes (e.g., name)
- Terms of service checkbox (optional)

**Password Reset:**
- Email input
- Code delivery via email
- New password input
- Password strength requirements

**Verification:**
- Email verification code input
- Resend code functionality
- Auto-verification with email link

### Internationalization

Hosted UI supports multiple languages:
- Auto-detects browser language
- Falls back to English
- Supported languages: 20+ including Spanish, French, German, Japanese, etc.

### Mobile Responsiveness

- Automatically adapts to screen size
- Touch-friendly buttons and inputs
- Mobile keyboard optimizations
- Proper viewport settings

## 🆘 Troubleshooting

### Logo Not Displaying
- **Cause**: Image too large or wrong format
- **Solution**: Resize to < 100KB, use PNG or JPG
- **Check**: Image dimensions and file size

### CSS Not Applied
- **Cause**: Invalid CSS syntax
- **Solution**: Validate CSS, check class names
- **Test**: Remove CSS and re-add section by section

### Hosted UI Returns Error
- **Cause**: Callback URL mismatch
- **Solution**: Verify callback URL in app client settings
- **Check**: URL is exactly as configured

### Custom Domain Not Working
- **Cause**: DNS not configured or certificate issue
- **Solution**: Verify DNS CNAME record, check ACM certificate
- **Note**: Certificate must be in us-east-1 region

### Blank Page or 400 Error
- **Cause**: Missing required parameters in URL
- **Solution**: Include client_id, response_type, redirect_uri
- **Check**: All URL parameters are properly encoded

## 📋 Next Steps

Your Hosted UI is now customized! Next:

1. **Configure user attributes** - Define what info you collect
2. **Set password policies** - Configure security requirements
3. **Test complete flow** - End-to-end authentication test

**Continue to**: [User Attributes](./05-user-attributes.md) →

## 💡 Advanced Customization

### Fully Custom UI (Alternative)

If you need complete control:
- Build custom login pages in your frontend
- Use AWS Amplify or Cognito SDK
- Implement OAuth flow manually
- More complex but fully customizable

**When to use custom UI:**
- Need very specific UX
- Want to match existing app design exactly
- Have complex authentication flows
- Hosted UI limitations are too restrictive

**When to use Hosted UI:**
- Quick setup
- Standard OAuth flows sufficient
- Don't want to maintain auth UI
- Want automatic security updates

## 📚 Additional Resources

- [Hosted UI Customization](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-app-ui-customization.html)
- [Custom Domain Setup](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-add-custom-domain.html)
- [CSS Customization Guide](https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-app-ui-customization.html#cognito-user-pools-app-ui-customization-css)

---

**Previous**: [App Client Setup](./03-app-client-setup.md) | **Next**: [User Attributes](./05-user-attributes.md)
