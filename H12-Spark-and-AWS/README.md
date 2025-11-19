---

# Hands-on-12 — Serverless Spark ETL Pipeline on AWS

This project implements a **fully automated, serverless Spark ETL pipeline on AWS**, triggered by S3 events and executed using an AWS Glue Spark job. The pipeline cleans raw review data, runs analytical Spark SQL queries, and stores processed results back into S3 in a structured format.

---

## 📸 Completed Pipeline Screenshots
### ✔️ AWS Lambda Function
<img width="1886" height="642" alt="image" src="https://github.com/user-attachments/assets/aa81f712-453d-41ed-a365-1048a5384eff" />

### ✔️ AWS Glue Job — Successful Runs

<img width="1867" height="668" alt="image" src="https://github.com/user-attachments/assets/d81743b2-6a11-461a-b81e-3aab69e26e99" />


### ✔️ S3 Buckets — Landing & Processed

<img width="1882" height="573" alt="image" src="https://github.com/user-attachments/assets/54fb45ce-57c5-4ab9-bfb7-8de9e0bfbc15" />



### ✔️ Athena Results — Output Folders

<img width="1892" height="752" alt="image" src="https://github.com/user-attachments/assets/f939eaed-f558-4dd0-9674-eff03389d03e" />


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
     <img width="1893" height="757" alt="image" src="https://github.com/user-attachments/assets/0ffb788c-2508-49f9-b054-50d9d51f1ecb" />

   * Query results → `Athena Results/`
4. Query results using **AWS Athena**.

---

## Results:
Folder : product_ratings
<img width="452" height="531" alt="image" src="https://github.com/user-attachments/assets/cd802f83-a70f-4d44-9123-3484ec46df67" />

Folder:datewise_reviews
<img width="247" height="832" alt="image" src="https://github.com/user-attachments/assets/1074be3c-1d12-4699-be16-4f708db04f8f" />

Folder:rating_distribution
<img width="202" height="176" alt="image" src="https://github.com/user-attachments/assets/5038c10e-1488-49ee-84c4-01889da06265" />

Folder: top_customers
<img width="265" height="147" alt="image" src="https://github.com/user-attachments/assets/a752f1d8-e892-4ac6-ac37-c9ae596b6e97" />


All elements of the assignment are complete:

* Glue job runs successfully
* S3 structure matches requirements
* SQL outputs appear in **Athena Results**
* Pipeline functions end-to-end

---


