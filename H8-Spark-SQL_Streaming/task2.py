from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, avg, sum as spark_sum, window, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
import os

# Create a Spark session
spark = SparkSession.builder \
    .appName("RideSharingAggregation") \
    .master("local[2]") \
    .config("spark.sql.streaming.checkpointLocation", "./checkpoint_task2") \
    .getOrCreate()

# Set log level to reduce noise
spark.sparkContext.setLogLevel("WARN")

print("Spark Session Created Successfully")
print("=" * 50)

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
    "timestamp", 
    to_timestamp(col("timestamp"), "yyyy-MM-dd HH:mm:ss")
)

# Add watermark to handle late data (10 seconds tolerance)
watermarked_data = parsed_data.withWatermark("timestamp", "10 seconds")

# Compute aggregations: total fare and average distance grouped by driver_id
aggregated_data = watermarked_data.groupBy("driver_id").agg(
    spark_sum("fare_amount").alias("total_fare"),
    avg("distance_km").alias("avg_distance")
)

# Round the aggregated values for better readability
aggregated_data = aggregated_data.withColumn(
    "total_fare", col("total_fare").cast("decimal(10,2)")
).withColumn(
    "avg_distance", col("avg_distance").cast("decimal(10,2)")
)

print("Starting streaming query with aggregations...")
print("=" * 50)

# Define a function to write each batch to a CSV file
def write_to_csv(batch_df, batch_id):
    """Write each micro-batch to a CSV file"""
    output_dir = "outputs/task_2"
    os.makedirs(output_dir, exist_ok=True)
    batch_file = os.path.join(output_dir, f"batch_{batch_id}.csv")
    
    # Only write if the batch has data
    if batch_df.count() > 0:
        batch_df.coalesce(1).write.mode("overwrite").option("header", True).csv(batch_file)
        print(f"✓ Batch {batch_id} written to {batch_file}")
        print(f"  Records: {batch_df.count()}")
        batch_df.show(truncate=False)
    else:
        print(f"  Batch {batch_id} is empty, skipping...")

# Use foreachBatch to apply the function to each micro-batch
query = aggregated_data.writeStream \
    .foreachBatch(write_to_csv) \
    .outputMode("complete") \
    .trigger(processingTime='5 seconds') \
    .start()

print("Streaming query is running. Press Ctrl+C to stop.")
print("Output files will be saved in: outputs/task_2/")
print("=" * 50)

try:
    query.awaitTermination()
except KeyboardInterrupt:
    print("\n" + "=" * 50)
    print("Stopping streaming query...")
    query.stop()
    spark.stop()
    print("Streaming stopped successfully")