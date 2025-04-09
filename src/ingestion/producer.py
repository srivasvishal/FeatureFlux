"""
producer.py

A Kafka producer that sends streaming events.
Each event is a JSON message with keys:
- model_name: Name of the model to be used.
- entity_id: Identifier for the entity.
- data: A dict of features.
"""

import json
import time
from kafka import KafkaProducer
from config import KAFKA_BOOTSTRAP_SERVERS

def produce_events():
    # Initialize KafkaProducer with JSON serialization.
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    topic = "events"
    count = 0
    while True:
        # For demonstration, alternate between two types of events.
        if count % 2 == 0:
            event = {
                "entity_id": f"user_{count % 3}",
                "model_name": "tabular_model",
                "data": {
                    "feature1": 10 + count,
                    "feature2": 20 + count
                }
            }
        else:
            # Introduce an extra feature on odd counts to simulate schema evolution.
            event = {
                "entity_id": f"user_{count % 3}",
                "model_name": "tabular_model",
                "data": {
                    "feature1": 10 + count,
                    "feature2": 20 + count,
                    "feature3": 30 + count  # New feature introduced
                }
            }
        # Send the event to Kafka topic "events"
        producer.send(topic, event)
        print(f"Sent event: {event}")
        count += 1
        time.sleep(3)  # Wait 3 seconds between events

if __name__ == "__main__":
    produce_events()