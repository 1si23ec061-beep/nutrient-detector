import streamlit as st
from PIL import Image
import random

st.set_page_config(page_title="Waste Classification Demo", layout="centered")

st.title("♻ Waste Classification Dashboard (Demo)")
st.write("Upload an image — the system will SIMULATE classification using random output.")

# Load the “trained” model file (simulated)
try:
    with open("trained_model.txt", "r") as f:
        model_info = f.read().strip()
except:
    model_info = "No trained model file found. Running in demo mode."

st.subheader("Loaded Model Info:")
st.code(model_info)

# Possible labels
labels = [
    "Biodegradable Waste",
    "Non-Biodegradable Waste",
    "Recyclable Waste",
    "Not Waste"
]

# Upload image
uploaded = st.file_uploader("Upload an image", type=["jpg","jpeg","png"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, use_column_width=True)

    # Simulated prediction
    result = random.choice(labels)

    st.subheader("Prediction:")
    st.success(result)

    st.subheader("Suggested Action:")
    if result == "Biodegradable Waste":
        st.info("Put in GREEN BIN — compostable.")
    elif result == "Non-Biodegradable Waste":
        st.warning("Put in RED BIN — harmful.")
    elif result == "Recyclable Waste":
        st.success("Put in BLUE BIN — recyclable.")
    else:
        st.write("This is not waste — reuse if possible.")
