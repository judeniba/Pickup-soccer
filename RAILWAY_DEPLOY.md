# 🚂 Railway Deployment Guide

## Quick Deploy to Railway

### Prerequisites
- GitHub account
- Railway account (sign up at https://railway.app)

### Step-by-Step Deployment

#### 1. Sign Up / Login to Railway
1. Go to https://railway.app
2. Click "Login with GitHub"
3. Authorize Railway to access your repositories

#### 2. Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose **judeniba/Pickup-soccer**
4. Railway will automatically:
   - Detect your Dockerfile
   - Build the container
   - Deploy your API

#### 3. Configure Environment (if needed)
Railway automatically sets:
- `PORT` (dynamic)
- `JAVA_HOME` (from Docker image)
- `HADOOP_HOME` (from Docker image)

Optional variables (add in Railway dashboard):
```
PYTHONUNBUFFERED=1
PYSPARK_PYTHON=python3.11
PYSPARK_DRIVER_PYTHON=python3.11
```

#### 4. Generate Sample Data (One-time)
After first deployment, run this command in Railway terminal:
```bash
python scripts/generate_data.py
```

#### 5. Access Your API
Railway provides a public URL like:
```
https://pickup-soccer-production.up.railway.app
```

Test endpoints:
- API Docs: `https://your-url.railway.app/docs`
- Health Check: `https://your-url.railway.app/api/health`
- Players: `https://your-url.railway.app/api/players`

### What Railway Deploys

#### API Service
- **Endpoint**: Your FastAPI REST API
- **Port**: Auto-assigned by Railway
- **Healthcheck**: `/api/health`
- **Documentation**: `/docs` (Swagger UI)

#### Resources Included
- ✅ JDK 17 (from Dockerfile)
- ✅ Python 3.11
- ✅ Apache Spark 4.1.1
- ✅ All dependencies from requirements.txt

### Managing Your Deployment

#### View Logs
```bash
# In Railway dashboard
Click on your service → Deployments → View Logs
```

#### Restart Service
```bash
# In Railway dashboard
Settings → Redeploy
```

#### Environment Variables
```bash
# In Railway dashboard
Variables tab → Add variable
```

### Deployment Options

#### Option 1: API Only (Current Setup)
- Deploys FastAPI REST API
- Access via public URL
- Best for: Mobile apps, external integrations

#### Option 2: API + Dashboard (docker-compose)
Railway can deploy both services:
```yaml
# Railway will use docker-compose.yml
services:
  api:
    build: .
    command: python -m uvicorn api:app --host 0.0.0.0 --port $PORT
  
  dashboard:
    build: .
    command: streamlit run dashboard.py --server.port=$PORT
```

Deploy each as separate Railway service.

### Cost Estimate

Railway Pricing:
- **Free Tier**: $5/month credit (enough for testing)
- **Usage-based**: $0.000231/GB-hour for compute
- **Estimated**: ~$5-10/month for this app

### Alternative: Deploy Dashboard to Streamlit Cloud

While API runs on Railway, deploy dashboard separately:

1. Go to https://share.streamlit.io
2. Connect GitHub repository
3. Set main file: `dashboard.py`
4. Add secrets (if needed)
5. Deploy

This gives you:
- API: `https://pickup-soccer-api.railway.app`
- Dashboard: `https://pickup-soccer.streamlit.app`

## Troubleshooting

### Build Fails
```bash
# Check Dockerfile syntax
docker build -t pickup-soccer .

# If successful locally, Railway should work
```

### Spark Errors
```bash
# Ensure environment variables are set
JAVA_HOME=/opt/java/openjdk
HADOOP_HOME (not required on Linux)
```

### Out of Memory
```bash
# In Railway dashboard
Settings → Increase memory limit
# Or optimize Spark config in src/config.py
```

### API Not Responding
```bash
# Check health endpoint first
curl https://your-url.railway.app/api/health

# Check logs for errors
Railway Dashboard → Logs
```

## Production Checklist

Before going live:

- [ ] Generate sample data: `python scripts/generate_data.py`
- [ ] Test all endpoints: Visit `/docs`
- [ ] Enable authentication (if needed)
- [ ] Set up custom domain (in Railway settings)
- [ ] Configure environment variables
- [ ] Enable monitoring/logging
- [ ] Set up backup for data files

## Next Steps After Deployment

1. **Custom Domain**: Add your domain in Railway settings
2. **Authentication**: Add JWT token protection (see DEVELOPMENT_GUIDE.md)
3. **Database**: Replace Parquet files with PostgreSQL
4. **Monitoring**: Add logging and metrics
5. **CI/CD**: Set up GitHub Actions for automated testing

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Project Docs: See DEVELOPMENT_GUIDE.md
