"""
model.py for image_model

A simple image classification model using a pre-trained ResNet50 from PyTorch.
It demonstrates inference using the PyTorch framework.
"""

import torch
import torchvision.transforms as transforms
from PIL import Image

# Load pre-trained ResNet50 model.
# Note: Using torch.hub to load a model that supports MPS on Apple Silicon.
model = torch.hub.load('pytorch/vision:v0.15.2', 'resnet50', pretrained=True)
model.eval()  # Set model to evaluation mode.

# Define image transformation pipeline.
transform_pipeline = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],  # Standard ImageNet means.
                         std=[0.229, 0.224, 0.225])
])

def predict(input_data: dict, features: dict = None):
    """
    Performs image classification.
    Expects input_data to have a key 'image_path' that points to an image file.
    """
    image_path = input_data.get("image_path", "")
    if not image_path:
        return {"error": "No image path provided"}
    
    # Open the image file.
    try:
        image = Image.open(image_path).convert("RGB")
    except Exception as e:
        return {"error": f"Could not open image: {e}"}
    
    # Apply transformations.
    img_tensor = transform_pipeline(image).unsqueeze(0)  # Add batch dimension.
    
    # Optionally, move tensor to MPS (for Apple Silicon) if available.
    device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu")
    img_tensor = img_tensor.to(device)
    model.to(device)
    
    # Inference.
    with torch.no_grad():
        output = model(img_tensor)
    # Apply softmax to get probabilities.
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    predicted_class = int(torch.argmax(probabilities))
    
    return {"predicted_class": predicted_class, "confidence": float(probabilities[predicted_class])}