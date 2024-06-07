import torch
from PIL import Image
from torchvision.models.detection import fasterrcnn_resnet50_fpn, FasterRCNN_ResNet50_FPN_Weights
import torchvision.transforms as T

weights = FasterRCNN_ResNet50_FPN_Weights.DEFAULT

# Initialize Faster R-CNN
model = fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()


# Function to detect objects using Faster R-CNN
def detect_objects(image_pil):
    image = image_pil.convert("RGB")
    transform = T.Compose([T.ToTensor()])
    image_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        predictions = model(image_tensor)

    return image, predictions[0]