"""
cli.py

A command-line interface (CLI) for interacting with the FeatureFlux system.
It uses argparse to define commands for sending events and testing predictions.
"""

import argparse
import json
from ingestion.producer import produce_events
from models import model_loader
from feature_store.store import RedisFeatureStore

def send_event(model, input_data, entity):
    """
    Sends an event using the producer logic.
    Here we simulate the sending by directly calling the consumer logic.
    (In a full system, this would publish to Kafka.)
    """
    # For demonstration, update the feature store and perform prediction.
    store = RedisFeatureStore()
    store.set_features(f"features:{entity}", input_data)
    print(f"Event sent for {entity} with data: {input_data}")
    result = model_loader.predict(model, input_data)
    print(f"Prediction result: {result}")

def main():
    parser = argparse.ArgumentParser(description="FeatureFlux CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command to send an event
    send_parser = subparsers.add_parser("send-event", help="Send a test event")
    send_parser.add_argument("--model", required=True, help="Model name (e.g., tabular_model)")
    send_parser.add_argument("--input", required=True, help="Input data as JSON string")
    send_parser.add_argument("--entity", required=True, help="Entity ID for the event")

    # Command to start the producer (continuous event production)
    prod_parser = subparsers.add_parser("produce-events", help="Start continuous event production")

    args = parser.parse_args()

    if args.command == "send-event":
        try:
            input_data = json.loads(args.input)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON input: {e}")
            return
        send_event(args.model, input_data, args.entity)
    elif args.command == "produce-events":
        produce_events()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()