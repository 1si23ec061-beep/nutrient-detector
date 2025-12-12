import streamlit as st
from PIL import Image
import random

st.set_page_config(page_title="Waste Classifier", layout="centered")

st.title("♻ Waste Classification — Smart Educational Demo")

# Keyword maps
BIO = ["banana", "peel", "apple", "fruit", "vegetable", "veg", "leaf", "leaves", "food", "compost", "paper"]
REC = ["bottle", "plastic", "can", "glass", "jar", "metal", "cardboard", "carton", "paperbox"]
NONBIO = ["chip", "chips", "wrapper", "packet", "styrofoam", "polythene", "plasticbag"]
NOTW = ["phone", "laptop", "toy", "book", "cloth", "tool"]

# Educational explanations
EXPLANATIONS = {
    "Biodegradable Waste": "Biodegradable materials break down naturally into the environment...",
    "Recyclable Waste": "Recyclable materials can be processed and reused...",
    "Non-Biodegradable Waste": "These items do not decompose and can harm the environment...",
    "Not Waste": "This item is not waste and can be reused or repurposed."
}

DISPOSAL = {
    "Biodegradable Waste": "Dispose in **GREEN BIN** (Organic Waste)",
    "Recyclable Waste": "Dispose in **BLUE BIN** (Recyclables)",
    "Non-Biodegradable Waste": "Dispose in **RED BIN** (Dry Waste)",
    "Not Waste": "Do not throw away — try to reuse!"
}

def smart_predict(name):
    """Predict label based on filename keywords."""
    name = name.lower() if name else ""

    # Check keywords
    if any(k in name for k in BIO):
        return "Biodegradable Waste", random.randint(90, 100)
    elif any(k in name for k in REC):
        return "Recyclable Waste", random.randint(85, 100)
    elif any(k in name for k in NONBIO):
        return "Non-Biodegradable Waste", random.randint(80, 100)
    elif any(k in name for k in NOTW):
        return "Not Waste", random.randint(10, 40)
    else:
        # fallback (unknown item)
        label = random.choice(["Biodegradable Waste", "Recyclable Waste", "Non-Biodegradable Waste"])
        return label, random.randint(60, 95)


uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, use_column_width=True)

    filename = uploaded.name
    label, percent = smart_predict(filename)

    st.markdown(f"## 🔍 Prediction: {percent}% {label}")

    st.markdown("### 📘 What This Means")
    st.write(EXPLANATIONS[label])

    st.markdown("### 🗑 Proper Disposal")
    st.success(DISPOSAL[label])

    st.info("This is a smart simulated model. No real AI is used.")
else:
    st.info("📤 Upload an image to begin.")
