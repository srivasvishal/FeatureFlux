"""
test_end_to_end.py

Integration tests for the entire pipeline.
This test simulates a full cycle: batch ingestion, sending an event, and prediction.
"""

import unittest
import json
from src.ingestion.batch_job import run_batch_job
from src.ingestion.producer import produce_events
from src.models import model_loader
from src.feature_store.store import RedisFeatureStore
import time

class TestEndToEnd(unittest.TestCase):
    def setUp(self):
        # Clear feature store before test.
        self.store = RedisFeatureStore(host="localhost", port=6379)
        self.store.client.flushdb()
        # Run batch ingestion to populate features from historical data.
        run_batch_job()
        # Give a small delay for batch job completion.
        time.sleep(2)

    def test_prediction_flow(self):
        # Simulate sending an event (here we call model_loader.predict directly)
        # In a full system, this would be sent via Kafka.
        entity_id = "user_1"
        # Example input from historical data; might match what batch_job ingested.
        input_data = {"feature1": 10, "feature2": 20}
        # Update feature store with new data.
        self.store.set_features(f"features:{entity_id}", input_data)
        result = model_loader.predict("tabular_model", input_data)
        self.assertIn("predicted_class", result)

if __name__ == "__main__":
    unittest.main()