"""
store.py

Defines the FeatureStore interface and implements RedisFeatureStore.
"""

import redis
import json
from abc import ABC, abstractmethod
from config import REDIS_HOST

class FeatureStore(ABC):
    @abstractmethod
    def get_features(self, entity_id: str) -> dict:
        """Retrieve features for the given entity_id."""
        pass

    @abstractmethod
    def set_features(self, entity_id: str, features: dict):
        """Store features for the given entity_id."""
        pass

class RedisFeatureStore(FeatureStore):
    def __init__(self, host=REDIS_HOST, port=6379):
        # Initialize Redis connection using the redis-py client.
        self.client = redis.Redis(host=host, port=port, decode_responses=True)

    def get_features(self, entity_id: str) -> dict:
        # Get all fields in the Redis hash for the entity.
        data = self.client.hgetall(entity_id)
        # Convert stored strings to float if possible.
        # (In a robust implementation, you might store type information.)
        result = {}
        for k, v in data.items():
            try:
                result[k] = float(v)
            except ValueError:
                result[k] = v
        return result

    def set_features(self, entity_id: str, features: dict):
        # Convert features to JSON strings if necessary, then update Redis hash.
        # Here, we simply convert numeric values to string.
        mapping = {k: str(v) for k, v in features.items()}
        self.client.hmset(entity_id, mapping)