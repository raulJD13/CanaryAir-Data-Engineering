# CanaryAir: Real-Time Air Quality Engineering Pipeline

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Container-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-Automated-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)


> A production-ready data engineering solution for real-time air quality monitoring in the Canary Islands, featuring automated ETL pipelines, cloud infrastructure, and interactive analytics.

**Live Dashboard:** [https://canaryair-data-engineering.streamlit.app/](https://canaryair-data-engineering.streamlit.app/)

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Key Features](#key-features)
- [System Design](#system-design)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Development Setup](#local-development-setup)
  - [Docker Deployment](#docker-deployment)
  - [Cloud Deployment](#cloud-deployment)
- [Project Structure](#project-structure)
- [Data Pipeline](#data-pipeline)
- [Dashboard Features](#dashboard-features)
- [Performance & Optimization](#performance--optimization)
- [Monitoring & Maintenance](#monitoring--maintenance)
- [Testing](#testing)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [License](#license)
- [Author](#author)
- [Acknowledgments](#acknowledgments)

---

## Overview

**CanaryAir** is an end-to-end Data Engineering project that implements a modern data stack for monitoring air quality in the Canary Islands. The system focuses on tracking the "Calima" phenomenon (Saharan dust intrusions), which significantly impacts air quality, visibility, and public health in the region.

This project demonstrates professional data engineering practices including:
- Scalable ETL/ELT pipeline architecture
- Cloud-native infrastructure on Neon.tech
- Automated orchestration with GitHub Actions
- Real-time data visualization and analytics
- Production-ready code with proper error handling and logging

### What Makes This Project Unique

- **Real-World Application:** Addresses actual environmental monitoring needs in the Canary Islands
- **Modern Stack:** Implements current industry best practices for data engineering
- **Full Automation:** Zero-maintenance pipeline with serverless execution
- **Comprehensive Documentation:** Production-ready code with detailed documentation
- **Scalable Design:** Architecture ready for expansion to multiple regions

---

## Problem Statement

The Canary Islands experience frequent "Calima" episodes—atmospheric events where Saharan dust particles are transported across the Atlantic Ocean. These events cause:

- **Health Impacts:** Respiratory issues, allergies, and increased hospitalizations
- **Economic Effects:** Disruption to tourism and aviation
- **Environmental Concerns:** Air quality degradation and ecosystem stress

**Solution:** CanaryAir provides real-time monitoring and historical analysis of air quality metrics (PM10, PM2.5, dust concentration) to help residents, health officials, and researchers make informed decisions.

---

## Architecture


The system implements a **Cloud-Native ETL Architecture** with the following components:

### Data Flow

```
┌─────────────────┐
│  Open-Meteo API │  ◄── Data Source (Meteorological Data)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ GitHub Actions  │  ◄── Orchestration (Cron Scheduler)
│  (Every Hour)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Python ETL     │  ◄── Processing Layer
│  - Extraction   │      • Data Validation
│  - Transform    │      • Cleaning & Enrichment
│  - Load         │      • Duplicate Prevention
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Neon.tech DB   │  ◄── Storage (Cloud PostgreSQL + PostGIS)
│  (PostgreSQL)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Streamlit App   │  ◄── Presentation Layer
│  + Plotly       │      • Interactive Dashboards
│  + PyDeck       │      • Real-time KPIs
│  + SciPy        │      • Data Quality Reports
└─────────────────┘
```

### Architecture Highlights

1. **Ingestion Layer:** Python scripts connect to Open-Meteo API for hourly meteorological data
2. **Orchestration:** GitHub Actions provides serverless scheduling (eliminates dedicated server costs)
3. **Storage:** Neon.tech serverless PostgreSQL with PostGIS for geospatial operations
4. **Transformation:** Pandas handles data cleaning, validation, and standardization
5. **Presentation:** Streamlit delivers interactive web-based analytics with Plotly visualizations

---

## Technology Stack

### Core Engineering

| Technology | Purpose | Version |
|-----------|---------|---------|
| **Python** | Primary programming language | 3.9+ |
| **SQLAlchemy** | ORM for database operations | Latest |
| **Psycopg2** | PostgreSQL adapter | Latest |
| **Pandas** | Data manipulation and transformation | Latest |
| **NumPy** | Numerical computing | Latest |
| **Python-dotenv** | Environment variable management | Latest |

### Infrastructure & DevOps

| Technology | Purpose | Details |
|-----------|---------|---------|
| **Docker** | Containerization for local development | Multi-container setup |
| **Docker Compose** | Local orchestration | Database + pgAdmin + ETL |
| **GitHub Actions** | CI/CD & scheduled jobs | Serverless cron execution |
| **Neon.tech** | Cloud PostgreSQL database | Serverless, auto-scaling |
| **Streamlit Cloud** | Frontend hosting | Free tier deployment |

### Data Visualization & Analytics

| Technology | Purpose | Use Case |
|-----------|---------|----------|
| **Streamlit** | Web application framework | Interactive dashboards |
| **PyDeck** | Geospatial visualization | 3D sensor location maps |
| **Plotly** | Interactive charts | Time-series analysis |
| **SciPy** | Statistical analysis | Correlations, distributions |

### APIs & Data Sources

- **Open-Meteo API:** Free meteorological data (no API key required)
- **PostGIS Extension:** Geospatial queries and operations

---

## Key Features

### Pipeline Features

- **Automated Execution:** Runs every hour via GitHub Actions without manual intervention
- **Idempotent Design:** Prevents duplicate data insertion with PostgreSQL `ON CONFLICT` clauses
- **Environment Detection:** Intelligently detects runtime environment (Docker, Mac, Cloud)
- **Error Handling:** Comprehensive exception handling with detailed logging
- **Data Validation:** Quality checks before database insertion
- **Timezone Management:** Proper UTC/local timezone handling

### Security Features

- **Credential Management:** Secrets stored in GitHub Secrets and `.env` files
- **No Hardcoded Values:** All sensitive data externalized
- **SSL Database Connections:** Encrypted connections to cloud database
- **Access Control:** Database credentials never exposed in version control

### Dashboard Features

- **Real-Time KPIs:** Current air quality metrics and health indices
- **Historical Analysis:** Trends over days, weeks, and months
- **Geospatial Visualization:** 3D maps showing sensor locations
- **Data Quality Reports:** Completeness analysis, outlier detection, missing data alerts
- **Correlation Analysis:** Statistical relationships between meteorological variables
- **Export Capabilities:** Download filtered data as CSV

### Data Quality Features

- **Completeness Checks:** Tracks missing data points
- **Outlier Detection:** Identifies anomalous readings
- **Timestamp Validation:** Ensures data freshness
- **Duplicate Prevention:** Guarantees data integrity
- **Schema Validation:** Type checking before insertion

---

## System Design

### Database Schema

```sql
CREATE TABLE air_quality_measurements (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    location_name VARCHAR(100) NOT NULL,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    pm10 DECIMAL(10,2),
    pm2_5 DECIMAL(10,2),
    dust DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(timestamp, location_name)
);

CREATE INDEX idx_timestamp ON air_quality_measurements(timestamp);
CREATE INDEX idx_location ON air_quality_measurements(location_name);
```

### API Integration

The project uses the Open-Meteo API with the following endpoint structure:

```python
API_BASE = "https://air-quality-api.open-meteo.com/v1/air-quality"
PARAMS = {
    "latitude": 28.4682,
    "longitude": -16.2546,
    "hourly": "pm10,pm2_5,dust",
    "timezone": "Europe/Madrid"
}
```

### CI/CD Workflow

```yaml
name: Hourly Data Ingestion

on:
  schedule:
    - cron: '0 * * * *'  # Every hour
  workflow_dispatch:

jobs:
  run-etl:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run ETL
        env:
          DATABASE_URL_CLOUD: ${{ secrets.DATABASE_URL_CLOUD }}
        run: python src/etl_pipeline.py
```

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Docker and Docker Compose (for local development)
- PostgreSQL client (optional, for database management)
- Active GitHub account (for CI/CD)
- Neon.tech account (for cloud database)

### Local Development Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/raulJD13/CanaryAir-Data-Engineering.git
cd CanaryAir-Data-Engineering
```

#### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# Cloud Database Connection
DATABASE_URL_CLOUD=postgresql://user:password@hostname/dbname?sslmode=require

# Local Database Connection (if using Docker)
DATABASE_URL_LOCAL=postgresql://postgres:postgres@localhost:5432/canaryair

# Application Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
```

#### 5. Initialize Database (Local)

If using local PostgreSQL:

```bash
# Run database initialization script
python scripts/init_db.py
```

#### 6. Run the ETL Pipeline

```bash
# Test the data ingestion
python src/etl_pipeline.py
```

#### 7. Launch the Dashboard

```bash
# Start Streamlit application
streamlit run src/app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`.

### Docker Deployment

For a fully containerized local environment:

#### 1. Build and Start Containers

```bash
# Build images and start services
docker-compose up -d --build
```

This command starts:
- PostgreSQL database on port 5432
- pgAdmin web interface on port 5050
- ETL worker container

#### 2. Access Services

- **pgAdmin:** `http://localhost:5050`
  - Email: `admin@canaryair.com`
  - Password: `admin`

- **Database Connection (from pgAdmin):**
  - Host: `postgres`
  - Port: `5432`
  - Database: `canaryair`
  - Username: `postgres`
  - Password: `postgres`

#### 3. View Logs

```bash
# View all container logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f etl_worker
```

#### 4. Stop Containers

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

### Cloud Deployment

#### Database Setup (Neon.tech)

1. Create a Neon.tech account at [neon.tech](https://neon.tech)
2. Create a new project: "CanaryAir"
3. Copy the connection string (PostgreSQL format)
4. Add connection string to GitHub Secrets as `DATABASE_URL_CLOUD`

#### GitHub Actions Setup

1. Navigate to repository Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `DATABASE_URL_CLOUD`: Your Neon.tech connection string
3. Enable GitHub Actions in your repository
4. The pipeline will run automatically every hour

#### Streamlit Cloud Deployment

1. Fork or push the repository to your GitHub account
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository and branch
5. Set main file path: `src/app.py`
6. Add secrets in "Advanced settings":
   ```toml
   [connections.postgresql]
   url = "your_connection_string_here"
   ```
7. Click "Deploy"

---

## Project Structure

```
CanaryAir-Data-Engineering/
│
├── .github/
│   └── workflows/
│       └── etl_pipeline.yml      # GitHub Actions workflow
│
├── src/
│   ├── app.py                    # Streamlit dashboard application
│   ├── etl_pipeline.py           # Main ETL script
│   ├── database.py               # Database connection utilities
│   ├── data_quality.py           # Data validation functions
│   └── visualizations.py         # Chart generation functions
│
├── scripts/
│   ├── init_db.py                # Database initialization script
│   └── test_connection.py        # Connection testing utility
│
├── data/
│   ├── raw/                      # Raw data samples (for testing)
│   └── processed/                # Processed data outputs
│
├── notebooks/
│   ├── exploration.ipynb         # Data exploration notebook
│   └── analysis.ipynb            # Statistical analysis notebook
│
├── tests/
│   ├── test_etl.py               # ETL pipeline tests
│   ├── test_database.py          # Database operation tests
│   └── test_api.py               # API integration tests
│
├── docker/
│   ├── Dockerfile                # ETL worker container
│   └── Dockerfile.streamlit      # Streamlit app container
│
├── docs/
│   ├── architecture.md           # Detailed architecture documentation
│   ├── api_reference.md          # API documentation
│   └── deployment_guide.md       # Step-by-step deployment guide
│
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── docker-compose.yml            # Local development stack
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── LICENSE                       # MIT License
```

---

## Data Pipeline

### Extraction Phase

The extraction process retrieves data from the Open-Meteo API:

```python
def extract_data(location):
    """
    Extract air quality data from Open-Meteo API.
    
    Args:
        location: Dict with latitude, longitude, name
        
    Returns:
        DataFrame with hourly measurements
    """
    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "hourly": "pm10,pm2_5,dust",
        "timezone": "Europe/Madrid"
    }
    
    response = requests.get(API_BASE, params=params)
    response.raise_for_status()
    
    return pd.DataFrame(response.json()["hourly"])
```

### Transformation Phase

Data transformation includes:

1. **Timestamp Parsing:** Convert string timestamps to datetime objects
2. **Data Validation:** Check for null values, out-of-range values
3. **Unit Standardization:** Ensure consistent measurement units
4. **Location Enrichment:** Add geographic metadata
5. **Quality Flags:** Mark suspicious or missing data

```python
def transform_data(df, location_name):
    """
    Transform and validate extracted data.
    
    Args:
        df: Raw DataFrame from API
        location_name: Name of measurement location
        
    Returns:
        Cleaned and validated DataFrame
    """
    df["timestamp"] = pd.to_datetime(df["time"])
    df["location_name"] = location_name
    df = df.drop("time", axis=1)
    
    # Validate ranges
    df = df[(df["pm10"] >= 0) & (df["pm10"] <= 1000)]
    df = df[(df["pm2_5"] >= 0) & (df["pm2_5"] <= 500)]
    
    return df
```

### Load Phase

Data is loaded into PostgreSQL with idempotent operations:

```python
def load_data(df, engine):
    """
    Load data into PostgreSQL with duplicate prevention.
    
    Args:
        df: Transformed DataFrame
        engine: SQLAlchemy engine
    """
    df.to_sql(
        "air_quality_measurements",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )
    
    # Handle duplicates at database level
    # UNIQUE constraint on (timestamp, location_name)
```

---

## Dashboard Features

### Home Page

- **Current Conditions Card:** Latest readings with health index
- **Key Metrics:** PM10, PM2.5, Dust concentration
- **Trend Indicators:** 24-hour change percentages
- **Health Recommendations:** Based on air quality index

### Time Series Analysis

- **Interactive Charts:** Plotly-powered zoom and pan
- **Multiple Variables:** Compare PM10, PM2.5, dust simultaneously
- **Time Range Selection:** Hour, day, week, month, custom
- **Statistical Overlays:** Moving averages, trend lines

### Geospatial Visualization

- **3D Map View:** PyDeck hexagon layers
- **Sensor Locations:** All monitoring stations
- **Color-Coded Severity:** Visual air quality representation
- **Interactive Tooltips:** Detailed station information

### Data Quality Dashboard

- **Completeness Metrics:** Percentage of expected vs. actual data points
- **Outlier Detection:** Statistical identification of anomalies
- **Missing Data Analysis:** Gaps in time series
- **Freshness Indicators:** Time since last update

### Statistical Analysis

- **Correlation Matrix:** Relationship between variables
- **Distribution Plots:** Histograms and box plots
- **Percentile Rankings:** Historical context for current readings
- **Calima Event Detection:** Automated identification of dust events

---

## Performance & Optimization

### Database Optimizations

- **Indexing Strategy:** Indexes on timestamp and location columns
- **Connection Pooling:** SQLAlchemy pool management
- **Query Optimization:** Efficient WHERE clauses and JOINs
- **Partitioning (Future):** Time-based partitioning for historical data

### Application Optimizations

- **Caching:** Streamlit `@st.cache_data` for expensive operations
- **Lazy Loading:** Load data only when needed
- **Query Limits:** Fetch only necessary date ranges
- **Asynchronous Operations:** Background data refresh

### Infrastructure Optimizations

- **Serverless Database:** Auto-scaling with Neon.tech
- **CDN Delivery:** Streamlit Cloud edge distribution
- **Minimal Dependencies:** Reduced container size
- **Efficient Scheduling:** Hourly execution only when needed

---

## Monitoring & Maintenance

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

### Health Checks

- **Database Connectivity:** Pre-execution connection tests
- **API Availability:** Open-Meteo endpoint validation
- **Data Freshness:** Alert if no new data in 2 hours
- **Error Rate Monitoring:** Track failed pipeline runs

### Alerts & Notifications

Configure GitHub Actions notifications for:
- Pipeline failures
- Data quality issues
- API rate limiting
- Database connection errors

---

## Testing

### Unit Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_etl.py
```

### Integration Tests

```bash
# Test database operations
pytest tests/test_database.py -v

# Test API integration
pytest tests/test_api.py -v
```

### Local Testing

```bash
# Test ETL pipeline locally
python src/etl_pipeline.py --dry-run

# Test dashboard locally
streamlit run src/app.py
```

---

## Contributing

Contributions are welcome! Please follow these guidelines:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Write tests** for new functionality
5. **Ensure tests pass**
   ```bash
   pytest tests/
   ```
6. **Commit with clear messages**
   ```bash
   git commit -m "Add: Description of your changes"
   ```
7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
8. **Submit a Pull Request**

### Code Standards

- Follow PEP 8 style guidelines
- Write docstrings for all functions
- Add type hints where applicable
- Keep functions focused and modular
- Write meaningful commit messages

### Areas for Contribution

- Additional data sources integration
- Advanced analytics features
- Mobile-responsive dashboard improvements
- Multi-language support
- Machine learning predictions
- Additional geographic locations

---

## Roadmap

### Phase 5: Machine Learning Integration (Q1 2026)

- Predictive models for Calima events
- Anomaly detection algorithms
- Forecast dashboard with 24-48 hour predictions

### Phase 6: Multi-Region Expansion (Q2 2026)

- Add monitoring for mainland Spain
- European air quality integration
- Comparative regional analysis

### Phase 7: Mobile Application (Q3 2026)

- Native iOS and Android apps
- Push notifications for poor air quality
- Location-based personalized alerts

### Phase 8: Advanced Analytics (Q4 2026)

- Real-time data streaming with Apache Kafka
- Data lake integration for historical analysis
- Advanced visualization with custom dashboards

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

- Commercial use allowed
- Modification allowed
- Distribution allowed
- Private use allowed
- Liability and warranty limitations apply

---

## Author

**Raúl Jiménez**  
*Data Engineer | Big Data & AI Enthusiast*

- GitHub: [@raulJD13](https://github.com/raulJD13)
- LinkedIn: [Connect with me]([https://www.linkedin.com/in/raul-jimenez-data-engineer](https://www.linkedin.com/in/raul-jimenez-delgado-06108436b/))
- Email: raul.jimenez.del@gmail.com
- Portfolio: [raul-jimenez.dev](https://raul-jimenez.dev)

---

## Acknowledgments

- **Open-Meteo:** For providing free, high-quality meteorological data
- **Neon.tech:** For serverless PostgreSQL infrastructure
- **Streamlit Community:** For the excellent web framework
- **Canary Islands Environmental Agency:** For air quality research and awareness
- **GitHub:** For free Actions runner hours and hosting

---

## Additional Resources

- [Open-Meteo API Documentation](https://open-meteo.com/en/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Neon.tech Documentation](https://neon.tech/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## Support

If you find this project helpful:

- Give it a ⭐ on GitHub
- Share it with others who might benefit
- Contribute to its development
- Report bugs or suggest features in [Issues](https://github.com/raulJD13/CanaryAir-Data-Engineering/issues)

