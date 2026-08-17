import os
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np

# Load pre-trained ResNet for feature extraction
resnet = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
resnet = torch.nn.Sequential(*list(resnet.children())[:-1]).eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Simulated local database of existing known tiger feature vectors
known_tigers_db = {}
tiger_counter = 1

def extract_features(img_path):
    img = Image.open(img_path).convert('RGB')
    tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        vec = resnet(tensor).flatten().numpy()
    return vec / np.linalg.norm(vec) # Normalize vector

def match_tiger(crop_path):
    global tiger_counter
    candidate_vec = extract_features(crop_path)
    
    # If database is empty, register first tiger
    if not known_tigers_db:
        tiger_id = f"TIGER_PENCH_00{tiger_counter}"
        known_tigers_db[tiger_id] = candidate_vec
        tiger_counter += 1
        return tiger_id, 1.0, False # ID, Match Score, Needs Review Flag

    best_match_id = None
    best_score = -1.0

    # Cosine Similarity Matching
    for tiger_id, db_vec in known_tigers_db.items():
        score = np.dot(candidate_vec, db_vec)
        if score > best_score:
            best_score = score
            best_match_id = tiger_id

    # Requirement ii Matching Threshold Rules
    if best_score >= 0.82:
        # High confidence match
        return best_match_id, round(float(best_score), 2), False
    elif 0.60 <= best_score < 0.82:
        # Ambiguous match -> surfaces to human reviewer
        return best_match_id, round(float(best_score), 2), True
    else:
        # New individual auto-enrollment
        new_id = f"TIGER_PENCH_00{tiger_counter}"
        known_tigers_db[new_id] = candidate_vec
        tiger_counter += 1
        return new_id, 1.0, False

def run_identification():
    CROPS_DIR = "data/crops"
    crop_files = [f for f in os.listdir(CROPS_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    print(f"\nProcessing {len(crop_files)} tiger crops for identification...")
    
    for fname in crop_files:
        path = os.path.join(CROPS_DIR, fname)
        tiger_id, score, review_flag = match_tiger(path)
        
        status = "NEEDS HUMAN REVIEW" if review_flag else "AUTO MATCHED"
        print(f"Crop: {fname} | Assigned: {tiger_id} | Score: {score} | Status: {status}")

if __name__ == "__main__":
    run_identification()