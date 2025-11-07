import streamlit as st
import sys
from pathlib import Path
import time
from src.inference import YOLOv11Inference
from src.utils import save_metadata,load_metadata,get_unique_classes_counts

## add project root to the system path

sys.path.append(str(Path(__file__).parent))


def init_session_state():
    session_detaults={
        "metadata":None,
        "unique_classes": [],
        "count_options":{}
    }

    for key,value in session_detaults.items():
        if key not in st.session_state:
            st.session_state[key]=value
        
init_session_state()
st.set_page_config(page_title="YOLOv11 Search Application",layout="wide")
st.title("Computer vision powers Search Application")

### Main options

option=st.radio("Choose an option:",
                ("process new image","load exiting data"),horizontal=True)

if option=="process new image":
    with st.expander("Process new iamges",expanded=True):
        col1, col2=st.columns(2)
        with col1:
            image_directory=st.text_input("Image directory path",placeholder="path/to/images")
        with col2:
            model_path=st.text_input("Model weights path",placeholder="yolo11m.pt")

        if st.button("Start Inference"):
            if image_directory:
                try:
                    with st.spinner("Running object detection"):
                        inferencer=YOLOv11Inference(model_name=model_path)
                        metadata=inferencer.process_directory(image_directory)
                        metadata_path=save_metadata(metadata,image_directory)
                        st.success(f"Processed {len(metadata)} images. Metadata Saved to:")
                        st.code(str(metadata_path))
                        st.session_state.metatdata=metadata
                        st.session_state.unique_classes,st.session_state.count_options=get_unique_classes_counts(metadata=metadata)
                        
                except Exception as e:
                    st.error(f"Error during inference {st.error}")
            else:
                st.warning(f"Please enter image directory path")
else:
    with st.expander("Load Existing metadata",expanded=True):
        metadata_path=st.text_input("Metadata file path",placeholder="path/to/metadata/json")
        if st.button("Load Metadata"):
            if metadata_path:
                try:
                    with st.spinner("Loading metadata... "):
                        metadata=load_metadata(metdata_path=metadata_path)
                        st.session_state.metatdata=metadata
                        st.session_state.unique_classes,st.session_state.count_options=get_unique_classes_counts(metadata=metadata)
                        st.success(f"Successfully loaded metadata for {len(metadata)} images")
                except Exception as e:
                    st.error(f"Error loading metadta {str(e)}")
            else:
                st.warning("Please enter a metadata file path")

