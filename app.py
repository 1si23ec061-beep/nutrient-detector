import streamlit as st
from PIL import Image
import numpy as np
import random

st.set_page_config(page_title="Waste Classifier", layout="centered")

# ----------------------------------------
# LIGHT BLUE BACKGROUND + CLEAN UI
# ----------------------------------------
st.markdown("""
<style>

body {
    background: #cfe8ff;   /* Light Blue Background */
    font-family: 'Segoe UI', sans-serif;
}

/* Center container */
.popup-box {
    max-width: 720px;
    margin: auto;
    padding: 10px;
    background: transparent !important;
}

/* Title */
.heading {
    text-align: center;
    font-size: 36px;
    font-weight: 900;
    color: #0056b3;   /* Dark Blue for Title */
}

/* Divider */
.divider {
    height: 4px;
    width: 110px;
    margin: 10px auto;
    background: #007bff;
    border-radius: 12px;
}

/* Result Card */
.result-card {
    padding: 20px;
    margin-top: 20px;
    border-radius: 15px;
    background: rgba(255,255,255,0.35);
    backdrop-filter: blur(8px);
    text-align: center;
}

.pred-percent {
    font-size: 50px;
    font-weight: 900;
    color: #003c80;
}

.pred-label {
    font-size: 32px;
    font-weight: 800;
    color: #0055cc;
}

/* Section Title */
.sec-title {
    font-size: 25px;
    font-weight: 800;
    margin-top: 18px;
    color: #003b70;
}

/* Info Box */
.info-box {
    background: rgba(255,255,255,0.40);
    padding: 14px;
    border-radius: 12px;
    border-left: 4px solid #007bff;
}

footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)



# ---------------------------------------------------------
# FINAL ACCURATE CLASSIFICATION LOGIC (ALL 3 CATEGORIES)
# ---------------------------------------------------------
def smart_image_predict(image):

    img = image.resize((64, 64))
    arr = np.array(img)

    r, g, b = np.
