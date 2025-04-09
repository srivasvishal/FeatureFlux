"""
test_model_loader.py

Unit tests for the model loader functionality.
"""

import unittest
from src.models import model_loader

class TestModelLoader(unittest.TestCase):
    def test_invalid_model(self):
        with self.assertRaises(ValueError):
            model_loader.predict("non_existent_model", {"dummy": 1})

    def test_tabular_model_prediction(self):
        # For testing, we assume that an initial training file exists.
        # Provide a dummy input with features matching the expected schema.
        input_data = {"feature1": 10, "feature2": 20}
        # This should trigger training if model not available.
        result = model_loader.predict("tabular_model", input_data)
        # Check that result is a dict and contains a predicted_class key.
        self.assertIn("predicted_class", result)

if __name__ == "__main__":
    unittest.main()