"""
config.py

Defines global configuration variables.
You can modify these values or set corresponding environment variables.
"""

import os

# Use environment variables if set, else default values.
USE_AWS = os.environ.get("USE_AWS", "0") == "1"
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")  # In Docker, use 'redis'; local testing may override to 'localhost'
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
APP_MODE = os.environ.get("APP_MODE", "both")  # Could be 'api', 'consumer', or 'both'

# Other configurations can be added as needed.