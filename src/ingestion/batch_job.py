import pandas as pd
import redis
import os

def run_batch_job():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    csv_path = os.path.join(base_dir, "data", "transactions.csv")
    print(f"Reading CSV file from: {csv_path}")
    df = pd.read_csv(csv_path)
    agg = df.groupby("user_id").agg(
        avg_transaction_amount=("transaction_amount", "mean"),
        transaction_count=("transaction_amount", "count")
    ).reset_index()
    r = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=6379)
    for index, row in agg.iterrows():
        key = f"features:{row['user_id']}"
        r.hset(key, mapping={
            "avg_transaction_amount": float(row["avg_transaction_amount"]),
            "transaction_count": int(row["transaction_count"])
        })
        print(f"Updated features for {row['user_id']}")

if __name__ == "__main__":
    run_batch_job()