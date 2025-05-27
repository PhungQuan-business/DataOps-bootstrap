
---
# 🚀 DataOps Demo: From Raw CSV to Data Analytics Dashboard

Welcome to the **DataOps Bootstrap Demo** – a hands-on walkthrough to show how raw data can go through a full data pipeline: from upload 🗂️ to transformation 🔧 to visualization 📊 — using open-source tools and a reproducible setup.

---

## 🧠 What You’ll Learn

This project introduces a simplified **DataOps** workflow that automates and validates how data flows across the system. You'll learn how to:

- Extract data from Google Drive
- Validate data quality using Great Expectations
- Store raw data in a data lake (MinIO)
- Process and post-validate the data
- Load clean data into PostgreSQL
- Visualize it with Superset

## Introduction

### 1. What is DataOps?

**DataOps** (Data Operations) is an approach for managing data pipelines in an automated, flexible, and scalable manner. It combines principles from **DevOps**, **Agile**, and **Lean Manufacturing** to ensure data is always available, accurate, and reliable throughout the analytics process.

_References pending_

### 2. Why DataOps for Data Analysis?


In modern analytics environments, data originates from multiple sources, changes frequently, and demands rapid processing. DataOps helps to:

- Automate the processes of data collection, transformation, and distribution.
- Improve data quality and transparency.
- Ensure reliable and testable data pipelines.
- Reduce the time from raw data to actionable insights.

---

## 📊 System Architecture

![Architecture Diagram](images/dataops-architecture.png)

---

## 🛠️ Tools Used

| Tool                   | Purpose                                           |
| ---------------------- | ------------------------------------------------- |
| **Google Drive**       | Upload source CSV files                           |
| **Great Expectations** | Validate data quality before and after processing |
| **MinIO**              | Acts as a Data Lake for raw CSV files             |
| **Astro + Airflow**    | Orchestrate the entire pipeline                   |
| **PostgreSQL**         | Store final, clean analytics-ready data           |
| **Jupyter Notebook**   | Analyze and experiment with processed data        |
| **Superset**           | Visualize and explore analytics dashboards        |

---

## 📦 Prerequisites (Xem lại cái này, nào là những tool cần)

Make sure you have the following tools installed:

- [Docker](https://www.docker.com/products/docker-desktop) 🐳
- [Astro CLI](https://docs.astronomer.io/astro/cli/install-cli) 🚀
- [Git](https://git-scm.com/) 🔧 

---

## 🧭 Step-by-Step Guide

### ✅ Step 1: Upload Your CSV Dataset

Upload your raw data (CSV format) to a folder on **Google Drive**. This acts as the entry point of the pipeline.

> 💡 Tip: Make sure the data format is consistent and clean (e.g., column names, date formats, etc.)

---

### 📥 Step 2: Extract Data to Local Machine

The pipeline will **automatically download** your uploaded file to the local filesystem using a Google Drive API or a shared download script.

---

### 🧪 Step 3: Pre-Validation with Great Expectations

Before the raw data gets processed:

- A **predefined validation rule** (expectation suite) is applied.
- If the data **passes validation**, it is allowed to move to the next step.
- If it **fails**, you'll get a detailed validation report so you can fix issues.

> ✅ Validation rules include checks like:
>
> - No missing values in key columns
> - Correct data types (e.g., integer, date, etc.)
> - No mismatch column count (missing column, additional column)

---

### 🗂️ Step 4: Store Raw Data in MinIO (Data Lake)

Once validated, the data is pushed to **MinIO**, an S3-compatible object storage system. This mimics the behavior of a modern **Data Lake**.

---

### 🔄 Step 5: Transform and Post-Validate

The pipeline retrieves data from MinIO and runs a **transformation script** to clean or restructure the dataset. After that:

- A second **post-validation** step ensures the processed data meets your final expectations.
- The final data is **stored locally** as files (CSV, Parquet, etc.)

---

### 🛢️ Step 6: Load Data into PostgreSQL

Cleaned and validated data is loaded into a **PostgreSQL** database for persistent storage.

You can now run queries on structured tables for reporting and analysis.

---

### 📊 Step 7: Visualize with Superset

Although not included in this version, the database is structured to connect with [Apache Superset](https://superset.apache.org/), a powerful open-source business intelligence tool.

---

## 🧰 Project Setup

### Clone the Repository

```bash
git clone https://github.com/PhungQuan-business/DataOps-bootstrap.git
cd DataOps-bootstrap
```

### Install Astro CLI (if not yet installed)

```bash
curl -sSL install.astronomer.io | sudo bash -s
```

### Install Docker (Linux)

```bash
chmod +x setup/machine-setup/install_docker.sh
./setup/machine-setup/install_docker.sh
```

### Update OS Settings (Linux)

```bash
chmod +x setup/machine-setup/update_OS_setting.sh
./setup/machine-setup/update_OS_setting.sh
```

### Setup Environment

```bash
cp .env.example demo/.env
```

### Initialize Airflow Project

```bash
cd demo
astro dev init
```

Access the Airflow UI at [http://localhost:8080](http://localhost:8080)

- **Username:** `admin`
- **Password:** `admin`

---

## 📌 Next Steps

- [ ] Add Data Ingestion setup
- [ ] Extend validations to include schema evolution checks
- [ ] Support other data sources (APIs, databases)

---

## 🙋‍♂️ Questions?

Feel free to open an issue or contact the maintainer. Happy DataOps-ing!

---

Welcome! This project is a simple but functional blueprint for a DataOps + BI with [Apache Airflow](https://airflow.apache.org/). Fork this project to create your own data processing pipeline!
