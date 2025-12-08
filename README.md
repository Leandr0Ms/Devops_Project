# DevOps Project - ERP System

A lightweight ERP (Enterprise Resource Planning) system demonstrating modern DevOps practices with AWS cloud deployment, Docker containerization, HTTPS/SSL, and CI/CD automation.

## Project Overview

This project is a full-stack web application built as a college DevOps demonstration, showcasing:
- Cloud infrastructure deployment on AWS
- Containerization with Docker
- Nginx reverse proxy with SSL/TLS
- Continuous Integration/Continuous Deployment (CI/CD)
- RESTful API design
- Database management with PostgreSQL
- Monitoring with Grafana and Prometheus

## Architecture

```
                        Internet (HTTPS/HTTP)
                                 │
                                 ▼
                    ┌────────────────────────────┐
                    │   No-IP Dynamic DNS        │
                    │  desafio-devops.ddns.net   │
                    └────────────────────────────┘
                                 │
┌────────────────────────────────▼──────────────────────────────┐
│                          AWS Cloud                             │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              EC2 Instance (Amazon Linux 2023)             │ │
│  │                                                            │ │
│  │  ┌────────────────────────────────────────────────┐      │ │
│  │  │         Nginx Reverse Proxy (Port 80/443)      │      │ │
│  │  │              with Let's Encrypt SSL            │      │ │
│  │  └───────────┬─────────────────┬──────────────────┘      │ │
│  │              │                 │                          │ │
│  │              ▼                 ▼                          │ │
│  │    ┌──────────────┐   ┌──────────────┐                  │ │
│  │    │  Frontend    │   │   Backend    │                  │ │
│  │    │  (Docker)    │   │   (Docker)   │                  │ │
│  │    │  Port 8080   │   │  Port 5000   │                  │ │
│  │    └──────────────┘   └──────┬───────┘                  │ │
│  │                              │                           │ │
│  │    ┌──────────────┐   ┌──────────────┐                  │ │
│  │    │   Grafana    │   │  Prometheus  │                  │ │
│  │    │  Port 3000   │   │  Port 9090   │                  │ │
│  │    └──────────────┘   └──────────────┘                  │ │
│  │                                                            │ │
│  └────────────────────────────┬───────────────────────────────┘ │
│                               │                                 │
│                               ▼                                 │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │              RDS PostgreSQL (db.t3.micro)                 │ │
│  │                  Database: erpdb                          │ │
│  └──────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 🌐 Accessing the Application

### Live Application URLs

**Main Application (HTTPS)**
```
https://desafio-devops.ddns.net
```
- Frontend web interface for product management
- Secured with Let's Encrypt SSL certificate
- Automatically redirects HTTP to HTTPS

**Backend API (via Nginx Proxy)**
```
https://desafio-devops.ddns.net/api
```
- RESTful API endpoints
- Proxied through Nginx to backend container

**Monitoring Services (Direct Access)**
```
Grafana:     http://desafio-devops.ddns.net:3000  (admin/admin)
Prometheus:  http://desafio-devops.ddns.net:9090  (no login)
cAdvisor:    http://desafio-devops.ddns.net:8081  (no login)
```

**Alternative Access (Direct IP)**
```
Frontend:    http://44.222.79.31
Grafana:     http://44.222.79.31:3000
Prometheus:  http://44.222.79.31:9090
cAdvisor:    http://44.222.79.31:8081
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
- **Reverse Proxy**: Nginx with SSL/TLS (Let's Encrypt)
- **DNS**: No-IP Dynamic DNS (desafio-devops.ddns.net)
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Version Control**: Git & GitHub
- **Monitoring**: Grafana, Prometheus, cAdvisor

## 🚀 Important Commands

### SSH Access to EC2

```bash
ssh -i your-key.pem ec2-user@44.222.79.31
```

### Docker Management

**View running containers:**
```bash
docker ps
```

**View all containers (including stopped):**
```bash
docker ps -a
```

**Check container logs:**
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend

# Follow logs in real-time
docker-compose logs -f backend
```

**Restart containers:**
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
docker-compose restart frontend
```

**Stop all containers:**
```bash
docker-compose down
```

**Start containers:**
```bash
docker-compose up -d
```

**Rebuild and restart after code changes:**
```bash
cd ~/erp-app/Devops_Project/erp-sistem
git pull
docker-compose up -d --build
```

**View resource usage:**
```bash
docker stats
```

### Nginx Management

**Test Nginx configuration:**
```bash
sudo nginx -t
```

**Reload Nginx (apply config changes):**
```bash
sudo systemctl reload nginx
```

**Restart Nginx:**
```bash
sudo systemctl restart nginx
```

**Check Nginx status:**
```bash
sudo systemctl status nginx
```

**View Nginx error logs:**
```bash
sudo tail -f /var/log/nginx/error.log
```

**View Nginx access logs:**
```bash
sudo tail -f /var/log/nginx/access.log
```

**Edit Nginx configuration:**
```bash
sudo nano /etc/nginx/conf.d/erp.conf
```

### SSL Certificate Management

**Check certificate expiration:**
```bash
sudo certbot certificates
```

**Renew SSL certificate manually:**
```bash
sudo certbot renew
sudo systemctl reload nginx
```

**Test auto-renewal:**
```bash
sudo certbot renew --dry-run
```

**Force certificate renewal:**
```bash
sudo certbot renew --force-renewal
```

### System Monitoring

**Check system resources:**
```bash
# CPU and memory usage
top

# Disk usage
df -h

# Memory usage
free -h
```

**Check Docker disk usage:**
```bash
docker system df
```

**Clean up Docker resources:**
```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Clean everything
docker system prune -a
```

### Application Health Checks

**Backend health check:**
```bash
curl http://localhost:5000/api/health
```

**Frontend check:**
```bash
curl -I http://localhost:8080
```

**Check through Nginx:**
```bash
curl http://localhost/api/health
```

**Check HTTPS:**
```bash
curl -I https://desafio-devops.ddns.net
```

### Database Operations

**Initialize database:**
```bash
docker exec -it erp-sistem-backend-1 python3 -c "from app import init_db; init_db()"
```

**Test database connection:**
```bash
curl http://localhost:5000/api/health
```

### Git Operations

**Pull latest changes:**
```bash
cd ~/erp-app/Devops_Project
git pull origin main
```

**Check current branch:**
```bash
git branch
```

**View recent commits:**
```bash
git log --oneline -10
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information and available endpoints |
| GET | `/api/health` | Health check (database connectivity) |
| GET | `/api/products` | Retrieve all products |
| POST | `/api/products` | Create a new product |

## Testing the API

**Health Check:**
```bash
curl https://desafio-devops.ddns.net/api/health
```
Expected response: `{"database":"connected","status":"healthy"}`

**Get All Products:**
```bash
curl https://desafio-devops.ddns.net/api/products
```

**Create a Product:**
```bash
curl -X POST https://desafio-devops.ddns.net/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "price": 999.99,
    "quantity": 5
  }'
```

## AWS Infrastructure Details

### EC2 Instance
- **Instance Type**: t3.micro
- **OS**: Amazon Linux 2023
- **Instance ID**: i-05fa6adb6efaa4b78
- **Public IP**: 44.222.79.31
- **Domain**: desafio-devops.ddns.net
- **Region**: us-east-1 (N. Virginia)
- **Storage**: 8 GB gp2 EBS volume

### Security Groups
- **SSH (Port 22)**: Open to 0.0.0.0/0 for management
- **HTTP (Port 80)**: Open to 0.0.0.0/0 (redirects to HTTPS)
- **HTTPS (Port 443)**: Open to 0.0.0.0/0 for secure access
- **Grafana (Port 3000)**: Open to 0.0.0.0/0 for dashboards
- **Backend API (Port 5000)**: Internal only (proxied via Nginx)
- **Frontend (Port 8080)**: Internal only (proxied via Nginx)
- **Prometheus (Port 9090)**: Open to 0.0.0.0/0 for metrics
- **cAdvisor (Port 8081)**: Open to 0.0.0.0/0 for container metrics
- **RDS (Port 5432)**: Only accessible from EC2 security group

### RDS Database
- **Engine**: PostgreSQL 16.6
- **Instance Class**: db.t3.micro
- **Endpoint**: erp-database.ci5goy2mgeul.us-east-1.rds.amazonaws.com
- **Database Name**: erpdb
- **Username**: erpuser
- **Allocated Storage**: 20 GB
- **Backup Retention**: 7 days

## Deployment Process

### Automated Deployment (CI/CD)

The project uses GitHub Actions for continuous deployment:

1. Push code to the `main` branch on GitHub
2. GitHub Actions workflow automatically triggers
3. Connects to EC2 instance via SSH
4. Pulls latest code from repository
5. Builds Docker images
6. Starts/restarts containers
7. Application is live!

### Manual Deployment

**On EC2 instance:**

```bash
# Navigate to project directory
cd ~/erp-app/Devops_Project/erp-sistem

# Pull latest code
git pull

# Rebuild and restart containers
docker-compose down
docker-compose up -d --build

# Verify deployment
docker ps
docker-compose logs
```

## Monitoring

### Grafana Dashboards

Access Grafana at `http://desafio-devops.ddns.net:3000`

**Default credentials:** admin / admin

**Available metrics:**
- Container CPU usage
- Container memory usage
- Network traffic (received/transmitted)
- Per-service metrics (backend, frontend)

**Data source:** Prometheus at `http://prometheus:9090`

### Prometheus Metrics

Access Prometheus at `http://desafio-devops.ddns.net:9090`

**Key metrics available:**
- `container_cpu_usage_seconds_total` - CPU usage per container
- `container_memory_usage_bytes` - Memory usage per container
- `container_network_receive_bytes_total` - Network received
- `container_network_transmit_bytes_total` - Network transmitted

**Useful queries:**
```promql
# CPU usage by container
sum by (name) (rate(container_cpu_usage_seconds_total{job="cadvisor"}[1m]))

# Memory usage by container
sum by (name) (container_memory_usage_bytes{job="cadvisor"})

# Backend CPU
rate(container_cpu_usage_seconds_total{container_label_com_docker_compose_service="backend"}[1m])
```

### cAdvisor

Access cAdvisor at `http://desafio-devops.ddns.net:8081`

Provides real-time container metrics and performance data.

## Troubleshooting

### Application not accessible

**Check Nginx:**
```bash
sudo systemctl status nginx
sudo nginx -t
```

**Check containers:**
```bash
docker ps
docker-compose logs
```

### SSL certificate issues

**Check certificate status:**
```bash
sudo certbot certificates
```

**Renew if needed:**
```bash
sudo certbot renew
sudo systemctl reload nginx
```

### Backend not responding

**Check backend logs:**
```bash
docker-compose logs backend
```

**Test backend directly:**
```bash
curl http://localhost:5000/api/health
```

**Restart backend:**
```bash
docker-compose restart backend
```

### Database connection failed

**Test connection:**
```bash
curl http://localhost:5000/api/health
```

**Check environment variables:**
```bash
docker-compose config
```

### Port conflicts

**Check what's using a port:**
```bash
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :443
```

### Out of disk space

**Check disk usage:**
```bash
df -h
docker system df
```

**Clean up Docker:**
```bash
docker system prune -a
docker volume prune
```

## Project Structure

```
Devops_Project/
├── .github/
│   └── workflows/
│       └── deploy.yml              # GitHub Actions CI/CD pipeline
├── erp-sistem/
│   ├── backend/
│   │   ├── app.py                  # Flask application
│   │   ├── requirements.txt        # Python dependencies
│   │   └── Dockerfile              # Backend container image
│   ├── frontend/
│   │   ├── index.html              # Single-page application
│   │   └── Dockerfile              # Frontend container image
│   ├── docker-compose.yml          # Container orchestration
│   ├── prometheus.yml              # Prometheus configuration
│   └── .env                        # Environment variables
├── nginx-erp.conf                  # Nginx reverse proxy config
└── README.md                       # This file
```

## Environment Variables

```bash
# Database Configuration
DB_HOST=erp-database.ci5goy2mgeul.us-east-1.rds.amazonaws.com
POSTGRES_DB=erpdb
POSTGRES_USER=erpuser
POSTGRES_PASSWORD=ErpPassword123!
DB_PORT=5432
```

## Security Features

- ✅ HTTPS/SSL with Let's Encrypt (automatic renewal)
- ✅ HTTP to HTTPS redirect
- ✅ AWS Security Groups for network isolation
- ✅ Environment variables for sensitive data
- ✅ Database in private subnet (RDS)
- ✅ Nginx reverse proxy (hides internal ports)
- ✅ No-IP Dynamic DNS for stable domain access

## Cost Considerations

This project is designed to run within AWS free tier limits:

- **EC2 t3.micro**: 750 hours/month (free tier)
- **RDS db.t3.micro**: 750 hours/month (free tier)
- **Storage**: 20 GB RDS + 8 GB EC2 (within free tier)
- **Data Transfer**: First 100 GB/month free

**Estimated Monthly Cost (after free tier expires)**: ~$15-20/month

## Future Enhancements

- [ ] Implement user authentication and authorization
- [ ] Add product update and delete endpoints
- [ ] Set up CloudWatch monitoring and alerts
- [ ] Add product categories and search functionality
- [ ] Implement caching layer (Redis)
- [ ] Add API rate limiting and request validation
- [ ] Set up log aggregation
- [ ] Implement blue-green deployment strategy
- [ ] Add automated database backups
- [ ] Create admin dashboard with analytics

## Repository

**GitHub**: https://github.com/Leandr0Ms/Devops_Project

## License

This project is created for educational purposes as part of a college DevOps course.

---

**Last Updated**: December 7, 2025
**Deployment Status**: ✅ Live and Running with HTTPS
**Application URL**: https://desafio-devops.ddns.net
**API URL**: https://desafio-devops.ddns.net/api
**Monitoring**: http://desafio-devops.ddns.net:3000 (Grafana)
