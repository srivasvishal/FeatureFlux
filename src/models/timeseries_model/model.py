"""
model.py for timeseries_model

A dummy time series prediction model.
For illustration, it computes the average of the input series as the forecast.
In a real implementation, you might use ARIMA, LSTM, or another method.
"""

def predict(input_data: dict, features: dict = None):
    """
    Expects input_data to have key 'series' which is a list of numeric values.
    Returns the average as the forecast.
    """
    series = input_data.get("series", [])
    if not series:
        return {"error": "No series data provided"}
    try:
        # Compute the average as a dummy forecast.
        forecast = sum(series) / len(series)
    except Exception as e:
        return {"error": f"Error computing forecast: {e}"}
    return {"forecast": forecast}