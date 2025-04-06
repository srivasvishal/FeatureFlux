import pandas as pd
from tensorflow.keras.models import load_model

model = load_model('keras_model.h5')

def predict_keras(csv_path):
    data = pd.read_csv(csv_path).values
    predictions = model.predict(data)
    return predictions.flatten().tolist()

if __name__ == "__main__":
    print(predict_keras('sample_input.csv'))