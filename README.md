# FeatureFlux 

**FeatureFlux Enhanced** is a fully modular, scalable ML serving platform that integrates:
- **Neural Networks & Deep Learning** (PyTorch, TensorFlow)
- **Machine Learning** (scikit-learn, etc.)
- **Graphical Models & Statistical Analysis** (pgmpy, correlation, importance)
- **Distributed Systems & Big Data** (PySpark, Airflow, Hive)

## Features
- **Dynamic Feature Store**: Supports evolving schemas, tracks feature statistics, and provides versioning.
- **Automatic Model Training**: Trains a model on the first event if none exists, and retrains when new features are introduced.
- **Multiple Model Frameworks**: Use scikit-learn, PyTorch, or TensorFlow/Keras models with a unified interface.
- **Distributed Processing**: Batch and streaming ingestion using PySpark and Kafka.
- **REST API and CLI**: Interact with the platform via FastAPI and command-line tools.
- **Optional AWS Integration**: Easily switch to AWS services for storage and orchestration.

## Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -e .
