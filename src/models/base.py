"""
base.py

Defines an abstract BaseModel class that all models should implement.
This standardizes the interface for training, prediction, saving, and loading.
"""

from abc import ABC, abstractmethod

class BaseModel(ABC):
    @abstractmethod
    def train(self, X, y):
        """Train the model on features X and labels y."""
        pass

    @abstractmethod
    def predict(self, X):
        """Predict output for given features X."""
        pass

    @abstractmethod
    def save(self, path: str):
        """Save the model to the specified path."""
        pass

    @abstractmethod
    def load(self, path: str):
        """Load the model from the specified path."""
        pass