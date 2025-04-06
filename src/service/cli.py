import argparse
import json
from models import model_loader
import redis
from kafka import KafkaProducer

def predict_cli(model_name, input_data, entity_id=None):
    redis_client = redis.Redis(host="localhost", port=6379)
    features = {}
    if entity_id:
        raw = redis_client.hgetall(f"features:{entity_id}")
        features = {k.decode('utf-8'): float(v.decode('utf-8')) for k, v in raw.items()} if raw else {}
    result = model_loader.predict(model_name, input_data, features)
    print("Prediction result:", result)

def send_event_cli(model_name, input_data, entity_id=None):
    producer = KafkaProducer(bootstrap_servers=["localhost:9092"],
                            value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    event = {"model_name": model_name, "data": input_data}
    if entity_id:
        event["entity_id"] = entity_id
    producer.send("events", event)
    producer.flush()
    print("Event sent to Kafka.")

def main():
    parser = argparse.ArgumentParser(prog="featureflux-cli")
    subparsers = parser.add_subparsers(dest="command")

    pred_parser = subparsers.add_parser("predict", help="Run a prediction")
    pred_parser.add_argument("--model", required=True, help="Model name")
    pred_parser.add_argument("--input", required=True, help="Input data (JSON string)")
    pred_parser.add_argument("--entity", help="Entity ID for feature lookup")

    evt_parser = subparsers.add_parser("send-event", help="Send event to Kafka")
    evt_parser.add_argument("--model", required=True, help="Model name")
    evt_parser.add_argument("--input", required=True, help="Input data (JSON string)")
    evt_parser.add_argument("--entity", help="Entity ID")

    args = parser.parse_args()
    if args.command == "predict":
        predict_cli(args.model, json.loads(args.input), args.entity)
    elif args.command == "send-event":
        send_event_cli(args.model, json.loads(args.input), args.entity)

if __name__ == "__main__":
    main()