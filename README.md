# DevOps Project - ERP System Deployment

College project demonstrating DevOps practices with Docker, AWS, and CI/CD.

## Project Overview

This project deploys a full-stack ERP system to AWS using:
- **Frontend**: React + Vite + Material UI
- **Backend**: Django REST Framework
- **Database**: PostgreSQL on AWS RDS
- **Infrastructure**: AWS EC2 with Docker
- **CI/CD**: GitHub Actions

## Architecture

```
┌─────────────┐
│   GitHub    │
│  (Source)   │
└──────┬──────┘
       │
       │ push to main
       ▼
┌─────────────┐
│   GitHub    │
│   Actions   │  (CI/CD Pipeline)
└──────┬──────┘
       │
       │ deploy
       ▼
┌─────────────┐     ┌─────────────┐
│     EC2     │────▶│     RDS     │
│   Docker    │     │ PostgreSQL  │
├─────────────┤     └─────────────┘
│  Frontend   │
│  Backend    │
└─────────────┘
```

## AWS Resources Created

### 1. RDS Database
- **Identifier**: `erp-database`
- **Engine**: PostgreSQL 16.6
- **Instance**: db.t3.micro
- **Database**: erpdb
- **Username**: erpuser
- **Password**: ErpPassword123!
- **Status**: Creating (check AWS Console)

### 2. EC2 Instance
- **Name**: erp-server
- **Type**: t3.micro
- **IP**: 3.237.106.142
- **OS**: Amazon Linux 2023
- **Software**: Docker, Docker Compose, Git

### 3. Security Groups
- **RDS SG** (sg-08eaa1456543842ea): Allows port 5432 from EC2
- **EC2 SG** (sg-086ff2df49a41bdb8): Allows ports 80 (HTTP), 22 (SSH)

## Setup Instructions

### Step 1: Wait for RDS to be Ready

The RDS database is currently being created. Check its status:

\`\`\`bash
export AWS_PROFILE=personal
aws rds describe-db-instances --db-instance-identifier erp-database --query 'DBInstances[0].[DBInstanceStatus,Endpoint.Address]' --output text
\`\`\`

Wait until status shows `available` and you see the endpoint address.

### Step 2: Configure GitHub Secrets

Go to your GitHub repository settings → Secrets and variables → Actions, and add these secrets:

1. **EC2_SSH_KEY**: Content of `~/.ssh/erp-key.pem` (your EC2 private key)
   \`\`\`bash
   cat ~/.ssh/erp-key.pem
   \`\`\`

2. **DJANGO_SECRET_KEY**: A secure random key
   \`\`\`bash
   python3 -c "import secrets; print(secrets.token_urlsafe(50))"
   \`\`\`

3. **DB_PASSWORD**: `ErpPassword123!`

4. **DB_HOST**: The RDS endpoint (get it from Step 1)

### Step 3: Test SSH Connection to EC2

\`\`\`bash
ssh -i ~/.ssh/erp-key.pem ec2-user@3.237.106.142
\`\`\`

Verify Docker is installed:
\`\`\`bash
docker --version
docker-compose --version
\`\`\`

### Step 4: Deploy the Application

#### Option A: Using GitHub Actions (Recommended)

1. Commit and push your changes to the `main` branch:
   \`\`\`bash
   git add .
   git commit -m "Initial DevOps setup"
   git push origin main
   \`\`\`

2. GitHub Actions will automatically deploy to EC2

3. Check the Actions tab on GitHub to see the deployment progress

#### Option B: Manual Deployment

1. SSH into EC2:
   \`\`\`bash
   ssh -i ~/.ssh/erp-key.pem ec2-user@3.237.106.142
   \`\`\`

2. Clone the repository:
   \`\`\`bash
   git clone https://github.com/Leandr0Ms/Devops_Project.git
   cd Devops_Project/erp-sistem
   \`\`\`

3. Create `.env` file with production values:
   \`\`\`bash
   cat > .env << 'EOF'
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=3.237.106.142,localhost,backend,frontend
   POSTGRES_DB=erpdb
   POSTGRES_USER=erpuser
   POSTGRES_PASSWORD=ErpPassword123!
   DB_HOST=your-rds-endpoint.rds.amazonaws.com
   DB_PORT=5432
   EOF
   \`\`\`

4. Build and start the containers:
   \`\`\`bash
   docker-compose -f docker-compose.prod.yml up -d
   \`\`\`

### Step 5: Access the Application

Once deployed, access your application at:
- **Frontend**: http://3.237.106.142
- **Backend API**: http://3.237.106.142/api/

## Local Development

To run the application locally for testing:

1. Start local database and application:
   \`\`\`bash
   cd erp-sistem
   docker-compose up -d
   \`\`\`

2. Access locally:
   - Frontend: http://localhost
   - Backend: http://localhost:8000

## Project Requirements Checklist

- ✅ Application with GET and POST using JSON
- ✅ Backend and Frontend components
- ✅ Database storage and modification
- ✅ Docker containers for all services
- ✅ GIT for source code management
- ✅ Production on AWS (EC2)
- ✅ CI/CD with GitHub Actions for automatic deployment

## File Structure

\`\`\`
Devops_Project/
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD workflow
├── erp-sistem/                 # ERP application
│   ├── backend/                # Django backend
│   │   ├── Dockerfile
│   │   └── ...
│   ├── src/                    # React frontend
│   ├── Dockerfile              # Frontend Dockerfile
│   ├── nginx.conf              # Nginx configuration
│   ├── docker-compose.yml      # Local development
│   └── docker-compose.prod.yml # Production deployment
├── ec2-userdata.sh            # EC2 bootstrap script
└── README.md                  # This file
\`\`\`

## Troubleshooting

### Check EC2 Instance Status
\`\`\`bash
export AWS_PROFILE=personal
aws ec2 describe-instances --instance-ids i-05fa6adb6efaa4b78 --query 'Reservations[0].Instances[0].State.Name'
\`\`\`

### Check RDS Status
\`\`\`bash
export AWS_PROFILE=personal
aws rds describe-db-instances --db-instance-identifier erp-database
\`\`\`

### View Docker Logs on EC2
\`\`\`bash
ssh -i ~/.ssh/erp-key.pem ec2-user@3.237.106.142
cd ~/erp-app/Devops_Project/erp-sistem
docker-compose -f docker-compose.prod.yml logs -f
\`\`\`

### Restart Services
\`\`\`bash
docker-compose -f docker-compose.prod.yml restart
\`\`\`

## Cleanup (When Done)

To avoid AWS charges:

\`\`\`bash
export AWS_PROFILE=personal

# Terminate EC2 instance
aws ec2 terminate-instances --instance-ids i-05fa6adb6efaa4b78

# Delete RDS database
aws rds delete-db-instance --db-instance-identifier erp-database --skip-final-snapshot

# Delete security groups (after instances are terminated)
aws ec2 delete-security-group --group-id sg-086ff2df49a41bdb8
aws ec2 delete-security-group --group-id sg-08eaa1456543842ea

# Delete subnets
aws ec2 delete-subnet --subnet-id subnet-07653f2f12a138a03
aws ec2 delete-subnet --subnet-id subnet-009295eca2622080e

# Delete RDS subnet group
aws rds delete-db-subnet-group --db-subnet-group-name erp-db-subnet-group

# Delete key pair
aws ec2 delete-key-pair --key-name erp-key
\`\`\`

## Support

For questions or issues, check the AWS Console or GitHub Actions logs.
