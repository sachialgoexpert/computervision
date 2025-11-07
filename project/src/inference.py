from ultralytics import YOLO
from pathlib import Path
import torch
from PIL import Image
import numpy
from src.config import load_config
from src.utils import save_metadata

class YOLOv11Inference:
    def __init__(self,model_name,device="cuda"):
        self.model=YOLO(model_name)
        self.model.to(device=device)
        self.device=device

        ## Loading config from default.yaml
        config=load_config()
        self.conf_threshold=config["model"]["conf_threshold"]
        self.extensions=config["data"]["image_extension"]
    def process_image(self,image_path):
        results=self.model.predict(
            source=image_path,
            conf=self.conf_threshold,
            device=self.device
        )

        ## Process Results
        detections=[]
        class_counts={}

        for result in result:
            for box in result.boxes:
                cls=result.names[int(box.cls)]
                conf=float(box.conf)
                bbox=box.xyxy[0].tolist()

                detections.append({
                    'class':cls,
                    'confidence':conf,
                    'bbox': bbox,
                    'count': 1
                })
                class_counts[cls]=class_counts.get(cls,0)+1
        for det in detections:
            det['count']=class_counts[det['class']]
        return {
            'image_path': str(image_path),
            'detections': detections,
            'total_objects': len(detections),
            'unique_class': list(class_counts.keys()),
            'class_counts': len(list(class_counts.keys()))
        }


    def process_directory(self,directory_path):
        metadata=[]

        patterns=[f"*{ext}" for ext in self.extensions]
        image_paths=[]
        for pattern in patterns:
            image_paths.extend(Path(directory_path).glob(pattern))
        for image_path in image_paths:
            try:
                metadata.extend(self.process_image(image_path))
            except Exception as e:
                print(f"Error processing {image_path} is str({e})")
                continue
        
