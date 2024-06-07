import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import requests
from io import BytesIO

# Load CLIP model and processor
model_name = "openai/clip-vit-base-patch32"
clip_model = CLIPModel.from_pretrained(model_name)
clip_processor = CLIPProcessor.from_pretrained(model_name)

# Function to get image embeddings using CLIP
def get_image_embedding(image):
    inputs = clip_processor(images=image, return_tensors="pt")
    with torch.no_grad():
        embeddings = clip_model.get_image_features(**inputs)
    return embeddings

# Function to get similarity between two image embeddings
def calculate_similarity(embedding1, embedding2):
    # Normalize the embeddings
    embedding1 = embedding1 / embedding1.norm(p=2, dim=-1, keepdim=True)
    embedding2 = embedding2 / embedding2.norm(p=2, dim=-1, keepdim=True)
    # Cosine similarity
    similarity = torch.matmul(embedding1, embedding2.T).item()
    return similarity

# Function to verify the best match using CLIP
def verify_image_similarity(cropped_image, search_results):
    cropped_embedding = get_image_embedding(cropped_image)
    best_match = None
    highest_similarity = 0

    for result in search_results:
        try:
            response = requests.get(result)
            if response.status_code == 200:
                search_image = Image.open(BytesIO(response.content)).convert("RGB")
                search_embedding = get_image_embedding(search_image)
                similarity = calculate_similarity(cropped_embedding, search_embedding)
                if similarity > highest_similarity:
                    highest_similarity = similarity
                    best_match = result
        except:
            continue

    return best_match