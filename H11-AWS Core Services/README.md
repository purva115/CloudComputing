# AWS Core Services: E-Commerce Data Analysis

## 📋 Project Overview

This project demonstrates the use of AWS core services (S3, Glue, CloudWatch, and Athena) to analyze e-commerce sales data. The assignment involves setting up a complete data pipeline from raw data storage to advanced SQL analytics.

**Course:** ITCS 6190/8190 - Cloud Computing for Data Analysis  
**Semester:** Fall 2025  

---

## 🎯 Project Objectives

- Configure and manage AWS S3 buckets for data storage
- Implement IAM roles for secure service access
- Use AWS Glue for automated data cataloging
- Monitor ETL processes with CloudWatch
- Perform advanced SQL analytics using Amazon Athena

---

## 📊 Dataset

**Source:** [E-Commerce Sales Data - Kaggle](https://www.kaggle.com/datasets/thedevastator/unlock-profits-with-e-commerce-sales-data)

**Description:** The dataset contains e-commerce sales transactions with the following key attributes:
- Order details (ID, date, status)
- Product information (category, SKU, ASIN)
- Sales metrics (amount, quantity, currency)
- Geographic data (city, state, postal code, country)
- Fulfillment details (channel, service level, courier status)
- Customer type (B2B indicator)

**Table Structure:**
```
Database: output_db
Table: raw
Total Columns: 24
Key Columns:
  - date (string, format: MM-DD-YY)
  - amount (double)
  - qty (bigint)
  - ship-state (string)
  - category (string)
  - status (string)
```

---

## 🏗️ AWS Architecture

### Services Used

1. **Amazon S3 (Simple Storage Service)**
   - Purpose: Store raw CSV data and Athena query results
   - Bucket Name: `s3-sales-demo`

2. **AWS IAM (Identity and Access Management)**
   - Purpose: Manage permissions for Glue crawler
   - Role Name: `GlueS3AccessRole`
   - Policies: `AWSGlueServiceRole`, `AmazonS3FullAccess`

3. **AWS Glue**
   - Purpose: Automated data cataloging and schema discovery
   - Database: `output_db`
   - Crawler: `ecommerce-sales-crawler`

4. **AWS CloudWatch**
   - Purpose: Monitor crawler execution and logs
   - Log Group: `/aws-glue/crawlers`

5. **Amazon Athena**
   - Purpose: SQL-based data analysis

---

## 🔧 Setup and Configuration

### Step 1: S3 Bucket Creation

1. Created S3 bucket with unique name
2. Uploaded raw CSV file to bucket
3. Configured folder structure:
   ```
   s3-sales-demo /
   ├── processed/
   └── raw/
        |__Amazon Sales Report.csv
   ```


### Step 2: IAM Role Setup

1. Created IAM role: `GlueS3AccessRole`
2. Attached policies:
   - `AWSGlueServiceRole` - Allows Glue service operations
   - `AmazonS3FullAccess` - Allows S3 read/write operations
3. Trust relationship: AWS Glue service



### Step 3: Glue Database and Crawler

1. Created Glue database: `output_db`
2. Created crawler: `ecommerce-sales-crawler`
3. Configured data source: S3 bucket path
4. Assigned IAM role: `GlueS3AccessRole`
5. Set target database: `output_db`
6. Ran crawler successfully

**Crawler Results:**
- Tables created: 1 (`raw`)
- Columns detected: 24
- Data format: CSV
- Execution time: [X] minutes

### Step 4: Athena Configuration

1. Set query result location in S3
2. Selected data source: `AwsDataCatalog`
3. Selected database: `output_db`
4. Verified table schema

---

## 📈 SQL Queries and Analysis

### Query 1: Cumulative Sales Over Time

**Objective:** Calculate the running total of sales for each day in a specific year.

**Key Concepts:**
- Window functions (`SUM() OVER()`)
- Date parsing and filtering
- Running totals

---

### Query 2: Geographic Hotspot Analysis

**Objective:** Identify states with the highest total negative profit (unprofitable regions).

**Key Concepts:**
- Aggregation by geographic dimension
- Filtering for unprofitable transactions
- Geographic analysis

---

### Query 3: Impact of Discounts on Profitability

**Objective:** Analyze how different discount levels affect the profit ratio for each product sub-category.

**Key Concepts:**
- CASE statements for categorization
- Profit ratio calculations
- Discount level segmentation

---

### Query 4: Top 3 Most Profitable Products

**Objective:** Rank and identify the top 3 most profitable products within each category.

**Key Concepts:**
- Common Table Expressions (CTEs)
- Window functions with PARTITION BY
- ROW_NUMBER() for ranking

---

### Query 5: Monthly Sales and Profit Growth

**Objective:** Calculate month-over-month growth rates for both sales and profit metrics.

**Key Concepts:**
- Date truncation to monthly level
- LAG() window function
- Growth rate calculations

## 🛠️ Technical Challenges and Solutions

### Challenge 1: Date Format Parsing
**Issue:** Date column stored as string in MM-DD-YY format  
**Solution:** Used `DATE_PARSE(date, '%m-%d-%y')` for proper date conversion

### Challenge 2: Column Names with Hyphens
**Issue:** Column names like `ship-state` caused SQL errors  
**Solution:** Enclosed column names in double quotes: `"ship-state"`

---

## 🚀 How to Reproduce

1. **Prerequisites**
   - AWS Account with appropriate permissions
   - Dataset downloaded from Kaggle

2. **Setup Steps**
   ```bash
   # 1. Create S3 bucket
   aws s3 mb s3-sales-demo
   
   # 2. Upload dataset
   aws s3-sales-demo

   
   # 3. Create IAM role (via AWS Console)
   # 4. Create Glue database and crawler (via AWS Console)
   # 5. Run crawler
   # 6. Execute queries in Athena
   ```

3. **Run Queries**
   - Open Amazon Athena console
   - Select database: `output_db`
   - Copy and execute queries from `/queries` folder
   - Download results as CSV

---

## 💡 Lessons Learned

1. **AWS Glue** significantly simplifies schema discovery and data cataloging
2. **Athena** provides powerful SQL analytics without managing infrastructure
3. **Window functions** are essential for time-series and ranking analyses
4. **Date formatting** requires careful attention when working with string dates
---

## 🔗 References

- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [AWS Glue Documentation](https://docs.aws.amazon.com/glue/)
- [Amazon Athena Documentation](https://docs.aws.amazon.com/athena/)
- [AWS IAM Documentation](https://docs.aws.amazon.com/iam/)
- [Kaggle Dataset](https://www.kaggle.com/datasets/thedevastator/unlock-profits-with-e-commerce-sales-data)

---

