# ELK Stack Log Analysis Pipeline

A **Elasticsearch, Logstash, Kibana (ELK)** stack implementation for collecting, processing, and analyzing build logs from distributed systems using Filebeat for real-time log shipping.

## 🎯 Project Objective

This project simulates a real-world distributed build system monitoring solution. It:
- **Collects** build logs from multiple sources
- **Ships** logs via Filebeat to Logstash in real-time
- **Processes** and enriches logs with structured parsing and anomaly detection
- **Stores** indexed data in Elasticsearch
- **Visualizes** metrics and patterns through Kibana dashboards

## 🏗️ Architecture

```
┌─────────────────┐
│  Log Files      │  (Build logs from distributed systems)
│  (simulate.py)  │
└────────┬────────┘
         │
┌────────▼────────────────────┐
│   Filebeat                  │  (Log shipping agent)
│   (beats.yml)               │
└────────┬────────────────────┘
         │
┌────────▼────────────────────┐
│   Logstash                  │  (Log processing pipeline)
│   (logstash.conf)           │
│   - Extraction              │
│   - Enrichment              │
│   - Error Detection         │
└────────┬────────────────────┘
         │
┌────────▼────────────────────┐
│  Elasticsearch              │  (Storage & Search)
└────────┬────────────────────┘
         │
┌────────▼────────────────────┐
│   Kibana                    │  (Visualization & Analysis)
│   (Dashboard)               │
└─────────────────────────────┘
```

## 📁 Project Structure

```
.
├── README.md                          # Project documentation
├── docker-compose.yml                 # ELK stack infrastructure
├── simulate.py                        # Log simulator script
├── filebeat/                          # Filebeat configuration
│   └── filebeat.yml                   # Log shipping configuration
├── logstash/                          # Logstash configuration
│   └── logstash.conf                  # Log processing pipeline
├── logs/                              # Output directory (generated)
│   └── *.txt                          # Processed log files
└── logs_data/                         # Input data
    └── OneDrive_1_21-10-2025/
        └── log-2018-06-08/
            └── *.txt                  # Source build logs
```

## 🔧 Components

### 1. **Elasticsearch 7.16.2**
- Central data store and search engine
- Indexes logs with pattern: `test_devoir_2_logs`
- REST API on port `9200`
- Node communication on port `9300`

**Configuration:**
- Single-node cluster
- Memory: 256MB min/max
- Volume: `elastic_data` (persistent)

### 2. **Logstash 7.16.2**
- Log processing and transformation pipeline
- Receives events from Filebeat (port `5044`)
- Pipeline stages:
  - **Input**: Beats protocol
  - **Filter**: Ruby scripts, Grok patterns, Date parsing
  - **Output**: Elasticsearch

**Key Processing Features:**
- Extracts header fields (builder, slave, starttime, etc.)
- Parses exit codes and elapsed times
- Converts Unix timestamps to readable dates
- Detects errors and anomalies
- Filters noise (empty lines, separator lines)

### 3. **Kibana 7.16.2**
- Visualization and analysis dashboard
- Web UI on port `5601`
- Connects to Elasticsearch cluster
- Create custom visualizations and alerts

### 4. **Filebeat**
- Lightweight log shipper
- Reads log files line-by-line
- Sends events to Logstash via `localhost:5044`
- Features:
  - Real-time log detection
  - Line buffering (16KB)
  - Field enrichment
  - Connection pooling

### 5. **Log Simulator** (`simulate.py`)
- Python script to generate synthetic logs
- Reads from `logs_data/` directory
- Writes to `logs/` directory
- Line-by-line output with configurable delays
- Simulates real-time log generation

## 📊 Log Format & Parsing

### Header Fields (Extracted from logs)
```
builder: mozilla-esr52_xp_ix-debug_test-marionette
slave: t-xp32-ix-006
starttime: 1528414102.79
results: success (0)
buildid: 20180607121919
builduid: 0a12ee6f156747b89b67c456d4296829
revision: f18535a212da01cb384259f9b286006d0ae8eb37
```

### Parsed Fields (via Grok)
| Field | Type | Pattern |
|-------|------|---------|
| `exit_code` | integer | "program finished with exit code %{NUMBER}" |
| `elapsed_time` | float | "elapsedTime=%{NUMBER}" |
| `result_status` | string | "results: %{WORD}" |
| `warning_message` | string | "WARNING: %{GREEDYDATA}" |

### Computed Fields
- `is_error`: Boolean (true if result_status ≠ "success")
- `@timestamp`: Converted from Unix timestamp

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.7+
- 4GB RAM minimum

### 1. Start the Stack
```bash
docker-compose up -d
```

Verify all services are running:
```bash
docker-compose ps
```

### 2. Verify Elasticsearch
```bash
curl http://localhost:9200
```

Expected response:
```json
{
  "name": "elasticsearch",
  "cluster_name": "docker-cluster",
  "version": {
    "number": "7.16.2"
  }
}
```

### 3. Run Log Simulation
```bash
python simulate.py
```

This will:
- Read logs from `logs_data/`
- Write to `logs/` directory
- Simulate real-time log generation (0.08s delay per line)

### 4. Monitor in Kibana
Open browser: http://localhost:5601

1. Create index pattern: `test_devoir_2_logs`
2. Explore logs in the Discover tab
3. Create visualizations and dashboards

## 📝 Configuration Details

### Filebeat (`filebeat/filebeat.yml`)
```yaml
inputs:
  - type: log
    paths: ["/var/log/firefox/*.txt"]
    
output.logstash:
  hosts: ["logstash:5044"]
  bulk_max_size: 1
```

### Logstash (`logstash/logstash.conf`)
- **Ruby filter**: Extracts and maintains state across log lines
- **Grok filter**: Parses structured fields
- **Date filter**: Converts starttime to @timestamp
- **Mutate filter**: Type conversions and field enrichment
- **Drop filter**: Removes noise

### Docker Compose Network
- Network: `elk`
- All services communicate via service names (e.g., `elasticsearch:9200`)

## 🔍 Common Tasks

### View Elasticsearch Indices
```bash
curl http://localhost:9200/_cat/indices
```

### Query Logs
```bash
curl http://localhost:9200/test_devoir_2_logs/_search?pretty
```

### Check Logstash Logs
```bash
docker logs logstash
```

### Check Filebeat Logs
```bash
docker logs filebeat
```

### Stop All Services
```bash
docker-compose down
```

### Remove Data & Start Fresh
```bash
docker-compose down -v
docker-compose up -d
```

## 📈 Use Cases

1. **Build System Monitoring**
   - Track build success/failure rates
   - Identify slow builds (elapsed_time analysis)
   - Monitor builder/slave utilization

2. **Error Detection & Alerting**
   - Automatic anomaly detection via `is_error` field
   - Real-time warning extraction
   - Exit code analysis

3. **Performance Analysis**
   - Elapsed time trends
   - Resource utilization patterns
   - Builder efficiency comparison

4. **Audit & Compliance**
   - Build history tracking
   - Revision traceability
   - Execution timeline reconstruction

## 🛠️ Troubleshooting

### Issue: Elasticsearch won't start
```bash
# Check available memory
docker stats elasticsearch

# Increase heap size in docker-compose.yml
ES_JAVA_OPTS: "-Xmx512m -Xms512m"
```

### Issue: No logs appearing in Kibana
1. Check Filebeat is running: `docker logs filebeat`
2. Verify Logstash received data: Check stdout output
3. Confirm logs exist in `logs/` directory

### Issue: Logstash errors
```bash
docker logs logstash -f
```

### Clear All Data
```bash
docker-compose down -v
docker volume rm elasticsearch_elastic_data
```

## 📚 References

- [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/7.16/index.html)
- [Logstash Documentation](https://www.elastic.co/guide/en/logstash/7.16/index.html)
- [Kibana Documentation](https://www.elastic.co/guide/en/kibana/7.16/index.html)
- [Filebeat Documentation](https://www.elastic.co/guide/en/beats/filebeat/7.16/index.html)

## 📄 License

This project is provided as-is for educational and development purposes.

## 👤 Author

Created for distributed log analysis and build system monitoring.

---

**Last Updated:** November 2025  
**ELK Stack Version:** 7.16.2  

