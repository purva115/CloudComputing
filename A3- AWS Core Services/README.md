# 🧩 ITCS-6190 Assignment 3: AWS Data Processing Pipeline

### Course: Cloud Computing for Data Analysis (ITCS 6190 / 8190, Fall 2025)

---

## 📘 Project Overview

This project demonstrates an **end-to-end serverless data processing pipeline** using AWS. The pipeline automates ingestion, transformation, cataloging, querying, and visualization of data using **S3, Lambda, Glue, Athena, and EC2**.

### **Approach**
The system is designed to simulate a real-world data engineering workflow:
1. **S3** acts as the storage layer for raw, processed, and enriched data.
2. **Lambda** automates data transformation upon file upload.
3. **Glue Crawler** dynamically catalogs processed data into a structured table.
4. **Athena** enables SQL-based queries on the data without servers.
5. **EC2 + Flask** hosts a simple web dashboard for data visualization.

---

## 🪣 1. Amazon S3 Bucket Structure

### **Explanation**
An Amazon S3 bucket is used to store and organize files throughout the data pipeline. The structure ensures a clean separation of workflow stages.

```plaintext
demo-bucket-as3/
│
├── raw/          # For incoming raw CSV data files
│   └── orders.csv
├── processed/    # For Lambda-processed and cleaned data
│   └── filtered_orders.csv
└── enriched/     # For Athena query results and dashboards
```

When a CSV file (e.g., `Orders.csv`) is uploaded to the `raw/` folder, the Lambda function automatically processes it and outputs results into the `processed/` folder.

📸 Screenshot - S3 Bucket
<img width="1881" height="717" alt="S3structure" src="https://github.com/user-attachments/assets/adbc6c06-4289-49df-b0a8-7466b28fcb62" />



---

## 🔐 2. IAM Roles and Permissions

### **Explanation**
IAM (Identity and Access Management) roles define permissions that allow AWS services to securely interact with one another. In this project, three distinct roles are created — each with a specific purpose and restricted access following the **principle of least privilege**.

---

### **Roles Configuration**

#### 🧩 1. Lambda Execution Role
**Purpose:** Allows the Lambda function to access and process data stored in Amazon S3.

**Setup Steps:**
1. Navigate to **IAM → Roles → Create Role**.
2. **Trusted Entity Type:** AWS Service
3. **Use Case:** Lambda
4. **Attach Policies:**
   - `AWSLambdaBasicExecutionRole`
   - `AmazonS3FullAccess`
5. **Role Name:** `Lambda-S3-Processing-Role`

This role grants Lambda permission to read from and write to S3 buckets while enabling CloudWatch logging.

---

#### 🕸️ 2. Glue Service Role
**Purpose:** Enables AWS Glue to access data in S3 and write metadata to the Glue Data Catalog.

**Setup Steps:**
1. Create a new IAM role for the **Glue** service.
2. **Attach Policies:**
   - `AmazonS3FullAccess`
   - `AWSGlueConsoleFullAccess`
   - `AWSGlueServiceRole`
3. **Role Name:** `Glue-S3-Crawler-Role`

This role allows the crawler to scan the processed S3 data and automatically create tables in the Glue Data Catalog.

---

#### 💻 3. EC2 Instance Role
**Purpose:** Allows the EC2 web server to query Athena and retrieve S3-stored results for dashboard visualization.

**Setup Steps:**
1. Create a new IAM role for the **EC2** service.
2. **Attach Policies:**
   - `AmazonS3FullAccess`
   - `AmazonAthenaFullAccess`
3. **Role Name:** `EC2-Athena-Dashboard-Role`

This ensures the EC2 instance can access query results and run the dashboard app seamlessly.

---

### **Approach**
Each role isolates specific AWS permissions:
- **Lambda** focuses on data processing.
- **Glue** manages cataloging.
- **EC2** handles data visualization.

This modular design prevents cross-service overreach and enhances security compliance.

---

📸 **Screenshot - IAM Roles Created**  
<img width="1387" height="492" alt="IAMroles" src="https://github.com/user-attachments/assets/c35cbf81-722c-409f-baa1-8b0e2e75eb07" />


---

## ⚙️ 3. Create the Lambda Function

### **Explanation**
The AWS Lambda function serves as the **automation core** of this data pipeline. It is triggered whenever a new raw data file (e.g., `Orders.csv`) is uploaded to the **raw/** folder in S3. The function reads, filters, and processes this file before saving the cleaned data into the **processed/** folder.

This enables **real-time data transformation** without any manual intervention or server management.

---

### **Steps to Create the Function**

1. Navigate to the **AWS Lambda Console** and click **Create Function**.
2. Choose **Author from scratch**.
3. Configure as follows:
   - **Function name:** `FilterAndProcessOrders`
   - **Runtime:** Python 3.9 (or newer)
   - **Permissions:** Expand **Change default execution role**, select **Use an existing role**, and choose `Lambda-S3-Processing-Role`.
4. Click **Create Function**.

---

### **Add Your Lambda Code**

Replace the default code in the editor with your `LambdaFunction.py` script. This script performs the following tasks:

1. **Reads** new `.csv` files from the `raw/` S3 folder.
2. **Cleans and filters** the dataset (e.g., removing invalid rows, filtering by criteria).
3. **Writes** the processed data to the `processed/` folder.
4. **Logs** each operation to CloudWatch for debugging and traceability.

---

### **Example Directory Flow**

```plaintext
S3 Bucket
│
├── raw/
│   └── Orders.csv  ← Upload here (triggers Lambda)
│
└── processed/
    └── Orders_Processed.csv  ← Lambda output
```

---

## ⚡ 4. Configure the S3 Trigger

### **Explanation**
The S3 Trigger connects your bucket to the Lambda function so that every time a new file is uploaded to the **raw/** folder, the Lambda automatically runs. This automation ensures **real-time data processing** without manual execution.

---

### **Steps to Configure the Trigger**

1. Open your **Lambda Function** in the AWS Console.
2. In the **Function Overview** section, click **+ Add Trigger**.
3. Configure the trigger as follows:
   - **Source:** Amazon S3
   - **Bucket:** Your project's S3 bucket name
   - **Event Type:** All object create events
   - **Prefix:** `raw/`
   - **Suffix:** `.csv`
4. Check the acknowledgment box confirming permissions for S3 to invoke Lambda.
5. Click **Add** to save the trigger.

After setting this up, **upload the Orders.csv file** into the `raw/` folder to test the pipeline. The Lambda function will process the data and output the cleaned file into the `processed/` folder.

---

### **Approach**
The S3 trigger implements an **event-driven workflow**, eliminating the need for periodic batch jobs. This ensures scalability and immediate response to new incoming data.

---

📸 **Screenshot - S3 Trigger Configuration**  
<img width="910" height="527" alt="Triggers" src="https://github.com/user-attachments/assets/5e84ed37-ebb9-4ff0-b094-ecd988da35ff" />


📸 **Screenshot - Processed CSV File in Processed Folder**  
<img width="1901" height="591" alt="S3processed" src="https://github.com/user-attachments/assets/ce822396-fb4b-45a9-b6fa-2f2f5c7e19d9" />
<img width="977" height="677" alt="S3processedcsvfile" src="https://github.com/user-attachments/assets/7326d748-b9df-41cd-9e37-887c7177fe33" />



---

## 🕸️ 5. AWS Glue Crawler

### **Explanation**
AWS Glue Crawlers automatically **discover and catalog** data stored in S3. They scan the processed data folder, identify its schema, and create a corresponding table inside the **Glue Data Catalog**, making it available for querying via Athena.

---

### **Steps to Create the Crawler**

1. Go to **AWS Glue Console → Crawlers → Create Crawler**.
2. **Name:** `orders_processed_crawler`
3. **Data Source:** Point to your **processed/** S3 folder.
4. **IAM Role:** Select the previously created `Glue-S3-Crawler-Role`.
5. **Output:**
   - Choose **Add database** → Create a new database named `orders_db`.
6. Finish the setup and **Run the crawler**.

After successful completion, you'll see a new table inside the **orders_db** database in the Glue Data Catalog.

---

### **Approach**
Using a crawler avoids manual schema definitions. It dynamically adapts to new data and ensures Athena always queries the most updated metadata.

---

📸 **Screenshot - Glue Crawler CloudWatch Logs**  
<img width="1896" height="743" alt="crawlerCloudWatch" src="https://github.com/user-attachments/assets/597ccd67-ed82-4c81-94a9-fdde183aec44" />


---

## 🔍 6. Query Data with Amazon Athena

### **Explanation**
Amazon Athena allows you to run **SQL queries directly on S3 data** using the Glue Data Catalog. It provides serverless, on-demand analytics without needing to provision or manage infrastructure.

---

### **Steps to Query the Data**

1. Navigate to the **Athena Console**.
2. Ensure:
   - **Data Source:** `AwsDataCatalog`
   - **Database:** `orders_db`
3. Open the **Query Editor** and run the following sample queries:

#### 💰 Total Sales by Customer
```sql
SELECT customer_id, SUM(total_amount) AS total_sales
FROM orders_processed
GROUP BY customer_id
ORDER BY total_sales DESC;
```

#### 📅 Monthly Order Volume and Revenue
```sql
SELECT date_format(order_date, '%Y-%m') AS month,
       COUNT(order_id) AS total_orders,
       SUM(total_amount) AS monthly_revenue
FROM orders_processed
GROUP BY month
ORDER BY month;
```

#### 🚚 Order Status Dashboard
```sql
SELECT status, COUNT(*) AS total_orders
FROM orders_processed
GROUP BY status;
```

#### 💵 Average Order Value (AOV) per Customer
```sql
SELECT customer_id,
       ROUND(AVG(total_amount), 2) AS avg_order_value
FROM orders_processed
GROUP BY customer_id;
```

#### 🏆 Top 10 Largest Orders in February 2025
```sql
SELECT * FROM orders_processed
WHERE month(order_date) = 2 AND year(order_date) = 2025
ORDER BY total_amount DESC
LIMIT 10;
```

---

### **Approach**

Athena transforms S3 into a queryable data lake, integrating seamlessly with Glue. This eliminates ETL overhead while providing quick business insights using standard SQL.
---

## 🖥️ 7. Launch EC2 Web Server

### **Explanation**
The EC2 instance hosts the **Flask web dashboard** that displays query results from Amazon Athena. This represents the final step in the AWS data pipeline — turning processed data into a visual, interactive web interface.

By integrating EC2 with IAM, Athena, and S3, the system remains **fully serverless, automated, and scalable**.

---

### **Steps to Launch and Configure the EC2 Instance**

1. Navigate to the **AWS EC2 Console** and click **Launch Instance**.
2. Configure your instance with the following details:
   - **Name:** `Athena-Dashboard-Server`
   - **AMI:** Amazon Linux 2023 (Free Tier eligible)
   - **Instance Type:** `t2.micro`
   - **Key Pair:** Create and download a `.pem` key file (store it securely)
3. Under **Network Settings → Edit**, configure the Security Group:
   - **Rule 1:** SSH — Port 22 — Source: *My IP*
   - **Rule 2:** Custom TCP — Port 5000 — Source: *Anywhere (0.0.0.0/0)*
4. In **Advanced Details → IAM Instance Profile**, select `EC2-Athena-Dashboard-Role`.
5. Click **Launch Instance** to create and start your server.

---

### **Connect to Your Instance**

From your terminal or command prompt:
```bash
ssh -i /path/to/your-key.pem ec2-user@YOUR_PUBLIC_IP_ADDRESS
```

---

### **⚙️ Install Required Dependencies**

Once your EC2 instance is launched and you've connected to it via SSH, you'll need to install the necessary software to run your Flask-based web dashboard.

#### **Step 1: Update System Packages**
Run the following command to ensure your instance has the latest updates:
```bash
sudo yum update -y
```

#### **Step 2: Install Python and Pip**
Install **Python 3** and **Pip** (Python's package manager):
```bash
sudo yum install python3-pip -y
```

After installation, verify that both Python and Pip are correctly installed:
```bash
python3 --version
pip3 --version
```

#### **Step 3: Install Flask and Boto3**
Install the required Python packages:
```bash
pip3 install Flask boto3
```

---

### **Create and Configure the Web Application**

Create the Flask application file:
```bash
nano app.py
```

Write your EC2 instance logic in the `app.py` file, then save and exit.

---

### **Run the App and View Your Dashboard**

Start the Flask application:
```bash
python3 app.py
```

Access your dashboard in a web browser:
```
http://YOUR_PUBLIC_IP_ADDRESS:5000
```

---

📸 **Screenshot - EC2 Dashboard Running**  
<img width="1630" height="808" alt="FinalOutputPage" src="https://github.com/user-attachments/assets/f30bb740-b964-46a7-a628-47e34d3451ae" />


---

## 🎯 Conclusion

This project successfully demonstrates a complete serverless data processing pipeline on AWS. The integration of S3, Lambda, Glue, Athena, and EC2 provides:

- **Automation:** Event-driven processing eliminates manual intervention
- **Scalability:** Serverless architecture handles varying workloads
- **Cost-Efficiency:** Pay only for resources used
- **Flexibility:** SQL-based analytics on raw S3 data
- **Visualization:** Web-based dashboard for business insights

---

## 📚 Technologies Used

- **AWS S3** - Object storage and data lake
- **AWS Lambda** - Serverless compute for data processing
- **AWS Glue** - Data cataloging and schema discovery
- **Amazon Athena** - Serverless SQL query engine
- **Amazon EC2** - Web server hosting
- **Python Flask** - Web application framework
- **Boto3** - AWS SDK for Python

---

## 👨‍💻 Author

**ITCS 6190/8190 - Cloud Computing for Data Analysis**  
Fall 2025

---

## 📝 License

This project is created for educational purposes as part of the ITCS-6190 course assignment.
