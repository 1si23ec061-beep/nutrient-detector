import streamlit as st
from PIL import Image
import numpy as np
import random

st.set_page_config(page_title="AI Waste Classifier", layout="centered")

# ----------------------------------------
# COLORFUL BACKGROUND + CLEAN UI
# ----------------------------------------
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #ff9a9e, #fad0c4, #a18cd1, #fbc2eb);
    background-size: 500% 500%;
    animation: bgmove 16s ease infinite;
    font-family: 'Segoe UI', sans-serif;
}

@keyframes bgmove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

.popup-box {
    max-width: 700px;
    margin: auto;
    padding: 10px;
    background: transparent !important;
    border: none !important;
}

.heading {
    text-align: center;
    font-size: 36px;
    font-weight: 900;
    background: linear-gradient(90deg, #0066ff, #00e1ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.divider {
    height: 4px;
    width: 120px;
    margin: 10px auto;
    background: #00aaff;
    border-radius: 12px;
    opacity: 0.8;
}

.result-card {
    padding: 20px;
    margin-top: 20px;
    border-radius: 15px;
    background: rgba(255,255,255,0.30);
    backdrop-filter: blur(10px);
    text-align: center;
}

.pred-percent {
    font-size: 50px;
    font-weight: 900;
    color: #003e80;
}

.pred-label {
    font-size: 32px;
    font-weight: 800;
    color: #0055cc;
}

.sec-title {
    font-size: 25px;
    font-weight: 800;
    margin-top: 18px;
    color: #003b70;
}

.info-box {
    background: rgba(255,255,255,0.28);
    padding: 14px;
    border-radius: 12px;
    margin-bottom: 10px;
    border-left: 4px solid #009dff;
}

footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)



# ----------------------------------------
# FINAL HIGH-ACCURACY CLAS
