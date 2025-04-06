import importlib

_loaded_models = {}

def predict(model_name: str, input_data, features: dict = None):
    if model_name not in _loaded_models:
        try:
            module = importlib.import_module(f"models.{model_name}.model")
            _loaded_models[model_name] = module
        except ImportError as e:
            raise ValueError(f"Model '{model_name}' is not available: {e}")
    else:
        module = _loaded_models[model_name]
    if features:
        return module.predict(input_data, features)
    else:
        return module.predict(input_data)