#!/bin/bash
# Manual Deployment Script for ERP System

set -e

# Configuration
EC2_HOST="3.237.106.142"
EC2_USER="ec2-user"
SSH_KEY="$HOME/.ssh/erp-key.pem"

echo "=== ERP System Deployment Script ==="
echo "Deploying to: $EC2_USER@$EC2_HOST"
echo ""

# Check if SSH key exists
if [ ! -f "$SSH_KEY" ]; then
    echo "Error: SSH key not found at $SSH_KEY"
    exit 1
fi

# Check if RDS endpoint is set
read -p "Enter RDS endpoint (or press Enter to skip): " RDS_ENDPOINT
read -p "Enter Django secret key (or press Enter to use default): " DJANGO_KEY

if [ -z "$DJANGO_KEY" ]; then
    DJANGO_KEY="change-me-in-production"
fi

if [ -z "$RDS_ENDPOINT" ]; then
    echo "Warning: No RDS endpoint provided. Make sure to set it manually on EC2."
    RDS_ENDPOINT="your-rds-endpoint"
fi

echo ""
echo "Connecting to EC2 and deploying..."

ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$EC2_USER@$EC2_HOST" bash -s << EOF
set -e

echo "=== Starting deployment on EC2 ==="

# Create app directory
mkdir -p ~/erp-app
cd ~/erp-app

# Clone or update repository
if [ -d "Devops_Project" ]; then
    echo "Updating existing repository..."
    cd Devops_Project
    git pull origin main
else
    echo "Cloning repository..."
    git clone https://github.com/Leandr0Ms/Devops_Project.git
    cd Devops_Project
fi

cd erp-sistem

# Create .env file
echo "Creating production environment file..."
cat > .env << 'ENVFILE'
SECRET_KEY=${DJANGO_KEY}
ALLOWED_HOSTS=${EC2_HOST},localhost,127.0.0.1,backend,frontend
POSTGRES_DB=erpdb
POSTGRES_USER=erpuser
POSTGRES_PASSWORD=ErpPassword123!
DB_HOST=${RDS_ENDPOINT}
DB_PORT=5432
ENVFILE

# Stop existing containers
echo "Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down || true

# Build images
echo "Building Docker images..."
docker-compose -f docker-compose.prod.yml build --no-cache

# Start containers
echo "Starting containers..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for containers to start
echo "Waiting for containers to start..."
sleep 10

# Show running containers
echo "Running containers:"
docker ps

echo ""
echo "=== Deployment completed successfully! ==="
echo "Application URL: http://${EC2_HOST}"
EOF

echo ""
echo "=== Deployment finished! ==="
echo "You can access your application at: http://$EC2_HOST"
echo ""
echo "To view logs, run:"
echo "  ssh -i $SSH_KEY $EC2_USER@$EC2_HOST 'cd ~/erp-app/Devops_Project/erp-sistem && docker-compose -f docker-compose.prod.yml logs -f'"
