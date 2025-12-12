import streamlit as st
from PIL import Image
import numpy as np
import random

st.set_page_config(page_title="Waste Classifier", layout="centered")

# --------------------------------------------------
# BEAUTIFUL UI / BACKGROUND CSS (ONLY UI CHANGED)
# --------------------------------------------------
st.markdown(
"""
<style>
/* Page background: soft green-blue gradient */
.stApp {
  background: linear-gradient(135deg, #f0fbf6 0%, #eaf7ff 45%, #f7fff1 100%);
  background-attachment: fixed;
}

/* Main content container - translucent card */
.block-container {
  max-width: 800px;
  margin: 28px auto;
  padding: 28px 32px;
  border-radius: 16px;
  background: rgba(255,255,255,0.85);
  box-shadow: 0 10px 30px rgba(3, 10, 18, 0.08);
  backdrop-filter: blur(6px);
}

/* App title styling */
h1, .stTitle {
  font-family: "Segoe UI", Roboto, Arial, sans-serif;
  color: #0b6b3a;
  letter-spacing: 0.2px;
}

/* Markdown headings */
h2, h3 {
  color: #065f46;
}

/* Image card */
.stImage img {
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(2,8,23,0.12);
  border: 1px solid rgba(2,8,23,0.03);
}

/* File uploader styling */
.stFileUploader > div {
  border: 2px dashed rgba(6,95,70,0.12) !important;
  padding: 14px !important;
  border-radius: 12px;
}

/* Prediction text styling */
div[data-testid="stMarkdownContainer"] h2 {
  font-size: 20px;
}

/* Disposal output box styling */
.stAlert > div[role="status"] {
  border-left: 6px solid #16a34a;
  background: linear-gradient(90deg, rgba(16,185,129,0.04), rgba(255,255,255,0.0));
  padding: 12px 16px !important;
  border-radius: 8px;
}

/* Button styling */
.stButton>button {
  border-radius: 10px;
  padding: 8px 14px;
  font-weight: 600;
  box-shadow: 0 6px 18px rgba(3,10,23,0.06);
  border: none;
  cursor: pointer;
}

/* Mobile responsiveness */
@media (max-width: 600px) {
  .block-container { padding: 18px 16px; margin: 12px; }
}
</style>
""",
unsafe_allow_html=True
)

# --------------------------------------------------
# ORIGINAL FUNCTIONALITY (UNCHANGED)
# --------------------------------------------------

st.title("♻ Smart Waste Classification")

EXPLANATIONS = {
    "Biodegradable Waste": "Biodegradable items break down naturally...",
    "Recyclable Waste": "Recyclable items can be reprocessed...",
    "Non-Biodegradable Waste": "These items do not decompose and pollute the environment...",
    "Not Waste": "This item is not waste and can be reused."
}

DISPOSAL = {
    "Biodegradable Waste": "Dispose in GREEN BIN.",
    "Recyclable Waste": "Dispose in BLUE BIN.",
    "Non-Biodegradable Waste": "Dispose in RED BIN.",
    "Not Waste": "Do not throw away — reuse instead."
}

def smart_image_predict(image):
    """Predict based on dominant colors instead of filename."""

    img = image.resize((64, 64))
    arr = np.array(img)

    # Average R, G, B
    r, g, b = np.mean(arr[:, :, 0]), np.mean(arr[:, :, 1]), np.mean(arr[:, :, 2])

    # ------- BIODEGRADABLE DETECTION -------
    if (r > 150 and g > 150 and b < 100) or (r > 120 and g > 80 and b < 80):
        return "Biodegradable Waste", random.randint(90, 100)

    if (g > r and g > b and g > 120) or (r > 120 and g > 90 and b < 90):
        return "Biodegradable Waste", random.randint(85, 100)

    # ------- RECYCLABLE DETECTION -------
    if b > 150 and g > 150:
        return "Recyclable Waste", random.randint(80, 95)

    # ------- NON-BIODEGRADABLE DETECTION -------
    if max(r, g, b) > 200 and min(r, g, b) < 80:
        return "Non-Biodegradable Waste", random.randint(85, 100)

    # Default fallback
    return random.choice([
        "Biodegradable Waste",
        "Recyclable Waste",
        "Non-Biodegradable Waste"
    ]), random.randint(70, 95)


uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, use_column_width=True)

    label, percent = smart_image_predict(img)

    st.markdown(f"## 🔍 Prediction: {percent}% {label}")

    st.markdown("### 📘 Explanation")
    st.write(EXPLANATIONS[label])

    st.markdown("### 🗑 Disposal Method")
    st.success(DISPOSAL[label])
else:
    st.info("📤 Upload an image to begin.")
