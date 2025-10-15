# Import the necessary libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    from_json, col, sum as spark_sum, window, to_timestamp
)
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
import os

# Create a Spark session
spark = SparkSession.builder \
    .appName("RideSharingWindowedAnalytics") \
    .master("local[2]") \
    .config("spark.sql.streaming.checkpointLocation", "./checkpoint_task3") \
    .getOrCreate()

# Set log level to reduce noise
spark.sparkContext.setLogLevel("WARN")

print("Spark Session Created Successfully - Task 3: Windowed Analytics")
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

print("Socket connection established")

# Parse JSON data into columns using the defined schema
parsed_data = lines.select(
    from_json(col("value"), schema).alias("data")
).select("data.*")

# Convert timestamp column to TimestampType and add a watermark
parsed_data = parsed_data.withColumn(
    "event_time", 
    to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss")
)

# Add watermark of 1 minute to handle late-arriving data
watermarked_data = parsed_data.withWatermark("event_time", "1 minute")

print("Watermark configured: 1 minute")

# Perform windowed aggregation: sum of fare_amount over a 5-minute window sliding by 1 minute
windowed_aggregation = watermarked_data.groupBy(
    window(col("event_time"), "5 minutes", "1 minute")
).agg(
    spark_sum("fare_amount").alias("total_fare")
)

# Extract window start and end times as separate columns
windowed_results = windowed_aggregation.select(
    col("window.start").alias("window_start"),
    col("window.end").alias("window_end"),
    col("total_fare").cast("decimal(10,2)").alias("total_fare")
)

print("Windowed aggregation configured:")
print("  - Window size: 5 minutes")
print("  - Slide interval: 1 minute")
print("  - Watermark: 1 minute")
print("=" * 70)

# Define a function to write each batch to a CSV file with column names
def write_to_csv(batch_df, batch_id):
    """Write each micro-batch to a CSV file with headers"""
    output_dir = "outputs/task_3"
    os.makedirs(output_dir, exist_ok=True)
    batch_file = os.path.join(output_dir, f"windowed_batch_{batch_id}.csv")
    
    # Only write if the batch has data
    if batch_df.count() > 0:
        # Save the batch DataFrame as a CSV file with headers included
        batch_df.coalesce(1).write.mode("overwrite").option("header", True).csv(batch_file)
        
        print(f"\n✓ Batch {batch_id} written to {batch_file}")
        print(f"  Records in batch: {batch_df.count()}")
        print("\n  Window Summary:")
        batch_df.show(truncate=False)
        print("-" * 70)
    else:
        print(f"  Batch {batch_id} is empty, skipping...")

# Use foreachBatch to apply the function to each micro-batch
query = windowed_results.writeStream \
    .foreachBatch(write_to_csv) \
    .outputMode("append") \
    .trigger(processingTime='10 seconds') \
    .start()

print("Streaming query is running. Press Ctrl+C to stop.")
print("Output files will be saved in: outputs/task_3/")
print("=" * 70)
print("\nEach window shows the total fare for trips within that 5-minute period.")
print("Windows slide by 1 minute, so trips may appear in multiple windows.\n")

try:
    query.awaitTermination()
except KeyboardInterrupt:
    print("\n" + "=" * 70)
    print("Stopping streaming query...")
    query.stop()
    spark.stop()
    print("Streaming stopped successfully")