"""
model_loader.py

Uses Python’s importlib to dynamically load the module corresponding to the model name
Dynamically loads a model module based on the provided model name.
It caches loaded modules to avoid repeated imports.
"""

import importlib

_loaded_models = {}

def predict(model_name: str, input_data, features: dict = None):
    """
    Loads the specified model module (e.g., 'tabular_model') and calls its predict function.
    
    Parameters:
      model_name: The name of the model to load (should correspond to a subpackage under models/).
      input_data: A dict of features from the incoming event.
      features: Optional additional features (e.g., from the feature store).
      
    Returns:
      The prediction result as a dict.
    """
    if model_name not in _loaded_models:
        try:
            # Dynamically import the model module from the models package.
            module = importlib.import_module(f"models.{model_name}.model")
            _loaded_models[model_name] = module
        except ImportError as e:
            raise ValueError(f"Model '{model_name}' is not available: {e}")
    else:
        module = _loaded_models[model_name]
    # Call the model's predict() function.
    return module.predict(input_data, features)