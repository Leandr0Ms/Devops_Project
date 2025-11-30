# Monitoring Setup Guide

This document explains how to use the monitoring tools (Zabbix and Grafana) deployed with the ERP system.

---

## Overview

The ERP system includes comprehensive monitoring using:
- **Zabbix**: Environment monitoring (servers, containers, resources)
- **Grafana**: Visualization and dashboards
- **cAdvisor**: Container metrics collection

All monitoring services run in Docker containers alongside the application.

---

## Monitoring Services

### 1. Zabbix

**Zabbix** is an enterprise-class open-source monitoring solution for networks and applications.

**Components:**
- **Zabbix Server**: Core monitoring engine
- **Zabbix Web Interface**: Web-based UI for configuration and viewing
- **Zabbix Agent**: Collects metrics from the host and containers
- **PostgreSQL Database**: Stores Zabbix configuration and monitoring data

**Access Zabbix:**
```
http://44.222.79.31:8080
```

**Default Credentials:**
- Username: `Admin`
- Password: `zabbix`

**What Zabbix Monitors:**
- EC2 instance CPU, memory, disk usage
- Docker containers status and resource usage
- Network traffic
- System processes
- Application availability

### 2. Grafana

**Grafana** provides visualization and dashboards for metrics.

**Access Grafana:**
```
http://44.222.79.31:3000
```

**Default Credentials:**
- Username: `admin`
- Password: `admin`
(You'll be prompted to change this on first login)

**Pre-configured Features:**
- Zabbix plugin installed automatically
- Can connect to Zabbix as data source
- Create custom dashboards for container metrics

### 3. cAdvisor

**cAdvisor** (Container Advisor) provides container resource usage and performance characteristics.

**Access cAdvisor:**
```
http://44.222.79.31:8081
```

**No authentication required.**

**What cAdvisor Shows:**
- Real-time container CPU usage
- Memory usage per container
- Network I/O
- Filesystem usage
- Container metrics history

---

## Quick Start Guide

### Step 1: Access Zabbix

1. Open browser and go to: `http://44.222.79.31:8080`
2. Login with default credentials (Admin/zabbix)
3. Navigate to **Monitoring** > **Hosts** to see monitored servers
4. Check **Monitoring** > **Latest data** to view real-time metrics

### Step 2: Configure Grafana

1. Open browser and go to: `http://44.222.79.31:3000`
2. Login with admin/admin (change password when prompted)
3. Go to **Configuration** > **Data Sources**
4. Click **Add data source**
5. Select **Zabbix**
6. Configure:
   - URL: `http://zabbix-web:8080/api_jsonrpc.php`
   - Username: `Admin`
   - Password: `zabbix`
7. Click **Save & Test**

### Step 3: Add cAdvisor to Grafana

1. In Grafana, go to **Configuration** > **Data Sources**
2. Click **Add data source**
3. Select **Prometheus** (cAdvisor exports Prometheus-compatible metrics)
4. Configure:
   - URL: `http://cadvisor:8080`
5. Click **Save & Test**

### Step 4: Create Your First Dashboard

1. In Grafana, click **+** > **Dashboard**
2. Click **Add new panel**
3. Select **Zabbix** as data source
4. Choose metrics to visualize:
   - CPU usage
   - Memory usage
   - Network traffic
   - Container stats
5. Customize visualization type (graph, gauge, table, etc.)
6. Click **Apply** and **Save**

---

## Monitoring Docker Containers

### Using Zabbix

**Monitor Container Status:**
1. Login to Zabbix web interface
2. Navigate to **Configuration** > **Hosts**
3. You should see "ERP-Server" host
4. Click on the host to configure monitoring items

**Add Docker Container Monitoring:**
1. Go to **Configuration** > **Hosts** > **ERP-Server**
2. Click **Items** tab
3. Click **Create item**
4. Configure to monitor Docker metrics using Zabbix Agent

### Using cAdvisor

**View Container Metrics:**
1. Open `http://44.222.79.31:8081`
2. Click on **Docker Containers** in the left sidebar
3. Select a container to view detailed metrics:
   - erp-sistem-backend-1
   - erp-sistem-frontend-1
   - erp-sistem-zabbix-server-1
   - erp-sistem-grafana-1
   - etc.

**Metrics Available:**
- CPU usage (total and per-core)
- Memory usage (current, max, cache)
- Network throughput (TX/RX)
- Filesystem I/O
- Container uptime

### Using Grafana Dashboards

**Create Container Monitoring Dashboard:**
1. In Grafana, create a new dashboard
2. Add panels for:
   - Container CPU usage
   - Container memory usage
   - Network I/O
   - Disk I/O
3. Use cAdvisor as data source
4. Save dashboard as "ERP Containers"

---

## Common Monitoring Tasks

### Check if All Containers are Running

**Via cAdvisor:**
- Go to `http://44.222.79.31:8081/docker/`
- View list of running containers

**Via SSH:**
```bash
ssh -i ~/.ssh/erp-key.pem ec2-user@44.222.79.31
cd ~/erp-app/Devops_Project/erp-sistem
docker-compose ps
```

### Monitor Application Performance

**Backend API Response Time:**
1. In Zabbix, create a web scenario
2. Configure to check `http://44.222.79.31:5000/api/health`
3. Set up triggers for slow responses

**Frontend Availability:**
1. Create web scenario for `http://44.222.79.31`
2. Monitor HTTP response codes
3. Alert on 4xx or 5xx errors

### Set Up Alerts

**In Zabbix:**
1. Go to **Configuration** > **Hosts** > **ERP-Server**
2. Click **Triggers**
3. Create trigger for high CPU:
   - Name: "High CPU usage"
   - Expression: `{ERP-Server:system.cpu.util[].avg(5m)}>80`
   - Severity: Warning
4. Configure **Actions** to send notifications

**In Grafana:**
1. Edit a panel in your dashboard
2. Click **Alert** tab
3. Configure alert conditions
4. Set up notification channels (email, Slack, etc.)

---

## Accessing Monitoring Services

### All Monitoring URLs

| Service | URL | Default Credentials |
|---------|-----|---------------------|
| Zabbix Web | http://44.222.79.31:8080 | Admin / zabbix |
| Grafana | http://44.222.79.31:3000 | admin / admin |
| cAdvisor | http://44.222.79.31:8081 | No login required |

### Application URLs

| Service | URL |
|---------|-----|
| ERP Frontend | http://44.222.79.31 |
| ERP Backend API | http://44.222.79.31:5000/api |
| API Health Check | http://44.222.79.31:5000/api/health |

---

## Troubleshooting

### Zabbix web interface not accessible

**Check if container is running:**
```bash
docker ps | grep zabbix-web
```

**Check logs:**
```bash
docker-compose -f ~/erp-app/Devops_Project/erp-sistem/docker-compose.yml logs zabbix-web
```

**Restart service:**
```bash
cd ~/erp-app/Devops_Project/erp-sistem
docker-compose restart zabbix-web
```

### Grafana not connecting to Zabbix

**Verify network connectivity:**
1. Check that zabbix-server and grafana are on the same Docker network
2. Use container names (not localhost) in data source configuration
3. Check Zabbix API endpoint: `http://zabbix-web:8080/api_jsonrpc.php`

### cAdvisor showing no data

**Check permissions:**
```bash
docker ps | grep cadvisor
docker logs erp-sistem-cadvisor-1
```

**Restart with correct permissions:**
```bash
cd ~/erp-app/Devops_Project/erp-sistem
docker-compose restart cadvisor
```

### High resource usage

**Check which container is using resources:**
```bash
docker stats
```

**Or via cAdvisor:**
- Open `http://44.222.79.31:8081`
- Check CPU and memory graphs for each container

---

## Docker Compose Configuration

The monitoring stack is defined in `erp-sistem/docker-compose.yml`:

```yaml
services:
  # Zabbix Database
  zabbix-db:
    image: postgres:16-alpine

  # Zabbix Server
  zabbix-server:
    image: zabbix/zabbix-server-pgsql:alpine-7.0-latest
    ports:
      - "10051:10051"

  # Zabbix Web Interface
  zabbix-web:
    image: zabbix/zabbix-web-nginx-pgsql:alpine-7.0-latest
    ports:
      - "8080:8080"

  # Zabbix Agent
  zabbix-agent:
    image: zabbix/zabbix-agent:alpine-7.0-latest

  # cAdvisor
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    ports:
      - "8081:8080"

  # Grafana
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
```

---

## Security Notes

**Change Default Passwords:**
1. **Zabbix**: Change Admin password after first login
2. **Grafana**: System prompts password change on first login

**Firewall Rules:**
- Ports 8080, 3000, 8081 are open to 0.0.0.0/0
- For production, restrict to specific IPs

**Database Credentials:**
- Zabbix DB password is in docker-compose.yml
- Should be moved to environment variables for production

---

## Best Practices

1. **Regular Monitoring**
   - Check dashboards daily
   - Review alerts weekly
   - Analyze trends monthly

2. **Alert Configuration**
   - Set up alerts for critical metrics
   - Avoid alert fatigue (don't over-alert)
   - Test alert notifications

3. **Dashboard Organization**
   - Create separate dashboards for different concerns
   - Use folders to organize dashboards
   - Share dashboards with team members

4. **Data Retention**
   - Configure data retention policies in Zabbix
   - Archive old data periodically
   - Monitor database size

5. **Performance**
   - Monitor the monitoring tools themselves
   - Ensure they don't impact application performance
   - Scale resources if needed

---

## Additional Resources

**Zabbix Documentation:**
- Official Docs: https://www.zabbix.com/documentation/current
- Docker Image: https://hub.docker.com/r/zabbix/zabbix-server-pgsql

**Grafana Documentation:**
- Official Docs: https://grafana.com/docs/
- Dashboards: https://grafana.com/grafana/dashboards/

**cAdvisor:**
- GitHub: https://github.com/google/cadvisor
- Metrics Guide: https://github.com/google/cadvisor/blob/master/docs/storage/prometheus.md

---

**Last Updated**: November 30, 2025
**System Status**: All monitoring services operational
