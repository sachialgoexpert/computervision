from pathlib import Path
import json
import pandas as pd


def ensure_processed_dir_present(raw_path):
    raw_path = Path(raw_path)
    processed_path = raw_path.parent.parent / "processed" / raw_path.name
    processed_path.mkdir(parents=True, exist_ok=True)  # corrected: parents=True, not parent=True
    return processed_path


def save_metadata(metadata, raw_path):
    processed_path = ensure_processed_dir_present(raw_path)
    output_path = processed_path / "metadata.json"

    with open(output_path, "w") as f:
        json.dump(metadata, f, indent=4)
    return output_path


def load_metadata(metadata_path):
    metadata_path = Path(metadata_path)
    if not metadata_path.exists():
        # Try to locate metadata in processed path
        possible_path = metadata_path.parent.parent / "processed" / metadata_path.name / "metadata.json"
        if possible_path.exists():
            metadata_path = possible_path
        else:
            raise FileNotFoundError(f"Metadata not found at {metadata_path}")
    with open(metadata_path, "r") as f:
        return json.load(f)


def get_unique_classes_counts(metadata):
    """
    Expects metadata as a list of dicts, each containing a 'detection' key with a list of detections.
    Example:
        metadata = [
            {'detection': [{'class': 'cat', 'count': 2}, {'class': 'dog', 'count': 1}]},
            {'detection': [{'class': 'cat', 'count': 3}]}
        ]
    """
    unique_classes = set()
    count_options = {}

    for item in metadata:
        for cls in item.get('detection', []):
            class_name = cls['class']
            unique_classes.add(class_name)
            if class_name not in count_options:
                count_options[class_name] = set()
            count_options[class_name].add(cls.get('count', 1))

    # Sort results
    unique_classes = sorted(unique_classes)
    count_options = {cls: sorted(count_options[cls]) for cls in count_options}

    return unique_classes, count_options
