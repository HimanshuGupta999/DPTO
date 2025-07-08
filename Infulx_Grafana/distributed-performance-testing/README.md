# 🚀 Distributed JMeter Test Execution with InfluxDB & Grafana

This project provides a complete setup to run **distributed JMeter tests** using a Docker-based **master-slave architecture**, with real-time metrics stored in **InfluxDB** and visualized in **Grafana**.

It automates provisioning of:
- ✅ JMeter Master and Slaves
- ✅ InfluxDB for storing metrics
- ✅ Grafana with pre-configured dashboards

---

## 📝 Prerequisites

Before running this setup, ensure you have:

- **Docker** and **Docker Compose** installed  
  - [Install Docker](https://docs.docker.com/get-docker/)  
  - [Install Docker Compose](https://docs.docker.com/compose/install/)  
- **Node.js (v14 or higher)** and **npm** installed for utility scripts  
- A valid **JMeter test plan (.jmx)** file located in the `test-files/` directory  
- SSH enabled on your system (required for communication between master and slaves)  
- Environment variables defined in a `.env` file (see [Configuration](#️-configuration))  

---

## ⚙️ Configuration

Create a `.env` file in the root directory with the following variables:

```env
# Master & Slave Config
MASTER_IP=<MASTER_CONTAINER_IP>
SLAVE_IPS=<SLAVE_CONTAINER_IP1>,<SLAVE_CONTAINER_IP2>
SSH_USERNAME=<SSH_USERNAME>
SSH_PASSWORD=<SSH_PASSWORD>

# JMeter Config
JMETER_VERSION=<JMETER_VERSION>
TEST_PLAN_PATH=<PATH_TO_YOUR_JMX_FILE>
RESULT_PATH=<PATH_TO_RESULTS_DIRECTORY>
NUMBER_OF_THREADS=<NUMBER_OF_THREADS>

# InfluxDB Config
INFLUXDB_ADMIN_USER=<INFLUXDB_USERNAME>
INFLUXDB_ADMIN_PASSWORD=<INFLUXDB_PASSWORD>
INFLUXDB_ORG=<INFLUXDB_ORGANIZATION>
INFLUXDB_BUCKET=<INFLUXDB_BUCKET>
INFLUXDB_TOKEN=<INFLUXDB_API_TOKEN>

# Grafana Config
GRAFANA_ADMIN_USER=<GRAFANA_USERNAME>
GRAFANA_ADMIN_PASSWORD=<GRAFANA_PASSWORD>

# Application Name (used in InfluxDB tags)
APPLICATION_NAME=<APPLICATION_NAME>
```
# Project Structure

INFLUX_GRAFANA/
├── distributed-performance-testing/
│   ├── config/
│   │   └── config.js
│   ├── grafana/
│   │   ├── dashboards/
│   │   ├── provisioning/
│   │   │   ├── datasources/
│   │   │   │   ├── datasources.template.yml
│   │   │   │   ├── datasource.yml (generated)
│   │   │   ├── dashboards/
│   │   │   │   ├── dashboard.yml
│   ├── src/
│   │   ├── commands/
│   │   ├── installation/
│   │   ├── remote/
│   │   ├── utility/
│   │   ├── index.js
│   │   ├── jmeter_execution.log
│   ├── test-files/
│   │   ├── <YOUR_TEST_PLAN>.jmx
│   │   ├── results/
│   │   ├── results_2/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── bkp_docker-compose.yml (optional backup)
│   ├── entrypoint.sh
│   ├── generateDatasourceConfig.js
│   ├── .env
│   ├── .env.template
│   ├── README.md



## 📦 Installation

### 1. Clone the Repository

Clone the repository to your local machine:  

```bash
git clone <repo>
cd distributed-performance-testing

```

### 2. Configure Environment Variables
 
 Copy the .env.template file to .env and modify the variables as per your setup:

```bash
cp .env.template .env

nano .env

```
Update details like:

    MASTER_IP, SLAVE_IPS

    JMETER_VERSION, TEST_PLAN_PATH, RESULT_PATH

    InfluxDB and Grafana credentials

### 3. Install Node.js Dependencies

```bash
npm install

```

### 4. Generate Grafana Datasource Configuration

```bash
node generateDatasourceConfig.js

```
This will create dashboard.template.yml file for grafana


### 5. Build and Start Docker Containers
```bash
docker-compose build 
docker-compose up 
```
### 6 Run the jmx file using index.js
Place your JMeter .jmx test plans in the test-files/ directory.

run the commands
```bash
cd src
node index.js
```