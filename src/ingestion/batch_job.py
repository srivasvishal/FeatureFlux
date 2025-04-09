
"""
batch_job.py

This script reads raw historical data from the transactions.csv file located in the data/ folder,
processes (aggregates) the data per entity, writes the processed data to a training file
(in src/models/tabular_model/training_data.csv), and updates the online feature store (Redis)
with these aggregated features.
"""

import os
import pandas as pd
from feature_store.store import RedisFeatureStore

def run_batch_job():
    # Construct the absolute path to the raw CSV file.
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    raw_csv_path = os.path.join(base_dir, "data", "transactions.csv")
    print(f"Reading raw CSV file from: {raw_csv_path}")
    
    # Load the raw data.
    df = pd.read_csv(raw_csv_path)
    
    # Ensure the CSV contains the 'entity_id' column.
    if "entity_id" not in df.columns:
        print("CSV must contain 'entity_id' column.")
        return
    
    # Drop the identifier column for training purposes.
    df_numeric = df.drop(columns=["entity_id"])
    
    # Identify numeric columns (should be all columns now if target is numeric).
    numeric_cols = df_numeric.select_dtypes(include=["number"]).columns.tolist()
    
    # Group by a common key if needed—here we assume that historical aggregation isn't required.
    # If you want to aggregate per entity, you may need to retain the id temporarily,
    # then drop it after aggregation.
    # For this example, we assume you simply want the raw numeric data for training.
    
    # Write the processed data to the training file.
    training_data_path = os.path.join(base_dir, "src", "models", "tabular_model", "training_data.csv")
    df_numeric.to_csv(training_data_path, index=False)
    print(f"Processed training data written to: {training_data_path}")
    
    # Optionally, update the online feature store for each row (if desired).
    store = RedisFeatureStore()
    for idx, row in df.iterrows():
        entity_id = row["entity_id"]
        # Use the numeric version for features.
        features = row.drop("entity_id").to_dict()
        store.set_features(f"features:{entity_id}", features)
        print(f"Updated feature store for {entity_id}: {features}")

if __name__ == "__main__":
    run_batch_job()