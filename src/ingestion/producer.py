from kafka import KafkaProducer
import json
import time

def produce_events():
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    topic = 'events'
    count = 0
    while True:
        if count % 2 == 0:
            data = {
                "entity_id": f"user_{count % 3}",
                "model_name": "sentiment_model",
                "data": {"text": "I love this product!"}
            }
        else:
            data = {
                "entity_id": f"user_{count % 3}",
                "model_name": "tabular_model",
                "data": {"featureX": count, "featureY": count * 2}
            }
        producer.send(topic, data)
        print(f"Sent event: {data}")
        count += 1
        time.sleep(1)

if __name__ == "__main__":
    produce_events()