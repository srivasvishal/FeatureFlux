import csv
import random
from datetime import datetime, timedelta

def generate_raw_data(filename, num_rows=100, num_entities=10):
    """
    Generates a raw CSV file with 100 rows of simulated transaction data.
    
    The file will have the following columns:
      - entity_id: an identifier for the entity (e.g., user)
      - feature1: a random float (simulating a numeric measurement)
      - feature2: a random float (simulating another measurement)
      - transaction_time: a timestamp of the transaction
      - details: a short description (categorical/free text)
      
    No target column is included, as this represents unprocessed, raw data.
    """
    # Base time for generating timestamps.
    base_time = datetime.now() - timedelta(days=30)
    
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        # Write the header row.
        writer.writerow(["entity_id", "feature1", "feature2", "transaction_time", "details"])
        
        for i in range(num_rows):
            # Cycle through a set of entity IDs (e.g., user_0 to user_9)
            entity_id = f"user_{i % num_entities}"
            # Generate random values for feature1 and feature2.
            feature1 = round(random.uniform(5.0, 10.0), 2)
            feature2 = round(random.uniform(3.0, 6.0), 2)
            # Generate a timestamp by adding a random number of minutes to the base_time.
            transaction_time = base_time + timedelta(minutes=random.randint(0, 43200))  # up to 30 days
            transaction_time_str = transaction_time.strftime("%Y-%m-%d %H:%M:%S")
            # Generate a random detail from a set of options.
            details = random.choice(["online", "in-store", "mobile", "web"])
            
            writer.writerow([entity_id, feature1, feature2, transaction_time_str, details])
    
    print(f"Generated {num_rows} rows of raw data in '{filename}'.")

if __name__ == "__main__":
    generate_raw_data("transactions_raw.csv")