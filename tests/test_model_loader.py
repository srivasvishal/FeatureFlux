import unittest
from models import model_loader

class TestModelLoader(unittest.TestCase):
    def test_sentiment_model(self):
        input_data = {"text": "I love this product!"}
        result = model_loader.predict("sentiment_model", input_data)
        self.assertIn("label", result)
        self.assertIn("score", result)

    def test_invalid_model(self):
        with self.assertRaises(ValueError):
            model_loader.predict("non_existent_model", {"text": "Test"})

if __name__ == "__main__":
    unittest.main()