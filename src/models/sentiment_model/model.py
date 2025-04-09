"""
model.py for sentiment_model

This is a simple sentiment analysis model.
For demonstration, it uses a TF-IDF vectorizer and logistic regression.
In a production system, you might replace this with a deep learning model.
"""

import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Global cache for model and vectorizer.
_model = None
_vectorizer = None

# Define paths relative to this file.
BASE_DIR = os.path.dirname(__file__)
TRAINING_DATA_PATH = os.path.join(BASE_DIR, "training_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "sentiment_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "tfidf_vectorizer.pkl")

def train_model():
    """
    Trains a sentiment model using training data.
    Assumes training_data.csv has columns: text,target
    """
    if not os.path.exists(TRAINING_DATA_PATH):
        raise FileNotFoundError(f"Training data not found at {TRAINING_DATA_PATH}")
    
    data = pd.read_csv(TRAINING_DATA_PATH)
    if "text" not in data.columns or "target" not in data.columns:
        raise ValueError("Training data must contain 'text' and 'target' columns.")
    
    texts = data["text"]
    y = data["target"]
    
    # Train TF-IDF vectorizer
    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform(texts)
    
    # Train a Logistic Regression model.
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    
    # Save both the vectorizer and model.
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)
    
    global _model, _vectorizer
    _model = model
    _vectorizer = vectorizer
    print("Sentiment model trained and saved.")
    return model

def load_model():
    """
    Loads the sentiment model and vectorizer from disk, or trains a new one if not found.
    """
    global _model, _vectorizer
    if _model is None or _vectorizer is None:
        if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
            print("No pre-trained sentiment model found. Training a new model...")
            train_model()
        else:
            with open(MODEL_PATH, "rb") as f:
                _model = pickle.load(f)
            with open(VECTORIZER_PATH, "rb") as f:
                _vectorizer = pickle.load(f)
            print("Loaded pre-trained sentiment model.")
    return _model, _vectorizer

def predict(input_data: dict, features: dict = None):
    """
    Predict sentiment from the input text.
    Expects input_data to have key 'text'.
    """
    model, vectorizer = load_model()
    text = input_data.get("text", "")
    if not text:
        return {"error": "No text provided"}
    X = vectorizer.transform([text])
    prediction = model.predict(X)
    # Return prediction as 0 or 1, or map to sentiment label if desired.
    label = "positive" if prediction[0] == 1 else "negative"
    return {"predicted_sentiment": label}