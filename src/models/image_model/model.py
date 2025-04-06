from torchvision import models, transforms
from PIL import Image
import torch

# Pre-trained ResNet50
model = models.resnet50(pretrained=True)
model.eval()

# Preprocessing pipeline
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def predict_image(img_path):
    img = Image.open(img_path)
    input_tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        outputs = model(input_tensor)
    _, predicted = outputs.max(1)
    return predicted.item()

if __name__ == "__main__":
    print(predict_image('sample_input.jpg'))