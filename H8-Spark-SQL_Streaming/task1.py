from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
import os
import shutil

# Clean up old checkpoint if exists
if os.path.exists("checkpoint_task1_clean"):
    shutil.rmtree("checkpoint_task1_clean")

# Create a Spark session
spark = SparkSession.builder \
    .appName("RideSharingAnalytics") \
    .master("local[2]") \
    .getOrCreate()

# Set log level
spark.sparkContext.setLogLevel("WARN")

print("=" * 70)
print("Task 1: Basic Streaming Ingestion and Parsing")
print("=" * 70)

# Define the schema for incoming JSON data
schema = StructType([
    StructField("trip_id", StringType(), True),
    StructField("driver_id", IntegerType(), True),
    StructField("distance_km", DoubleType(), True),
    StructField("fare_amount", DoubleType(), True),
    StructField("timestamp", StringType(), True)
])

# Read streaming data from socket
print("Connecting to socket localhost:9999...")
lines = spark.readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

print("✓ Connected to socket")

# Parse JSON data into columns using the defined schema
parsed_data = lines.select(
    from_json(col("value"), schema).alias("data")
).select("data.*")

# Convert timestamp string to TimestampType
parsed_data = parsed_data.withColumn(
    "timestamp", 
    to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss")
)

print("✓ Data parsing configured")
print("=" * 70)

# Define function to write each batch to CSV files
def write_batch_to_csv(batch_df, batch_id):
    """Write each micro-batch to CSV and display on console"""
    
    # Create output directory
    output_dir = "outputs/task1"
    os.makedirs(output_dir, exist_ok=True)
    
    if batch_df.isEmpty():
        print(f"Batch {batch_id}: No data")
        return
    
    # Define the full path for CSV output
    csv_path = os.path.join(output_dir, f"batch_{batch_id}")
    
    # Write to CSV with headers
    batch_df.coalesce(1) \
        .write \
        .mode("overwrite") \
        .option("header", "true") \
        .csv(csv_path)
    
    # Find the actual CSV file created (Spark creates a folder with part files)
    csv_files = [f for f in os.listdir(csv_path) if f.endswith('.csv')]
    if csv_files:
        actual_file = os.path.join(csv_path, csv_files[0])
        print(f"\n{'='*70}")
        print(f"BATCH {batch_id} PROCESSED")
        print(f"{'='*70}")
        print(f"✓ CSV saved to: {csv_path}/")
        print(f"✓ File: {csv_files[0]}")
        print(f"✓ Records: {batch_df.count()}")
        print("\nData Preview:")
        batch_df.show(truncate=False)
        print("-" * 70)
    else:
        print(f"Warning: CSV file not found in {csv_path}")

# Write parsed data to CSV files
query = parsed_data.writeStream \
    .foreachBatch(write_batch_to_csv) \
    .outputMode("append") \
    .trigger(processingTime='5 seconds') \
    .option("checkpointLocation", "./checkpoint_task1_clean") \
    .start()

print("✓ Streaming query started")
print("=" * 70)
print("OUTPUT:")
print("  - Console: Real-time display below")
print("  - CSV Files: outputs/task1/batch_X/")
print("=" * 70)
print("Waiting for data... (Press Ctrl+C to stop)\n")

try:
    query.awaitTermination()
except KeyboardInterrupt:
    print("\n" + "=" * 70)
    print("Stopping streaming query...")
    query.stop()
    spark.stop()
    print("✓ Stopped successfully")
    print("=" * 70)