# Grafana Setup Guide for Container Monitoring

Simple guide to monitor your ERP containers with Grafana + cAdvisor.

---

## Access Grafana

**URL:** `http://44.222.79.31:3000`

**Login:**
- Username: `admin`
- Password: `admin`

(You'll be asked to change the password on first login - you can skip this)

---

## Step-by-Step: Monitor Your Containers

### Step 1: Login to Grafana

1. Open browser: `http://44.222.79.31:3000`
2. Login with admin/admin
3. Click "Skip" when asked to change password (or change it if you want)

### Step 2: Add cAdvisor as Data Source

1. Click the **☰ menu** (top left) → **Connections** → **Data sources**
2. Click **"Add data source"**
3. Search for **"Prometheus"** and click it
4. Configure:
   - **Name:** `cAdvisor`
   - **URL:** `http://cadvisor:8080`
5. Scroll down and click **"Save & Test"**
6. You should see: ✅ "Data source is working"

### Step 3: Create Your First Dashboard

1. Click **☰ menu** → **Dashboards**
2. Click **"New"** → **"New Dashboard"**
3. Click **"Add visualization"**
4. Select **"cAdvisor"** as data source

### Step 4: Add Container CPU Usage Panel

In the query editor at the bottom:

1. **Metric:** Type or select: `container_cpu_usage_seconds_total`
2. **Legend:** `{{name}}`
3. Click **"Run queries"** button (top right)

You should see CPU usage graphs for your containers!

**Configure the panel:**
1. On the right side, find **"Panel options"**
2. **Title:** "Container CPU Usage"
3. **Description:** "CPU usage per container"
4. Click **"Apply"** (top right)

### Step 5: Add Container Memory Usage Panel

1. Click **"Add"** → **"Visualization"**
2. Select **"cAdvisor"** as data source
3. **Metric:** `container_memory_usage_bytes`
4. **Legend:** `{{name}}`
5. **Panel Title:** "Container Memory Usage"
6. Click **"Apply"**

### Step 6: Add Network Traffic Panel

1. Click **"Add"** → **"Visualization"**
2. Select **"cAdvisor"** as data source
3. **Metric:** `container_network_receive_bytes_total`
4. **Legend:** `{{name}} - Received`
5. **Panel Title:** "Network Traffic"
6. Click **"Apply"**

### Step 7: Save Your Dashboard

1. Click the **💾 Save** icon (top right)
2. **Dashboard name:** "ERP Container Monitoring"
3. Click **"Save"**

---

## Quick Metrics Reference

Here are the most useful cAdvisor metrics:

### CPU Metrics
```
container_cpu_usage_seconds_total          # Total CPU usage
container_cpu_system_seconds_total         # System CPU
container_cpu_user_seconds_total           # User CPU
```

### Memory Metrics
```
container_memory_usage_bytes               # Current memory usage
container_memory_max_usage_bytes           # Maximum memory used
container_memory_cache                     # Cache memory
container_memory_rss                       # Resident memory
```

### Network Metrics
```
container_network_receive_bytes_total      # Bytes received
container_network_transmit_bytes_total     # Bytes sent
container_network_receive_packets_total    # Packets received
container_network_transmit_packets_total   # Packets sent
```

### Filesystem Metrics
```
container_fs_usage_bytes                   # Filesystem usage
container_fs_limit_bytes                   # Filesystem limit
container_fs_reads_bytes_total             # Bytes read
container_fs_writes_bytes_total            # Bytes written
```

---

## Import a Pre-built Dashboard (Easy Way!)

Instead of creating panels manually, you can import a ready-made dashboard:

1. Click **☰ menu** → **Dashboards**
2. Click **"New"** → **"Import"**
3. Enter this dashboard ID: **14282**
   (This is "Docker Container & Host Metrics" from grafana.com)
4. Click **"Load"**
5. Select **"cAdvisor"** as the data source
6. Click **"Import"**

You'll instantly have a professional dashboard with:
- Container CPU usage
- Memory usage
- Network traffic
- Disk I/O
- Running containers count

---

## What Each Container Shows

When viewing your dashboard, you'll see metrics for:

- **erp-sistem-backend-1** - Your Flask API container
- **erp-sistem-frontend-1** - Your Nginx frontend container
- **erp-sistem-cadvisor-1** - cAdvisor itself (the metrics collector)
- **erp-sistem-grafana-1** - Grafana itself

---

## Useful Dashboard Features

### Time Range
- Click the time range (top right) to change: Last 5m, 15m, 1h, 6h, 24h, etc.
- Click **🔄 Refresh** to update data

### Zoom In
- Click and drag on any graph to zoom into that time period
- Click **"Zoom out"** to return

### Auto-Refresh
- Click the refresh icon → Select auto-refresh interval (5s, 10s, 30s, 1m, etc.)

### Export/Share
- Click **Share** icon to get dashboard link
- Click **Export** to download as JSON

---

## Troubleshooting

### "No data" in graphs

**Check cAdvisor is running:**
```bash
ssh -i ~/.ssh/erp-key.pem ec2-user@44.222.79.31
docker ps | grep cadvisor
```

**Check cAdvisor directly:**
Open: `http://44.222.79.31:8081`
If you see metrics there, cAdvisor is working.

**Check data source connection:**
1. Go to **Connections** → **Data sources** → **cAdvisor**
2. Click **"Save & Test"**
3. Should see ✅ "Data source is working"

### Graphs show strange values

**For memory:** Use `container_memory_usage_bytes` and format as **Bytes**
- In panel → **Standard options** → **Unit** → **Data (IEC)** → **bytes(IEC)**

**For CPU:** Use rate function:
```
rate(container_cpu_usage_seconds_total[1m])
```

---

## Demo Tips for Your Presentation

1. **Start with the overview:**
   - Show the main dashboard with all containers
   - Point out the backend and frontend containers

2. **Explain what you're monitoring:**
   - CPU usage shows application load
   - Memory shows if containers have enough RAM
   - Network shows API traffic (requests/responses)

3. **Interact with your app:**
   - Open your ERP frontend: `http://44.222.79.31`
   - Add some products
   - Go back to Grafana - show the network traffic spike!
   - Show CPU usage increase during requests

4. **Highlight the benefits:**
   - Real-time monitoring
   - Can detect performance issues
   - Track resource usage
   - Historical data for analysis

---

## Simple Dashboard Layout for Presentation

Here's a good layout for your demo:

**Row 1 - Overview:**
- Panel: Running Containers (Stat visualization)

**Row 2 - Resource Usage:**
- Panel: CPU Usage (Time series graph)
- Panel: Memory Usage (Time series graph)

**Row 3 - Network:**
- Panel: Network Traffic (Time series graph, showing both RX and TX)

**Row 4 - Application Specific:**
- Panel: Backend Container CPU (single container focus)
- Panel: Frontend Container CPU (single container focus)

---

## Access URLs

**Grafana Dashboard:**
```
http://44.222.79.31:3000
```

**cAdvisor (raw metrics):**
```
http://44.222.79.31:8081
```

**Your ERP Application:**
```
Frontend: http://44.222.79.31
Backend:  http://44.222.79.31:5000/api
```

---

**Last Updated:** November 30, 2025
**Status:** ✅ Grafana + cAdvisor monitoring active
