# Handson-L10-Spark-Streaming-MachineLearning-MLlib
# Spark Structured Streaming with MLlib - Real-Time Ride-Sharing Analytics

## 📋 Overview
Real-time analytics pipeline for ride-sharing platform using Apache Spark Structured Streaming and MLlib for fare prediction and trend analysis.

## 📁 Project Structure
```
├── models/
│   ├── fare_model/
│   └── fare_trend_model_v2/
├── data_generator.py
├── task4.py
├── task5.py
├── training-dataset.csv
└── README.md
```

## 🎯 Tasks

### Task 4: Real-Time Fare Prediction
- Trains LinearRegression model on `distance_km` → `fare_amount`
- Predicts fares for streaming rides in real-time
- Calculates deviation to detect anomalies

### Task 5: Time-Based Fare Trend Prediction
- Aggregates data into 5-minute windows
- Engineers temporal features: `hour_of_day`, `minute_of_hour`
- Predicts average fare trends over time windows

## 🚀 How to Run

1. **Start Data Generator**
```bash
python data_generator.py
```

2. **Run Task 4**
```bash
spark-submit task4.py
```

3. **Run Task 5**
```bash
spark-submit task5.py
```

## 📊 Sample Outputs

### Task 4: Fare Prediction
```
Batch: 1
+------------------------------------+---------+-----------+-----------+----------------+--------------------+
|trip_id                             |driver_id|distance_km|fare_amount|predicted_fare  |deviation           |
+------------------------------------+---------+-----------+-----------+----------------+--------------------+
|aeb1ec42-0472-4ea3-bbb7-4f25fa99d4b0|1        |36.63      |115.23     |89.14           |26.08               |
|ee201927-f876-434c-8201-fbf347d0d43d|55       |36.95      |66.49      |89.07           |22.58               |
+------------------------------------+---------+-----------+-----------+----------------+--------------------+
```

### Task 5: Fare Trend Prediction
```
Batch: 7
+-------------------+-------------------+------------------+----------------------+
|window_start       |window_end         |avg_fare          |predicted_next_avg_fare|
+-------------------+-------------------+------------------+----------------------+
|2025-10-21 17:23:00|2025-10-21 17:28:00|78.88             |92.39                 |
+-------------------+-------------------+------------------+----------------------+
```

## 🛠️ Tech Stack
- Apache Spark (Structured Streaming + MLlib)
- Python 3.x
- LinearRegression Model
- Socket Streaming (localhost:9999)

## 📸 Screenshots


### Task 4 Output


### Task 4 Data Stream




### Task 5 Output


### Task 5 Data Stream



---
*Apache Spark + MLlib real-time ML pipeline*
