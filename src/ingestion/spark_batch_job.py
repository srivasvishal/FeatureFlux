"""
spark_batch_job.py

A PySpark-based batch ingestion script for large-scale data.
It reads a CSV file, aggregates features per entity, and updates the feature store.
This version is domain-independent and computes the average for all numeric columns.
"""

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg
from feature_store.store import RedisFeatureStore

def run_spark_batch_job(entity_key="entity_id", input_file="data/transactions.csv"):
    # Initialize SparkSession in local mode.
    spark = SparkSession.builder.appName("FeatureFluxSparkBatchJob").getOrCreate()
    
    # Compute the absolute path to the input CSV file.
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    csv_path = os.path.join(base_dir, input_file)
    print(f"Reading CSV file from: {csv_path}")
    
    # Read CSV file with header and infer schema.
    df = spark.read.csv(csv_path, header=True, inferSchema=True)
    
    if entity_key not in df.columns:
        print(f"Error: '{entity_key}' column not found in CSV.")
        spark.stop()
        return
    
    # Aggregate: compute average of all numeric columns (except the entity key)
    numeric_cols = [col for col, dtype in df.dtypes if dtype in ("int", "bigint", "double", "float") and col != entity_key]
    agg_expr = {col: "avg" for col in numeric_cols}
    agg_df = df.groupBy(entity_key).agg(agg_expr)
    
    # Convert aggregated DataFrame to Pandas for simplicity.
    pandas_df = agg_df.toPandas()
    
    # Update Redis feature store.
    store = RedisFeatureStore()
    for _, row in pandas_df.iterrows():
        entity = row[entity_key]
        # Build a dictionary of aggregated features (convert column names appropriately)
        features = {col.replace("avg(", "").replace(")", ""): float(row[col]) for col in row.index if col != entity_key}
        store.set_features(f"features:{entity}", features)
        print(f"Updated features for {entity}: {features}")
    
    spark.stop()

if __name__ == "__main__":
    run_spark_batch_job()