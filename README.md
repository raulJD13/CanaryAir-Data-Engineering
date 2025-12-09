# 🌪️ CanaryAir: Real-Time Air Quality Engineering Pipeline

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Container-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-Automated-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)

## 📋 Project Overview

**CanaryAir** is an end-to-end Data Engineering project designed to monitor air quality, specifically focusing on the "Calima" (Saharan dust) phenomenon in the Canary Islands. 

This project demonstrates a full **Modern Data Stack** implementation, moving from a local Dockerized development environment to a fully automated cloud architecture. It ingests meteorological data in real-time, processes it using Python, stores it in a Cloud Data Warehouse, and visualizes it through an interactive analytical dashboard.

👉 **Live Demo:** [Click here to view the Dashboard](https://canaryair-data-engineering.streamlit.app/)

---

## 🏗️ Architecture

The system follows a **Cloud-Native ETL (Extract, Transform, Load)** architecture:

1.  **Ingestion:** A Python script connects to the **Open-Meteo API** to fetch hourly metrics (PM10, PM2.5, Dust).
2.  **Orchestration (CI/CD):** **GitHub Actions** acts as the scheduler (Cron Job), triggering the pipeline every hour automatically (Serverless execution).
3.  **Storage:** Data is loaded into **Neon.tech (Serverless PostgreSQL)**. The database is optimized with **PostGIS** extensions for geospatial queries.
4.  **Transformation:** Pandas handles data cleaning, timestamp standardization, and idempotency checks (preventing duplicates).
5.  **Visualization:** A **Streamlit** web app consumes the data from the cloud DB to render real-time KPIs, historical trends (Plotly), and geospatial maps (PyDeck).

---

## 🛠️ Tech Stack

### 🔹 Core Engineering
* **Python 3.9+**: Main programming language for ETL and Backend logic.
* **SQLAlchemy & Psycopg2**: ORM and database adapters for secure SQL transactions.
* **Pandas**: Data manipulation, cleaning, and transformation.
* **Dotenv**: Environment variable management for security.

### 🔹 Infrastructure & Cloud
* **Docker & Docker Compose**: Used for local development (isolating Database, pgAdmin, and ETL Worker).
* **GitHub Actions**: CI/CD pipeline for automated hourly data ingestion (Serverless Cron).
* **Neon.tech**: Serverless Cloud PostgreSQL Database.
* **Streamlit Cloud**: Hosting platform for the frontend application.

### 🔹 Data Visualization & Analytics
* **Streamlit**: Interactive web framework.
* **PyDeck**: Geospatial visualization (3D Maps) for sensor location.
* **Plotly**: Advanced interactive charting for time-series analysis.
* **SciPy**: Used for statistical analysis (correlations, distributions).

---

## 🚀 Key Features

* **🔄 Automated Pipeline:** Zero-maintenance ETL running on GitHub infrastructure.
* **🛡️ Idempotent Ingestion:** The pipeline is designed to handle re-runs gracefully without creating duplicate records (`ON CONFLICT DO NOTHING`).
* **🌍 Hybrid Environment Logic:** The code intelligently detects if it's running inside Docker, on a Mac, or in the Cloud, adjusting database connections automatically.
* **🔒 Security:** Credentials are managed via GitHub Secrets and `.env` files, never exposed in the codebase.
* **📊 Data Quality Checks:** The dashboard includes a dedicated tab for analyzing data completeness, validity, and outliers.

---

## ⚙️ Local Setup (For Developers)

If you want to run this project locally:

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/raulJD13/CanaryAir-Data-Engineering.git](https://github.com/raulJD13/CanaryAir-Data-Engineering.git)
    cd CanaryAir-Data-Engineering
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    Create a `.env` file in the root directory:
    ```env
    DATABASE_URL_CLOUD=postgresql://user:password@hostname/dbname?sslmode=require
    ```

5.  **Run with Docker (Optional)**
    To spin up the local database and worker:
    ```bash
    docker-compose up -d --build
    ```

6.  **Run the Dashboard**
    ```bash
    streamlit run src/app.py
    ```

---

## 📈 Project Evolution

* **Phase 1:** Local Python Scripts & CSVs.
* **Phase 2:** Containerization with Docker & Local PostgreSQL.
* **Phase 3:** Cloud Migration (Neon DB) & Advanced Analytics.
* **Phase 4:** Full Automation with GitHub Actions (Current Version).

---

## 👤 Author

**Raúl Jiménez** *Data Engineer | Big Data & AI Enthusiast*

---
