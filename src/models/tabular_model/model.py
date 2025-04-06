import pickle
import os

# Global variable to cache the model once loaded
_model = None

def load_model():
    global _model
    if _model is None:
        model_path = os.path.join(os.path.dirname(__file__), "tabular_model.pkl")
        with open(model_path, "rb") as f:
            _model = pickle.load(f)
    return _model

def predict(input_data, features=None):
    model = load_model()
    # Assume input_data is a dict containing a numeric value for 'transaction_amount'
    try:
        transaction_amount = float(input_data.get("transaction_amount", 0))
    except ValueError:
        return {"error": "Invalid transaction amount"}
    
    # Scikit-learn models expect a 2D array: [[value]]
    prediction = model.predict([[transaction_amount]])
    return {"predicted_class": int(prediction[0])}