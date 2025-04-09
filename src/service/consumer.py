"""
consumer.py

A Kafka consumer that listens to the 'events' topic, updates the feature store,
and triggers model prediction.
"""

import json
from kafka import KafkaConsumer
from config import KAFKA_BOOTSTRAP_SERVERS
from feature_store.store import RedisFeatureStore
from models import model_loader

def consume_events():
    # Initialize Redis Feature Store; in Docker, host may be 'redis'; locally, set environment accordingly.
    store = RedisFeatureStore()
    
    # Initialize Kafka consumer with given bootstrap servers.
    consumer = KafkaConsumer(
        "events",
        bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
        group_id="ml-serving-group",
        auto_offset_reset="latest",
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    print("Starting Kafka consumer...")
    for msg in consumer:
        try:
            event = msg.value
            model_name = event.get("model_name")
            entity_id = event.get("entity_id")
            data = event.get("data")
            
            # Update feature store with the new data.
            store.set_features(f"features:{entity_id}", data)
            print(f"Updated feature store for {entity_id} with data: {data}")
            
            # Perform prediction using the dynamic model loader.
            result = model_loader.predict(model_name, data)
            print(f"Inference result for {entity_id} using {model_name}: {result}")
        except Exception as e:
            print(f"Error processing event: {e}")

if __name__ == "__main__":
    consume_events()