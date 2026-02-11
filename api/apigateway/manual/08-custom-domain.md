# Custom Domain Setup (Optional)

This guide walks through configuring a custom domain for your API Gateway.

## 📋 Overview

Instead of using the default API Gateway URL:
```
https://abc123.execute-api.us-east-1.amazonaws.com/prod
```

Use a custom domain:
```
https://api.personal-finance.example.com
```

**Estimated Time**: 30-45 minutes

## Prerequisites

- ✅ Domain name registered (Route 53, GoDaddy, etc.)
- ✅ Access to DNS configuration
- ✅ AWS Certificate Manager certificate (or ability to create one)

## 🚀 Step-by-Step Instructions

### Step 1: Request SSL Certificate

1. **Go to AWS Certificate Manager**
   - Navigate to: https://console.aws.amazon.com/acm/
   - **Region**: Must be in `us-east-1` for edge-optimized, or same region as API for regional

2. **Request Certificate**
   - Click **Request a certificate**
   - Select **Request a public certificate**
   - Click **Next**

3. **Domain Names**:
   ```
   api.personal-finance.example.com
   *.api.personal-finance.example.com  (optional - for subdomains)
   ```

4. **Validation Method**:
   - Select **DNS validation** (recommended)
   - Click **Request**

5. **DNS Validation**:
   - Add CNAME records to your DNS
   - If using Route 53, click "Create records in Route 53"
   - Wait for validation (5-30 minutes)

### Step 2: Create Custom Domain in API Gateway

1. **Go to API Gateway**
   - Click **Custom Domain Names** in left sidebar

2. **Create Custom Domain Name**:
   - Domain Name: `api.personal-finance.example.com`
   - TLS Version: **TLS 1.2** (recommended)
   - Endpoint Type: **Regional** (matches your API)
   - ACM Certificate: Select your certificate

3. **Click Create**

4. **Note the Target Domain**:
   - Format: `d-abc123.execute-api.us-east-1.amazonaws.com`
   - You'll use this for DNS configuration

### Step 3: Configure API Mappings

Map your custom domain to API stages:

1. **API Mappings Tab**

2. **Configure API Mapping**:
   - API: Select `personal-finance-api`
   - Stage: `prod`
   - Path: Leave empty (or use `/` for default)

3. **Add Additional Mappings** (optional):
   - API: `personal-finance-api`
   - Stage: `dev`
   - Path: `dev`
   
   This creates:
   - `https://api.example.com` → prod stage
   - `https://api.example.com/dev` → dev stage

4. **Save**

### Step 4: Configure DNS

#### Using Route 53:

1. **Go to Route 53 Console**

2. **Select Hosted Zone** for your domain

3. **Create Record**:
   - Record name: `api`
   - Record type: **A** (Alias)
   - Alias to: **API Gateway API**
   - Region: Select your region
   - API Gateway domain: Select your custom domain
   - Routing policy: Simple
   - Click **Create records**

#### Using External DNS Provider:

1. **Create CNAME Record**:
   - Name: `api`
   - Type: `CNAME`
   - Value: `d-abc123.execute-api.us-east-1.amazonaws.com`
   - TTL: `300`

### Step 5: Test Custom Domain

Wait 5-10 minutes for DNS propagation, then test:

```bash
# Test custom domain
curl https://api.personal-finance.example.com/v1/transactions \
  -H "Authorization: Bearer YOUR_TOKEN"

# Check DNS resolution
nslookup api.personal-finance.example.com
dig api.personal-finance.example.com
```

## 📋 Checklist

- [ ] SSL certificate created and validated
- [ ] Custom domain created in API Gateway
- [ ] API mapping configured for prod stage
- [ ] DNS record created (A record or CNAME)
- [ ] Custom domain accessible via HTTPS
- [ ] Frontend updated with new API URL

## 🚨 Troubleshooting

### Certificate Pending Validation
**Solution**: Add CNAME records to DNS, wait up to 30 minutes

### Custom Domain Not Accessible
**Solution**: Check DNS propagation (use dig/nslookup), wait longer

### SSL Certificate Not Available
**Solution**: Ensure certificate is in correct region (us-east-1 for edge)

## 💡 Best Practices

1. **Use Regional Endpoint**: Lower latency for single-region apps
2. **Separate Domains**: Consider different domains for different environments
3. **Use Route 53**: Simplifies DNS management with AWS
4. **Monitor Certificate Expiration**: ACM auto-renews if using DNS validation

---

**Next Step**: [Monitoring and Logging](./09-monitoring-logging.md) →

**Previous Step**: [← Deployment and Stages](./07-deployment-stages.md)

**Back to**: [Manual Setup Guide](./README.md)
