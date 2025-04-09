"""
test_feature_store.py

Unit tests for the FeatureStore implementation.
"""

import unittest
from src.feature_store.store import RedisFeatureStore

class TestFeatureStore(unittest.TestCase):
    def setUp(self):
        # Create a RedisFeatureStore instance.
        self.store = RedisFeatureStore(host="localhost", port=6379)
        # Clear the store before each test.
        self.store.client.flushdb()

    def test_set_and_get_features(self):
        entity_id = "features:test_entity"
        features = {"feature1": 123, "feature2": 4.56, "feature3": 0.0}
        self.store.set_features(entity_id, features)
        result = self.store.get_features(entity_id)
        self.assertEqual(result, features)

if __name__ == "__main__":
    unittest.main()