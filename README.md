# DevOps Project - ERP System

A lightweight ERP (Enterprise Resource Planning) system demonstrating modern DevOps practices with AWS cloud deployment, Docker containerization, and CI/CD automation.

## Project Overview

This project is a full-stack web application built as a college DevOps demonstration, showcasing:
- Cloud infrastructure deployment on AWS
- Containerization with Docker
- Continuous Integration/Continuous Deployment (CI/CD)
- RESTful API design
- Database management with PostgreSQL

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        AWS Cloud                             │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                    EC2 Instance                         │ │
│  │                  (t3.micro - Amazon Linux 2023)         │ │
│  │                                                          │ │
│  │  ┌──────────────┐          ┌──────────────┐            │ │
│  │  │   Frontend   │          │   Backend    │            │ │
│  │  │   (Nginx)    │   ◄────► │   (Flask)    │            │ │
│  │  │   Port 80    │          │   Port 5000  │            │ │
│  │  └──────────────┘          └──────────────┘            │ │
│  │         │                         │                     │ │
│  │         └─────────────┬───────────┘                     │ │
│  │                       │                                 │ │
│  └───────────────────────┼─────────────────────────────────┘ │
│                          │                                   │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                  RDS PostgreSQL                         │ │
│  │                  (db.t3.micro)                          │ │
│  │                  Database: erpdb                        │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Frontend
- **Framework**: Vanilla JavaScript (no build process)
- **Web Server**: Nginx (Alpine Linux)
- **UI**: Responsive HTML5 with embedded CSS
- **Features**: Product management interface with real-time updates

### Backend
- **Framework**: Flask (Python 3.11)
- **API**: RESTful JSON API
- **Server**: Gunicorn with 2 workers
- **CORS**: Flask-CORS for cross-origin requests

### Database
- **Engine**: PostgreSQL 16.6
- **Service**: AWS RDS (Relational Database Service)
- **Driver**: psycopg2-binary

### Infrastructure
- **Cloud Provider**: Amazon Web Services (AWS)
- **Compute**: EC2 t3.micro instance
- **Database**: RDS PostgreSQL db.t3.micro
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Version Control**: Git & GitHub

## 🌐 Accessing the Application

### Live Application URLs

**Frontend (Web Interface)**
```
http://44.222.79.31
```
Open this URL in your browser to access the product management interface.

**Backend API**
```
http://44.222.79.31:5000/api
```

### Quick Demo

1. **Open the web interface**: Visit http://44.222.79.31 in your browser
2. **Add a product**: Fill in the form with:
   - Product Name: e.g., "Laptop"
   - Price: e.g., "999.99"
   - Quantity: e.g., "5"
3. **Click "Add Product"** - The product will be saved to the database
4. **View products**: The table below automatically updates showing all products

## Features

### Product Management
- **Create Products**: Add new products with name, price, and quantity
- **View Products**: List all products in a responsive table
- **Real-time Updates**: Automatic UI refresh after operations
- **Health Monitoring**: System health check endpoint
- **Database Persistence**: All data stored in AWS RDS PostgreSQL

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information and available endpoints |
| GET | `/api/health` | Health check (database connectivity) |
| GET | `/api/products` | Retrieve all products |
| POST | `/api/products` | Create a new product |

## Testing the API

You can test the API directly using curl commands:

**Health Check:**
```bash
curl http://44.222.79.31:5000/api/health
```
Expected response: `{"database":"connected","status":"healthy"}`

**Get All Products:**
```bash
curl http://44.222.79.31:5000/api/products
```

**Create a Product:**
```bash
curl -X POST http://44.222.79.31:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "price": 999.99,
    "quantity": 5
  }'
```

## Project Structure

```
Devops_Project/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD pipeline
├── erp-sistem/
│   ├── backend/
│   │   ├── app.py              # Flask application
│   │   ├── requirements.txt    # Python dependencies
│   │   └── Dockerfile          # Backend container image
│   ├── frontend/
│   │   ├── index.html          # Single-page application
│   │   └── Dockerfile          # Frontend container image
│   ├── docker-compose.yml      # Container orchestration
│   └── .env                    # Environment variables
└── README.md                   # This file
```

## AWS Infrastructure Details

### EC2 Instance
- **Instance Type**: t3.micro
- **OS**: Amazon Linux 2023
- **Instance ID**: i-05fa6adb6efaa4b78
- **Public IP**: 44.222.79.31
- **Region**: us-east-1 (N. Virginia)
- **Storage**: 8 GB gp2 EBS volume

### Security Groups
- **SSH (Port 22)**: Open to 0.0.0.0/0 for management
- **HTTP (Port 80)**: Open to 0.0.0.0/0 for frontend
- **Backend API (Port 5000)**: Open to 0.0.0.0/0 for API access
- **RDS (Port 5432)**: Only accessible from EC2 security group

### RDS Database
- **Engine**: PostgreSQL 16.6
- **Instance Class**: db.t3.micro
- **Endpoint**: erp-database.ci5goy2mgeul.us-east-1.rds.amazonaws.com
- **Database Name**: erpdb
- **Username**: erpuser
- **Allocated Storage**: 20 GB
- **Backup Retention**: 7 days

## Deployment Overview

### What Was Done

1. **AWS Infrastructure Setup**
   - Created VPC with public subnets across 2 availability zones
   - Configured internet gateway and route tables
   - Set up security groups with appropriate firewall rules
   - Launched EC2 t3.micro instance with Amazon Linux 2023
   - Created RDS PostgreSQL database instance
   - Configured RDS subnet group for multi-AZ support

2. **Docker Configuration**
   - Created optimized Dockerfile for Flask backend (Python 3.11-slim)
   - Created lightweight Dockerfile for frontend (nginx:alpine)
   - Configured docker-compose.yml for container orchestration
   - Set up environment variables for database connection

3. **Application Development**
   - Built RESTful API with Flask
   - Implemented CRUD operations for products
   - Created responsive frontend with vanilla JavaScript
   - Integrated frontend with backend API
   - Set up database schema and migrations

4. **CI/CD Pipeline**
   - Configured GitHub Actions workflow
   - Set up automated deployment on push to main branch
   - Implemented SSH-based deployment to EC2

### Deployment Process

#### Automated Deployment (CI/CD)
The project uses GitHub Actions for continuous deployment:

1. Push code to the `main` branch on GitHub
2. GitHub Actions workflow automatically triggers
3. Connects to EC2 instance via SSH
4. Pulls latest code from repository
5. Builds Docker images
6. Starts/restarts containers
7. Application is live!

#### Manual Deployment

**Prerequisites:**
- AWS account with EC2 and RDS access
- SSH key pair for EC2 access
- Docker and Docker Compose installed on EC2

**Steps:**

1. **SSH into EC2:**
   ```bash
   ssh -i ~/.ssh/erp-key.pem ec2-user@44.222.79.31
   ```

2. **Clone Repository:**
   ```bash
   git clone https://github.com/Leandr0Ms/Devops_Project.git
   cd Devops_Project/erp-sistem
   ```

3. **Build Docker Images:**
   ```bash
   docker build -t erp-sistem-backend:latest ./backend
   docker build -t erp-sistem-frontend:latest ./frontend
   ```

4. **Start Services:**
   ```bash
   docker-compose up -d
   ```

5. **Initialize Database (First Time Only):**
   ```bash
   docker exec erp-sistem-backend-1 python3 -c "from app import init_db; init_db()"
   ```

6. **Verify Deployment:**
   ```bash
   docker ps
   docker-compose logs
   ```

## Environment Variables

The application uses the following environment variables (stored in `.env`):

```bash
# Database Configuration
DB_HOST=erp-database.ci5goy2mgeul.us-east-1.rds.amazonaws.com
POSTGRES_DB=erpdb
POSTGRES_USER=erpuser
POSTGRES_PASSWORD=ErpPassword123!
DB_PORT=5432
```

## Database Schema

### Products Table
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Docker Configuration

### Backend Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "2", "app:app"]
```

### Frontend Dockerfile
```dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose Configuration
```yaml
services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - DB_HOST=${DB_HOST}
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - DB_PORT=5432
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
```

## Monitoring and Logs

### View Container Status
```bash
ssh -i ~/.ssh/erp-key.pem ec2-user@44.222.79.31 'docker ps'
```

### View Backend Logs
```bash
ssh -i ~/.ssh/erp-key.pem ec2-user@44.222.79.31 'docker-compose -f ~/erp-app/Devops_Project/erp-sistem/docker-compose.yml logs backend --tail=50'
```

### View Frontend Logs
```bash
ssh -i ~/.ssh/erp-key.pem ec2-user@44.222.79.31 'docker-compose -f ~/erp-app/Devops_Project/erp-sistem/docker-compose.yml logs frontend --tail=50'
```

### Check System Health
```bash
# Check if services are running
docker ps

# Check backend health
curl http://44.222.79.31:5000/api/health

# Check frontend
curl -I http://44.222.79.31
```

## Project Evolution

This project underwent significant optimization to work within the constraints of AWS free-tier resources:

### Initial Version (Replaced)
- Django REST Framework backend
- React + Vite frontend
- Complex build process with 11,731+ modules
- **Issue**: Build process overwhelmed t3.micro instance (1 GB RAM)

### Current Version (Optimized)
- Flask backend (minimal dependencies: 4 packages)
- Static HTML frontend (no build required)
- Lightweight Docker images
- **Result**: Successfully runs on t3.micro without performance issues

### Key Optimizations
1. Replaced Django with Flask - 10x smaller memory footprint
2. Removed Vite build process - no node_modules needed
3. Used nginx:alpine for frontend - 5 MB base image
4. Used python:3.11-slim for backend - minimal system dependencies

## Key DevOps Practices Demonstrated

1. **Infrastructure as Code**: AWS resources configured via AWS CLI
2. **Containerization**: All services run in isolated Docker containers
3. **Orchestration**: Docker Compose manages multi-container application
4. **CI/CD**: Automated deployment via GitHub Actions
5. **Cloud Services**: Leveraging AWS EC2 and RDS
6. **Version Control**: Git for source code management
7. **Security**: Environment variables for sensitive data, security groups for network isolation
8. **Monitoring**: Health check endpoints and centralized logging
9. **Resource Optimization**: Lightweight images and minimal dependencies

## Project Requirements Checklist

- ✅ **Application with GET and POST using JSON**: RESTful API with JSON payloads
- ✅ **Backend and Frontend**: Flask backend + HTML/JS frontend
- ✅ **Database storage and modification**: PostgreSQL on RDS with CRUD operations
- ✅ **Docker containers**: All services containerized
- ✅ **GIT for source control**: Hosted on GitHub
- ✅ **Production on AWS**: Deployed on EC2 with RDS database
- ✅ **CI/CD**: GitHub Actions for automatic deployment

## Troubleshooting

### Issue: Cannot access application
**Solution**: Check if EC2 instance is running and security groups allow traffic
```bash
aws ec2 describe-instances --profile personal --region us-east-1 --instance-ids i-05fa6adb6efaa4b78 --query 'Reservations[0].Instances[0].State.Name'
```

### Issue: Database connection fails
**Solution**: Verify RDS instance is available and security groups allow EC2 to connect
```bash
curl http://44.222.79.31:5000/api/health
```

### Issue: IP address changed
**Solution**: EC2 public IPs change when instance stops/starts. Get current IP:
```bash
aws ec2 describe-instances --profile personal --region us-east-1 --instance-ids i-05fa6adb6efaa4b78 --query 'Reservations[0].Instances[0].PublicIpAddress' --output text
```

### Issue: Products table doesn't exist
**Solution**: Initialize the database:
```bash
ssh -i ~/.ssh/erp-key.pem ec2-user@44.222.79.31 'docker exec erp-sistem-backend-1 python3 -c "from app import init_db; init_db()"'
```

### Issue: Containers not running
**Solution**: Check container status and restart if needed:
```bash
ssh -i ~/.ssh/erp-key.pem ec2-user@44.222.79.31 'cd ~/erp-app/Devops_Project/erp-sistem && docker-compose ps && docker-compose restart'
```

## Cost Considerations

This project is designed to run within AWS free tier limits:

- **EC2 t3.micro**: 750 hours/month (free tier)
- **RDS db.t3.micro**: 750 hours/month (free tier)
- **Storage**: 20 GB RDS + 8 GB EC2 (within free tier)
- **Data Transfer**: First 100 GB/month free

**Estimated Monthly Cost (after free tier expires)**: ~$15-20/month

**Cost Optimization Tips:**
- Stop EC2 when not in use (but note: public IP will change)
- Use RDS snapshots instead of keeping instance running 24/7
- Monitor data transfer to stay within free tier limits.

## Future Enhancements

- [ ] Allocate Elastic IP for consistent addressing
- [ ] Implement user authentication and authorization
- [ ] Add product update and delete endpoints
- [ ] Set up CloudWatch monitoring and alerts
- [ ] Implement automated RDS backups and restore procedures
- [ ] Add product categories and search functionality
- [ ] Create admin dashboard with analytics
- [ ] Set up SSL/TLS certificates (HTTPS with Let's Encrypt)
- [ ] Implement caching layer (Redis) for improved performance
- [ ] Add API rate limiting and request validation
- [ ] Set up log aggregation (CloudWatch Logs)
- [ ] Implement blue-green deployment strategy

## Repository

**GitHub**: https://github.com/Leandr0Ms/Devops_Project

## License

This project is created for educational purposes as part of a college DevOps course.

---

**Last Updated**: November 30, 2025
**Deployment Status**: ✅ Live and Running
**Application URL**: http://44.222.79.31
**API URL**: http://44.222.79.31:5000/api

