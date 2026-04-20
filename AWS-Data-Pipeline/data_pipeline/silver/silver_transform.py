from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Create Spark session
spark = SparkSession.builder \
    .appName("Uber Silver Layer") \
    .getOrCreate()

# Path to Bronze Data (LOCAL or S3)
BRONZE_PATH = "data/bronze/"
# If S3 doesn't work, download locally and use:
# BRONZE_PATH = "data/bronze/"

# Read JSON files
df = spark.read.json(BRONZE_PATH)

print("Schema:")
df.printSchema()

print("Sample Data:")
df.show(5, truncate=False)

# Basic Cleaning (example)
df_clean = df.dropDuplicates(["ride_id"])

# Add derived column
df_clean = df_clean.withColumn(
    "ride_value_category",
    when(col("total_fare") > 100, "High")
    .when(col("total_fare") > 50, "Medium")
    .otherwise("Low")
)

# Write to Silver Layer
SILVER_PATH = "s3a://uber-data-lake-pooja/silver/obt/"

df_clean.write \
    .mode("overwrite") \
    .parquet(SILVER_PATH)

print("Silver layer written successfully")