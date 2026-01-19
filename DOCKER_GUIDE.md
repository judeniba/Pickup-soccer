# 🐳 Docker Deployment Guide

## Quick Start

### Prerequisites
- Docker Desktop installed and running
- At least 4GB RAM allocated to Docker

### Launch Everything
```powershell
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build
```

Access:
- **API**: http://localhost:8000/docs
- **Dashboard**: http://localhost:8501

### Stop Services
```powershell
docker-compose down
```

## Individual Services

### API Only
```powershell
docker-compose up api
```

### Dashboard Only
```powershell
docker-compose up dashboard
```

## Development Mode

The Docker setup includes volume mounts for hot-reloading:
- Changes to `src/` are immediately reflected
- API auto-reloads on code changes
- Dashboard auto-reloads on code changes

## Building for Production

### Build Docker Image
```powershell
docker build -t pickup-soccer:latest .
```

### Run API Container
```powershell
docker run -d `
  -p 8000:8000 `
  -v ${PWD}/data:/app/data `
  --name pickup-soccer-api `
  pickup-soccer:latest `
  python3.11 -m uvicorn api:app --host 0.0.0.0 --port 8000
```

### Run Dashboard Container
```powershell
docker run -d `
  -p 8501:8501 `
  -v ${PWD}/data:/app/data `
  --name pickup-soccer-dashboard `
  pickup-soccer:latest `
  python3.11 -m streamlit run dashboard.py --server.port=8501 --server.address=0.0.0.0
```

## Troubleshooting

### Container Won't Start
```powershell
# Check logs
docker-compose logs api
docker-compose logs dashboard

# Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### Port Already in Use
```powershell
# Check what's using the port
netstat -ano | findstr :8000
netstat -ano | findstr :8501

# Kill the process (replace PID)
taskkill /PID <PID> /F
```

### Data Not Persisting
The `data/` directory is mounted as a volume. Ensure your sample data exists:
```powershell
# Generate sample data first
.\venv311\Scripts\Activate.ps1
python scripts/generate_data.py
```

## Environment Variables

Customize in `docker-compose.yml`:
- `PYSPARK_PYTHON`: Python executable for Spark workers
- `PYSPARK_DRIVER_PYTHON`: Python executable for Spark driver
- `PYTHONUNBUFFERED`: Enable real-time logging

## Resource Limits

Add to services in `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 4G
```

## Next Steps

1. **Push to Registry**:
   ```powershell
   docker tag pickup-soccer:latest your-registry/pickup-soccer:latest
   docker push your-registry/pickup-soccer:latest
   ```

2. **Deploy to Cloud**:
   - AWS ECS
   - Azure Container Instances
   - Google Cloud Run
   - Kubernetes

3. **Add Database**:
   - Add PostgreSQL service to `docker-compose.yml`
   - Configure persistent volumes

4. **CI/CD Integration**:
   - GitHub Actions
   - Azure DevOps
   - Jenkins
