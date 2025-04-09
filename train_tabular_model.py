"""
train_tabular_model.py

This standalone script trains a tabular model (RandomForestClassifier from scikit-learn)
using the initial training data from 'src/models/tabular_model/training_data.csv'.
It then saves the trained model to 'src/models/tabular_model/tabular_model.pkl'.
"""

import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle

def main():
    base_dir = os.path.dirname(__file__)
    training_file = os.path.join(base_dir, "src", "models", "tabular_model", "training_data.csv")
    
    if not os.path.exists(training_file):
        print(f"Training file not found at {training_file}")
        return
    
    data = pd.read_csv(training_file)
    
    # Drop non-numeric columns if any exist (e.g., 'id' if it were there).
    numeric_data = data.select_dtypes(include=["number"])
    
    if numeric_data.shape[1] < 2:
        print("Insufficient data after dropping non-numeric columns.")
        return
    
    feature_columns = list(numeric_data.columns[:-1])
    target_column = numeric_data.columns[-1]
    
    X = numeric_data[feature_columns]
    y = numeric_data[target_column].astype(int)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy: {accuracy:.2f}")
    
    model_dir = os.path.join(base_dir, "src", "models", "tabular_model")
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "tabular_model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    
    print(f"Trained model saved to {model_path}")

if __name__ == "__main__":
    main()