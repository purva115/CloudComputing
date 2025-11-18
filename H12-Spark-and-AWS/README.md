---

# Hands-on-12 — Serverless Spark ETL Pipeline on AWS

This project implements a **fully automated, serverless Spark ETL pipeline on AWS**, triggered by S3 events and executed using an AWS Glue Spark job. The pipeline cleans raw review data, runs analytical Spark SQL queries, and stores processed results back into S3 in a structured format.

---

## 📸 Completed Pipeline Screenshots

### ✔️ AWS Glue Job — Successful Runs

![Glue job run](images/glue-job.png)

### ✔️ S3 Buckets — Landing & Processed

![S3 buckets](images/s3-buckets.png)

### ✔️ Athena Results — Output Folders

![Athena Results](images/athena-results.png)

---

## 📊 Project Overview

This pipeline automates the full data engineering flow:

```
S3 Upload → Lambda Trigger → Glue Spark ETL → S3 Processed → Athena
```

The Spark job performs:

* Reading raw CSV review data
* Cleaning & standardizing columns
* Converting dates and casting numeric fields
* Running analytical Spark SQL queries
* Writing Parquet outputs to S3

---

## 📁 Repository Structure

```
/
├── README.md
├── reviews.csv
├── src/
│   ├── glue_job_script.py
│   └── lambda_function.py
└── images/
    ├── glue-job.png
    ├── s3-buckets.png
    ├── athena-results.png
```

---

## 🔧 Components Implemented

### 1️⃣ AWS Lambda Trigger

Automatically invokes the Glue ETL job whenever a file is added to the landing bucket.

### 2️⃣ AWS Glue Job (PySpark)

Handles:

* Data ingestion
* Cleaning and transformations
* Running Spark SQL aggregations
* Outputting to S3

### 3️⃣ S3 Buckets

* `landing/` → raw input files
* `processed/` → cleaned data
* `Athena Results/` → Spark SQL outputs

---

## 📊 Required Spark SQL Queries

All required queries are implemented in the Glue ETL script.

### ✔️ Query A — Average rating per product category

```sql
SELECT category, 
       ROUND(AVG(rating),2) AS avg_rating,
       COUNT(*) AS review_count
FROM reviews
GROUP BY category
ORDER BY avg_rating DESC;
```

### ✔️ Query B — Top 10 products with ≥ 50 reviews

```sql
SELECT product_id,
       ROUND(AVG(rating),2) AS avg_rating,
       COUNT(*) AS reviews
FROM reviews
GROUP BY product_id
HAVING COUNT(*) >= 50
ORDER BY avg_rating DESC
LIMIT 10;
```

### ✔️ Query C — Monthly rating trend

```sql
SELECT date_format(to_date(review_date, 'yyyy-MM-dd'), 'yyyy-MM') AS year_month,
       ROUND(AVG(rating),2) AS avg_rating,
       COUNT(*) AS reviews
FROM reviews
GROUP BY date_format(to_date(review_date, 'yyyy-MM-dd'), 'yyyy-MM')
ORDER BY year_month;
```

---

## 🔁 How to Run the Pipeline

1. Upload `reviews.csv` to the **landing** bucket.
2. Lambda auto-triggers the Glue ETL job.
3. Glue job generates output:

   * Cleaned data → `processed/`
   * Query results → `Athena Results/`
4. Query results using **AWS Athena**.

---

## 🎉 Status

All elements of the assignment are complete:

* Glue job runs successfully
* S3 structure matches requirements
* SQL outputs appear in **Athena Results**
* Pipeline functions end-to-end

---


