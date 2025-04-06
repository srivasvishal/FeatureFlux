import os
import redis
import json
from kafka import KafkaConsumer
from models import model_loader

def consume_events():
    redis_host = os.environ.get("REDIS_HOST", "localhost")
    redis_client = redis.Redis(host=redis_host, port=6379)
    
    consumer = KafkaConsumer(
        "events",
        bootstrap_servers=["localhost:9092"],
        group_id="ml-serving-group",
        auto_offset_reset="latest"
    )
    print("Starting Kafka consumer...")
    for msg in consumer:
        try:
            event = json.loads(msg.value.decode('utf-8'))
            model_name = event.get("model_name")
            input_data = event.get("data")
            entity_id = event.get("entity_id")
            features = {}
            if entity_id:
                raw = redis_client.hgetall(f"features:{entity_id}")
                features = {k.decode('utf-8'): float(v.decode('utf-8')) for k, v in raw.items()} if raw else {}
            result = model_loader.predict(model_name, input_data, features)
            print(f"Inference result for {entity_id} using {model_name}: {result}")
        except Exception as e:
            print(f"Error processing event: {e}")

if __name__ == "__main__":
    consume_events()