"""
model.py for tabular_model

This module implements a tabular model using scikit-learn's RandomForestClassifier.
It is designed to:
  - Train on an initial CSV file.
  - When a new event arrives, append the new data to the CSV file.
  - Retrain the model using the updated CSV.
  - Then, perform prediction using the retrained model.

Note: Since no ground-truth target is available during inference,
we append new events with a default target value (0). In a real system,
you might use semi-supervised learning or wait for true labels.
"""

import os
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Global cache for the model
_model = None

# Set the directory containing the training CSV and model artifact.
BASE_DIR = os.path.dirname(__file__)
# Path to the training data CSV. It should be initially created with proper columns.
TRAINING_DATA_PATH = os.path.join(BASE_DIR, "training_data.csv")
# Path to save the trained model.
MODEL_PATH = os.path.join(BASE_DIR, "tabular_model.pkl")

def train_model():
    """
    Trains a RandomForestClassifier using data from TRAINING_DATA_PATH.
    
    Assumes that the CSV file has the feature columns followed by the target column.
    Returns the trained model.
    """
    if not os.path.exists(TRAINING_DATA_PATH):
        raise FileNotFoundError(f"Training data not found at {TRAINING_DATA_PATH}")
    
    # Load training data from CSV into a pandas DataFrame.
    data = pd.read_csv(TRAINING_DATA_PATH)
    
    # Ensure that there is at least one feature column and one target column.
    if data.shape[1] < 2:
        raise ValueError("Training data must have at least one feature column and one target column.")
    
    # Assume the last column is the target.
    feature_columns = list(data.columns[:-1])
    target_column = data.columns[-1]
    
    # Extract features (X) and target (y) from the DataFrame.
    X = data[feature_columns]
    y = data[target_column]
    
    # Train the RandomForestClassifier.
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Store the order of features in the model so that predictions are made correctly.
    model.feature_names_in_ = feature_columns
    
    # Save the trained model to disk using pickle.
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    
    print(f"Model trained with features {feature_columns} and saved to {MODEL_PATH}")
    return model

def load_model():
    """
    Loads the model from disk if available; otherwise, trains a new model.
    """
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            print("No pre-trained model found. Training new model...")
            _model = train_model()
        else:
            with open(MODEL_PATH, "rb") as f:
                _model = pickle.load(f)
            if not hasattr(_model, "feature_names_in_"):
                raise ValueError("Loaded model does not have stored feature names.")
            print(f"Loaded pre-trained model with features: {_model.feature_names_in_}")
    return _model

def update_training_data(new_record: dict, target_value=0):
    """
    Updates the training data CSV by appending a new record.
    This function removes keys that represent identifiers or metadata 
    (e.g., 'entity_id', 'user_id', 'timestamp', 'time', 'date', 'details')
    so that only numeric features are stored for training.
    
    Parameters:
      new_record: dict containing the new event's data.
      target_value: default target value (used during inference).
    """
    # Define keys to be removed (case-insensitive)
    keys_to_remove = {"entity_id", "user_id", "timestamp", "time", "date", "details"}
    
    # Remove keys that are in our removal set (using lowercasing to be safe)
    for key in list(new_record.keys()):
        if key.lower() in keys_to_remove:
            new_record.pop(key)
    
    # Now, build a new record containing only values that can be converted to float.
    numeric_record = {}
    for key, value in new_record.items():
        try:
            numeric_record[key] = float(value)
        except (ValueError, TypeError):
            print(f"Warning: Skipping non-numeric key '{key}' with value '{value}'.")
            continue

    # Append the target value.
    numeric_record['target'] = target_value

    # Load existing training data if available; otherwise, create an empty DataFrame.
    if os.path.exists(TRAINING_DATA_PATH):
        df = pd.read_csv(TRAINING_DATA_PATH)
    else:
        df = pd.DataFrame()

    # Create a DataFrame for the new record.
    new_df = pd.DataFrame([numeric_record])
    
    # Ensure both DataFrames have the same columns.
    for col in new_df.columns:
        if col not in df.columns:
            df[col] = 0
    for col in df.columns:
        if col not in new_df.columns:
            new_df[col] = 0

    # Append the new record and save the updated CSV.
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(TRAINING_DATA_PATH, index=False)
    print(f"Updated training data with new record: {numeric_record}")
    
def predict(input_data: dict, features: dict = None):
    """
    Makes a prediction using the tabular model.
    
    Workflow:
      1. Update the training CSV with the new input_data (with a default target of 0).
      2. Retrain the model using the updated training data.
      3. Use the retrained model to predict the outcome for the input_data.
    
    Parameters:
      input_data: dict containing feature values for prediction.
      features: (optional) additional features (not used here).
    
    Returns:
      A dict containing the prediction result.
    """
    # Update the training data CSV with the new event.
    update_training_data(new_record=input_data, target_value=0)
    # Retrain the model with the updated training data.
    model = train_model()
    # Build the input vector using the model's expected feature order.
    X_new = [[input_data.get(feat, 0) for feat in model.feature_names_in_]]
    prediction = model.predict(X_new)
    return {"predicted_class": int(prediction[0])}