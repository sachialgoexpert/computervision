from pathlib import Path
import json
import pandas as pd

def ensure_processed_dir_present(raw_path):
    raw_path=Path(raw_path)
    processed_path=raw_path.parent.parent / "processed" / raw_path.name
    processed_path.mkdir(parent=True,exists_ok=True)
    return processed_path

def save_metadata(metadata,raw_path):
    processed_path=ensure_processed_dir_present(raw_path=raw_path)
    output_path=processed_path / "metadata.json"

    with open(output_path, "w") as f:
        json.dump(metadata,f)
    return output_path

def load_metadata(metdata_path):
    metadata_path=Path(metdata_path)
    if not metdata_path.exists():
        processed_path=metdata_path.parent.parent / "processed" /metdata_path.name / "metadata.json"
        if processed_path.exists():
            processed_path=metadata_path
        else:
            raise FileNotFoundError(f"Metadata is not found at location {metadata_path}.")
    with open(metadata_path, 'r') as f:
        return json.load(f)

        
def get_unique_classes_Counts(metadata):

    unique_classes=set()
    count_options=set()
    for item in metadata:
        for cls in item['detection']:
            unique_classes.add(cls)
            if cls['class'] not in count_options:
                count_options(cls['class'])=set()
            count_options[cls['class']].add(cls['count'])
    for cls in count_options:
        count_options=sorted(count_options[cls])
    unique_classes=sorted(unique_classes)
    return unique_classes,count_options
