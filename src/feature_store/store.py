import redis
import json
from abc import ABC, abstractmethod

class FeatureStore(ABC):
    @abstractmethod
    def get_features(self, entity_id):
        pass

    @abstractmethod
    def set_features(self, entity_id, features):
        pass

class RedisFeatureStore(FeatureStore):
    def __init__(self, host="localhost", port=6379):
        self.client = redis.Redis(host=host, port=port)

    def get_features(self, entity_id):
        data = self.client.hgetall(entity_id)
        return {k.decode('utf-8'): json.loads(v) for k, v in data.items()} if data else {}

    def set_features(self, entity_id, features):
        mapping = {k: json.dumps(v) for k, v in features.items()}
        self.client.hmset(entity_id, mapping)