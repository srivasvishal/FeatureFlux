"""
model.py for keras_model

A simple Keras model example for demonstration.
It defines a Sequential model and a predict() function.
For training, it uses model.fit() and saves the model; for inference, it loads the model.
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model as keras_load_model
from tensorflow.keras.layers import Dense
import pickle

# Define paths for saving the model.
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "keras_model.h5")

def train_model():
    """
    Trains a simple Keras Sequential model on dummy data.
    In a real scenario, replace this with your own training pipeline.
    """
    # Generate dummy data: 100 samples, 3 features.
    X = np.random.rand(100, 3)
    y = (np.sum(X, axis=1) > 1.5).astype(int)  # Binary target.
    
    model = Sequential([
        Dense(16, activation='relu', input_shape=(3,)),
        Dense(8, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X, y, epochs=10, batch_size=8, verbose=1)
    
    # Save the model
    model.save(MODEL_PATH)
    print(f"Keras model trained and saved to {MODEL_PATH}")
    return model

def load_model():
    """
    Loads the Keras model if it exists, else trains a new one.
    """
    if not os.path.exists(MODEL_PATH):
        print("No pre-trained Keras model found, training a new one...")
        return train_model()
    else:
        model = keras_load_model(MODEL_PATH)
        print("Loaded pre-trained Keras model.")
        return model

def predict(input_data: dict, features: dict = None):
    """
    Uses the Keras model to make a prediction.
    Expects input_data to have 3 features (as a list).
    """
    model = load_model()
    # Expecting input_data to be like: {"features": [val1, val2, val3]}
    features_list = input_data.get("features")
    if not features_list or len(features_list) != 3:
        return {"error": "Expected 'features' to be a list of 3 numeric values."}
    
    # Convert to numpy array with shape (1, 3)
    X_new = np.array([features_list])
    pred = model.predict(X_new)
    # Convert sigmoid output to binary prediction.
    predicted_class = 1 if pred[0][0] >= 0.5 else 0
    return {"predicted_class": predicted_class, "raw_output": float(pred[0][0])}