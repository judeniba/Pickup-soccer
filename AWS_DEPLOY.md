# ☁️ AWS Deployment Guide (ECS Fargate)

## Why AWS?
- ✅ **Enterprise Grade** - Used by Fortune 500 companies
- ✅ **Highly Scalable** - Auto-scaling, load balancing
- ✅ **Full Control** - Complete infrastructure management
- ✅ **RDS Integration** - Replace Parquet with PostgreSQL
- ✅ **Free Tier** - 12 months free for new accounts

## Architecture Overview

```
Internet → ALB (Load Balancer) → ECS Fargate (Docker) → RDS (Optional)
                                      ↓
                                   ECR (Container Registry)
```

## Prerequisites

1. **AWS Account** - Sign up at https://aws.amazon.com
2. **AWS CLI** - Install: https://aws.amazon.com/cli/
3. **Docker Desktop** - Already installed
4. **IAM User** - Create with ECS, ECR permissions

## Deployment Methods

### Method 1: AWS Copilot (Easiest)

#### Install AWS Copilot
```powershell
# Install via PowerShell
Invoke-WebRequest -UseBasicParsing https://github.com/aws/copilot-cli/releases/latest/download/copilot-windows.exe -OutFile $env:USERPROFILE\copilot.exe
Move-Item $env:USERPROFILE\copilot.exe C:\Windows\System32\
```

#### Deploy in 3 Commands
```powershell
# 1. Initialize app
copilot app init pickup-soccer

# 2. Deploy API service
copilot svc init --name api --svc-type "Load Balanced Web Service" --dockerfile Dockerfile

# 3. Deploy to environment
copilot deploy
```

AWS Copilot will:
- ✅ Create VPC, Subnets, Security Groups
- ✅ Build and push Docker image to ECR
- ✅ Create ECS cluster and service
- ✅ Configure Application Load Balancer
- ✅ Provide public URL

#### Access Your App
```bash
# Get URL from Copilot
copilot svc show api

# Output will show:
# URL: http://pickup-api-xxxxx.us-east-1.elb.amazonaws.com
```

### Method 2: Manual Setup (Full Control)

#### Step 1: Create ECR Repository
```powershell
# Create container registry
aws ecr create-repository --repository-name pickup-soccer --region us-east-1

# Authenticate Docker
$ecrUri = aws ecr describe-repositories --repository-names pickup-soccer --query 'repositories[0].repositoryUri' --output text
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ecrUri
```

#### Step 2: Build and Push Image
```powershell
# Build image
docker build -t pickup-soccer .

# Tag for ECR
docker tag pickup-soccer:latest $ecrUri:latest

# Push to ECR
docker push $ecrUri:latest
```

#### Step 3: Create ECS Cluster
```powershell
# Create cluster
aws ecs create-cluster --cluster-name pickup-soccer-cluster --region us-east-1
```

#### Step 4: Create Task Definition

Create `ecs-task-definition.json`:
```json
{
  "family": "pickup-soccer",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "api",
      "image": "YOUR_ECR_URI:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "PYTHONUNBUFFERED", "value": "1"},
        {"name": "PYSPARK_PYTHON", "value": "python3.11"},
        {"name": "PYSPARK_DRIVER_PYTHON", "value": "python3.11"}
      ],
      "command": ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/pickup-soccer",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "api"
        }
      }
    }
  ]
}
```

Register task:
```powershell
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json
```

#### Step 5: Create Application Load Balancer
```powershell
# Create ALB (requires VPC, subnets, security groups)
# Use AWS Console for easier setup:
# 1. EC2 → Load Balancers → Create
# 2. Application Load Balancer
# 3. Internet-facing, IPv4
# 4. Select VPC and subnets (at least 2 AZs)
# 5. Create target group: pickup-soccer-tg (HTTP:8000)
# 6. Health check: /api/health
```

#### Step 6: Create ECS Service
```powershell
aws ecs create-service `
  --cluster pickup-soccer-cluster `
  --service-name api `
  --task-definition pickup-soccer `
  --desired-count 1 `
  --launch-type FARGATE `
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx,subnet-yyy],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" `
  --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=api,containerPort=8000"
```

### Method 3: AWS App Runner (Simplest)

AWS App Runner is like Render but on AWS:

```powershell
# Create App Runner service
aws apprunner create-service `
  --service-name pickup-soccer `
  --source-configuration '{
    "CodeRepository": {
      "RepositoryUrl": "https://github.com/judeniba/Pickup-soccer",
      "SourceCodeVersion": {"Type": "BRANCH", "Value": "main"},
      "CodeConfiguration": {
        "ConfigurationSource": "API",
        "CodeConfigurationValues": {
          "Runtime": "PYTHON_3",
          "BuildCommand": "pip install -r requirements.txt",
          "StartCommand": "python -m uvicorn api:app --host 0.0.0.0 --port 8000",
          "Port": "8000"
        }
      }
    }
  }'
```

⚠️ **Note**: App Runner doesn't support Docker images with JDK out of the box. Use Copilot or ECS instead.

## Add PostgreSQL Database (RDS)

### Create RDS Instance
```powershell
aws rds create-db-instance `
  --db-instance-identifier pickup-soccer-db `
  --db-instance-class db.t3.micro `
  --engine postgres `
  --master-username admin `
  --master-user-password YourPassword123! `
  --allocated-storage 20 `
  --publicly-accessible `
  --vpc-security-group-ids sg-xxx
```

### Update Application
```python
# In src/config.py, add:
import os
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://admin:password@endpoint/pickup_soccer')

# Then use SQLAlchemy instead of Parquet
```

## Environment Variables

Set in ECS Task Definition or via Systems Manager Parameter Store:
```powershell
aws ssm put-parameter --name /pickup-soccer/java-home --value "/opt/java/openjdk" --type String
aws ssm put-parameter --name /pickup-soccer/database-url --value "postgresql://..." --type SecureString
```

## Auto-Scaling

```powershell
# Create auto-scaling target
aws application-autoscaling register-scalable-target `
  --service-namespace ecs `
  --resource-id service/pickup-soccer-cluster/api `
  --scalable-dimension ecs:service:DesiredCount `
  --min-capacity 1 `
  --max-capacity 10

# Create scaling policy (CPU-based)
aws application-autoscaling put-scaling-policy `
  --policy-name cpu-scaling `
  --service-namespace ecs `
  --resource-id service/pickup-soccer-cluster/api `
  --scalable-dimension ecs:service:DesiredCount `
  --policy-type TargetTrackingScaling `
  --target-tracking-scaling-policy-configuration '{
    "TargetValue": 70.0,
    "PredefinedMetricSpecification": {
      "PredefinedMetricType": "ECSServiceAverageCPUUtilization"
    }
  }'
```

## Monitoring with CloudWatch

View logs and metrics:
```powershell
# View logs
aws logs tail /ecs/pickup-soccer --follow

# Create dashboard (in AWS Console)
# CloudWatch → Dashboards → Create
# Add widgets for: CPU, Memory, Request Count, Response Time
```

## Cost Estimate

### Free Tier (First 12 Months)
- ECS Fargate: First month free
- RDS t3.micro: 750 hours/month free
- ALB: 750 hours/month free
- ECR: 500MB storage free

### After Free Tier (~$30-50/month)
- **ECS Fargate**: ~$20/month (1 vCPU, 2GB RAM)
- **ALB**: ~$20/month (minimal traffic)
- **RDS**: ~$15/month (db.t3.micro)
- **ECR**: ~$1/month (storage)
- **Data Transfer**: ~$5/month

**Cost Optimization**:
- Use Savings Plans (up to 50% off)
- Use Spot Instances for ECS (70% cheaper)
- Stop dev environments when not in use

## CI/CD with GitHub Actions

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to AWS ECS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Login to ECR
        id: ecr-login
        uses: aws-actions/amazon-ecr-login@v1
      
      - name: Build and push image
        env:
          ECR_REGISTRY: ${{ steps.ecr-login.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/pickup-soccer:$IMAGE_TAG .
          docker push $ECR_REGISTRY/pickup-soccer:$IMAGE_TAG
      
      - name: Deploy to ECS
        run: |
          aws ecs update-service --cluster pickup-soccer-cluster --service api --force-new-deployment
```

## Security Best Practices

1. **Use IAM Roles** - Don't hardcode credentials
2. **Private Subnets** - Keep ECS tasks in private subnets
3. **Security Groups** - Restrict access to ALB only
4. **Secrets Manager** - Store database passwords
5. **WAF** - Add Web Application Firewall to ALB

## Custom Domain

1. **Route 53**: Register or transfer domain
2. **Certificate Manager**: Create SSL certificate
3. **ALB**: Add HTTPS listener with certificate
4. **Route 53**: Create A record pointing to ALB

## Troubleshooting

### Task Fails to Start
```powershell
# Check logs
aws logs tail /ecs/pickup-soccer --follow

# Common issues:
# - Not enough memory (increase from 2048 to 4096)
# - Port conflicts (ensure port 8000)
# - Missing environment variables
```

### Can't Access Service
```powershell
# Check security groups allow port 8000 from ALB
# Check target group health checks passing
# Verify ALB listener routes to correct target group
```

## Comparison: AWS vs Railway vs Render

| Feature | AWS ECS | Railway | Render |
|---------|---------|---------|--------|
| Ease of Use | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Cost (small) | $30-50 | $5-10 | $0-7 |
| Scalability | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Control | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Free Tier | 12 months | $5 credit | Unlimited |

## Recommendation

**For This Project**:
- 🥇 **Render.com** - Easiest, free tier, Docker support
- 🥈 **Railway** - Simple, good for prototypes
- 🥉 **AWS Copilot** - If you need enterprise features

**Use AWS ECS when**:
- Need enterprise-grade scalability
- Require fine-grained control
- Have AWS expertise
- Budget > $50/month

---

**Quick Start AWS**: Use Copilot for easiest deployment  
**Best Value**: Render.com free tier  
**Enterprise**: Full AWS ECS setup
