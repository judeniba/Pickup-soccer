# 🎨 Render.com Deployment Guide

## Why Render?
- ✅ **Free Tier Available** - $0/month for testing
- ✅ **Native Docker Support** - Works with your Dockerfile
- ✅ **Automatic HTTPS** - Free SSL certificates
- ✅ **Easy as Railway** - Simple GitHub integration
- ✅ **Better than Vercel** - Supports Spark workloads

## Quick Deploy (5 minutes)

### Step 1: Sign Up
1. Go to https://render.com
2. Click "Get Started"
3. Sign up with GitHub

### Step 2: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub account
3. Select **Pickup-soccer** repository
4. Render auto-detects Docker

### Step 3: Configure Service
```yaml
Name: pickup-soccer-api
Environment: Docker
Region: Oregon (US West)
Branch: main
Build Command: (auto-detected from Dockerfile)
Start Command: python -m uvicorn api:app --host 0.0.0.0 --port $PORT
```

### Step 4: Set Environment Variables
Add these in Render dashboard:
```bash
PYTHONUNBUFFERED=1
PYSPARK_PYTHON=python3.11
PYSPARK_DRIVER_PYTHON=python3.11
PORT=10000
```

### Step 5: Deploy!
Click "Create Web Service" - Render will:
- Build your Docker image
- Deploy to cloud
- Provide public URL

## Your Live URLs

After deployment:
```
Landing Page: https://pickup-soccer-api.onrender.com
API Docs: https://pickup-soccer-api.onrender.com/docs
Health Check: https://pickup-soccer-api.onrender.com/api/health
```

## Generate Sample Data

After first deployment, use Render Shell:
```bash
# In Render Dashboard → Shell tab
python scripts/generate_data.py
```

## Deploy Dashboard (Separate Service)

### Option 1: Render (Recommended)
1. Click "New +" → "Web Service"
2. Same repository
3. Different configuration:
```yaml
Name: pickup-soccer-dashboard
Start Command: streamlit run dashboard.py --server.port=$PORT --server.address=0.0.0.0
```

### Option 2: Streamlit Cloud (Free)
1. Go to https://share.streamlit.io
2. Connect GitHub → Select Pickup-soccer
3. Main file: `dashboard.py`
4. Deploy

Result:
- API: `https://pickup-soccer-api.onrender.com`
- Dashboard: `https://pickup-soccer-dashboard.onrender.com`

## Pricing

### Free Tier
- **Cost**: $0/month
- **Specs**: 512MB RAM, 0.1 CPU
- **Limitations**: Spins down after 15 min inactivity
- **Good for**: Testing, demos, personal projects

### Starter Tier ($7/month)
- **Cost**: $7/month per service
- **Specs**: 512MB RAM, always on
- **No spin down**: Instant response
- **Good for**: Small production apps

### Standard Tier ($25/month)
- **Specs**: 2GB RAM, 1 CPU
- **Good for**: Production workloads

## Custom Domain

1. Go to service settings
2. Click "Custom Domains"
3. Add your domain: `api.yourdomain.com`
4. Update DNS records as instructed
5. Free SSL auto-configured

## Persistent Storage

Render provides persistent disks:

1. Go to service settings
2. Click "Disks"
3. Add disk: `/app/data` (mount path)
4. Size: 1GB (free tier)
5. Your Parquet files persist across deploys

## Health Checks

Render auto-configures health checks:
```yaml
Health Check Path: /api/health
Health Check Interval: 30s
```

Already configured in your `api.py`!

## Logs & Monitoring

View logs in real-time:
```bash
# In Render Dashboard
Logs tab → Live tail
```

## Troubleshooting

### Build Fails
```bash
# Check build logs in Render dashboard
# Most common: Missing dependencies in requirements.txt
```

### Out of Memory
```bash
# Upgrade to Standard tier (2GB RAM)
# Or optimize Spark config in src/config.py
```

### Service Not Starting
```bash
# Check start command matches:
python -m uvicorn api:app --host 0.0.0.0 --port $PORT

# Not: uvicorn api:app (missing module flag)
```

### Slow Response (Free Tier)
```bash
# Free tier spins down after 15 min
# First request takes ~30-60 seconds (cold start)
# Solution: Upgrade to Starter tier ($7/month)
```

## Advantages over Railway

✅ **Free Tier**: Render has generous free tier  
✅ **Persistent Disks**: Built-in storage management  
✅ **Better for Spark**: More RAM options  
✅ **Cron Jobs**: Schedule data generation  
✅ **Preview Environments**: Auto-deploy PR branches  

## Deployment Checklist

- [ ] Sign up at render.com
- [ ] Connect GitHub repository
- [ ] Create web service with Docker
- [ ] Set environment variables
- [ ] Deploy and wait for build
- [ ] Generate sample data via Shell
- [ ] Test all endpoints via `/docs`
- [ ] (Optional) Add custom domain
- [ ] (Optional) Deploy dashboard separately

## Next Steps

### Add Cron Job for Data Refresh
```yaml
# In Render Dashboard → Cron Jobs
Name: refresh-data
Schedule: 0 0 * * * (daily at midnight)
Command: python scripts/generate_data.py
```

### Add PostgreSQL Database
```yaml
# Instead of Parquet files
1. Add PostgreSQL service in Render
2. Get DATABASE_URL from dashboard
3. Update src/config.py to use PostgreSQL
```

### CI/CD Integration
Render auto-deploys on git push to main:
- Push to GitHub → Render builds → Auto-deploy
- No extra configuration needed!

## Support

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- Project Docs: See DEVELOPMENT_GUIDE.md

---

**Ready to Deploy?** → https://render.com 🚀
