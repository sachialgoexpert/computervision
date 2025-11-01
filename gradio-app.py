import gradio as gr

def predict (class_idx):
    if class_idx=="0":
        return "CAT"
    elif class_idx=="1":
        return "DOG"
    elif class_idx=="2":
        return "PERSON"
    else:
        return "No class labels found"

demo=gr.Interface(
    fn=predict,
    inputs="text",
    outputs="text"
)

if __name__=="__main__":
    demo.launch()