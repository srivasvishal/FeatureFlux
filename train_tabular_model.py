import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import os

def main():
    # Load the dataset. Here we use the transactions.csv file.
    # Adjust the file path and columns as needed.
    data = pd.read_csv("data/transactions.csv")
    
    # For demonstration, let's assume the following:
    # Use 'transaction_amount' as a feature.
    # Create a dummy binary target: fraud = 1 if transaction_amount > 150, else 0.
    data['target'] = data['transaction_amount'].apply(lambda x: 1 if x > 150 else 0)
    
    # Define features (X) and target (y)
    X = data[['transaction_amount']]
    y = data['target']
    
    # Split the data into training and testing sets (optional)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create and train a RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate the model (optional)
    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy: {accuracy:.2f}")
    
    # Ensure the directory for the pickled model exists
    model_dir = os.path.join("src", "models", "tabular_model")
    os.makedirs(model_dir, exist_ok=True)
    
    # Save the trained model as tabular_model.pkl in the src/models/tabular_model folder
    model_path = os.path.join(model_dir, "tabular_model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    main()