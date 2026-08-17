import os
import shutil
import cv2
import torch
import numpy as np
import pandas as pd
from PIL import Image
from ultralytics import YOLO
import torchvision.models as models
import torchvision.transforms as transforms

# Initialize Models
yolo = YOLO('yolov8n.pt')
resnet = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
resnet = torch.nn.Sequential(*list(resnet.children())[:-1]).eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

known_db = {}
tiger_counter = 1

def extract_features(crop_img):
    img = Image.fromarray(cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB))
    tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        vec = resnet(tensor).flatten().numpy()
    return vec / np.linalg.norm(vec)

def process_batch(raw_dir="data/raw_images", quarantine_dir="data/quarantine"):
    global tiger_counter
    raw_files = [f for f in os.listdir(raw_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    results_list = []
    quarantined_count = 0
    space_saved_bytes = 0

    # Mock station coordinates in Pench Tiger Reserve for GIS integration
    stations = [
        {"station_id": "STN_CORE_01", "lat": 21.6521, "lon": 79.3102, "zone": "Core"},
        {"station_id": "STN_CORE_02", "lat": 21.6610, "lon": 79.3215, "zone": "Core"},
        {"station_id": "STN_BUF_01",  "lat": 21.6905, "lon": 79.3550, "zone": "Buffer"},
    ]

    for idx, fname in enumerate(raw_files):
        fpath = os.path.join(raw_dir, fname)
        file_size = os.path.getsize(fpath)
        
        # 1. Blank Image Triage
        yolo_res = yolo(fpath, verbose=False)[0]
        if len(yolo_res.boxes) == 0:
            quarantined_count += 1
            space_saved_bytes += file_size
            shutil.move(fpath, os.path.join(quarantine_dir, fname))
            continue

        # 2. Tiger Detection & Feature Matching
        img = cv2.imread(fpath)
        stn = stations[idx % len(stations)] # Assign station mock data
        
        for box in yolo_res.boxes:
            if float(box.conf[0]) < 0.30: continue
            xyxy = box.xyxy[0].cpu().numpy().astype(int)
            crop = img[xyxy[1]:xyxy[3], xyxy[0]:xyxy[2]]
            
            vec = extract_features(crop)
            
            # Match Logic
            best_id, best_score = None, -1.0
            for t_id, db_vec in known_db.items():
                score = np.dot(vec, db_vec)
                if score > best_score:
                    best_score, best_id = score, t_id

            if best_score >= 0.82:
                assigned_id, review = best_id, False
            elif 0.60 <= best_score < 0.82:
                assigned_id, review = best_id, True
            else:
                assigned_id = f"TIGER_PENCH_00{tiger_counter}"
                known_db[assigned_id] = vec
                tiger_counter += 1
                review = False

            results_list.append({
                "image_name": fname,
                "tiger_id": assigned_id,
                "confidence": round(float(best_score if best_score > 0 else 1.0), 2),
                "needs_human_review": review,
                "station_id": stn["station_id"],
                "latitude": stn["lat"],
                "longitude": stn["lon"],
                "zone_type": stn["zone"],
                "timestamp": "2026-08-17 14:30:00"
            })

    metrics = {
        "total_processed": len(raw_files),
        "quarantined_blanks": quarantined_count,
        "space_saved_mb": round(space_saved_bytes / (1024 * 1024), 2),
        "time_saved_mins": round((quarantined_count * 30) / 60, 2)
    }

    return pd.DataFrame(results_list), metrics

if __name__ == "__main__":
    df, metrics = process_batch()
    print("--- METRICS ---", metrics)
    print("--- DETECTION RESULTS ---")
    print(df)