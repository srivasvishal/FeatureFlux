import torch
import torch.nn as nn
import pandas as pd
import numpy as np

class LSTMForecast(nn.Module):
    def __init__(self, input_size=1, hidden_size=32):
        super(LSTMForecast, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.linear = nn.Linear(hidden_size, 1)

    def forward(self, x):
        output, _ = self.lstm(x)
        return self.linear(output[:, -1, :])

model = LSTMForecast()
model.load_state_dict(torch.load('lstm_model.pth'))
model.eval()

def predict_timeseries(csv_path):
    data = pd.read_csv(csv_path)
    inputs = torch.tensor(data.values, dtype=torch.float32).unsqueeze(0)
    with torch.no_grad():
        prediction = model(inputs).item()
    return prediction

if __name__ == "__main__":
    print(predict_timeseries('sample_input.csv'))