import os
import shutil
import cv2
import pandas as pd
from ultralytics import YOLO

# Load pre-trained lightweight model
model = YOLO('yolov8n.pt')

RAW_DIR = "data/raw_images"
QUARANTINE_DIR = "data/quarantine"
CROPS_DIR = "data/crops"

def run_triage():
    raw_files = [f for f in os.listdir(RAW_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    total_images = len(raw_files)
    quarantined_count = 0
    space_saved_bytes = 0
    results_data = []

    print(f"Processing {total_images} images...")

    for fname in raw_files:
        fpath = os.path.join(RAW_DIR, fname)
        file_size = os.path.getsize(fpath)
        
        # Run YOLO inference
        results = model(fpath, verbose=False)[0]
        
        # If no objects detected or low confidence, quarantine as blank frame
        if len(results.boxes) == 0:
            quarantined_count += 1
            space_saved_bytes += file_size
            shutil.move(fpath, os.path.join(QUARANTINE_DIR, fname))
            continue

        # Object detected -> process crops
        img = cv2.imread(fpath)
        for i, box in enumerate(results.boxes):
            conf = float(box.conf[0].cpu())
            if conf < 0.30:
                continue
                
            xyxy = box.xyxy[0].cpu().numpy().astype(int)
            crop = img[xyxy[1]:xyxy[3], xyxy[0]:xyxy[2]]
            
            crop_fname = f"crop_{i}_{fname}"
            crop_path = os.path.join(CROPS_DIR, crop_fname)
            cv2.imwrite(crop_path, crop)
            
            results_data.append({
                "original_image": fname,
                "crop_path": crop_path,
                "confidence": round(conf, 2)
            })

    # Metric calculations (Prompt Requirement i)
    space_saved_mb = round(space_saved_bytes / (1024 * 1024), 2)
    # Estimate 30 seconds saved per human review per blank image
    time_saved_mins = round((quarantined_count * 30) / 60, 2)

    print("\n--- TRIAGE COMPLETE ---")
    print(f"Total Frames Processed: {total_images}")
    print(f"Blank Frames Quarantined: {quarantined_count}")
    print(f"Storage Space Saved: {space_saved_mb} MB")
    print(f"Estimated Time Saved: {time_saved_mins} Minutes")

    return pd.DataFrame(results_data)

if __name__ == "__main__":
    df = run_triage()