import unittest
from feature_store.store import RedisFeatureStore

class TestFeatureStore(unittest.TestCase):
    def setUp(self):
        self.store = RedisFeatureStore(host="localhost", port=6379)
        self.store.client.flushdb()

    def test_set_and_get_features(self):
        entity_id = "features:generic_entity"
        features = {"feature1": 123, "feature2": "example", "feature3": 4.56, "feature4": True}
        self.store.set_features(entity_id, features)
        result = self.store.get_features(entity_id)
        self.assertEqual(result, features)

if __name__ == "__main__":
    unittest.main()