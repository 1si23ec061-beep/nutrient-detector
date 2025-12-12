import streamlit as st
from PIL import Image
import numpy as np
import random

st.set_page_config(page_title="Pop-Up Waste Classifier", layout="centered")

# ============================
# POP-UP DASHBOARD CSS
# ============================
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #dbeafe, #e8f5e9);
}

/* Center popup container */
.popup-dashboard {
    max-width: 650px;
    margin: auto;
    margin-top: 40px;
    padding: 25px;
    border-radius: 20px;
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(15px);
    box-shadow: 0 12px 28px rgba(0,0,0,0.25);
    animation: fadeIn 0.6s ease;
}

/* Smooth fade-in animation */
@keyframes fadeIn {
    from {opacity:0; transform: scale(0.94);}
    to {opacity:1; transform: scale(1);}
}

.header {
    text-align: center;
    font-size: 32px;
    font-weight: 900;
    color: #004c99;
    margin-bottom: 12px;
}

.subtext {
    text-align: center;
    font-size: 16px;
    color: #333;
    margin-bottom: 25px;
}

.prediction-box {
    background: rgba(255,255,255,0.55);
    padding: 18px;
    border-radius: 16px;
    text-align: center;
    margin-top: 20px;
    border: 1px solid #cccccc;
}

.pred-label {
    font-size: 34px;
    font-weight: 900;
    color: #0055aa;
}

.pred-percent {
    font-size: 46px;
    font-weight: 900;
    margin-top: -10px;
    color: #003366;
}

.section-title {
    margin-top: 25px;
    font-size: 22px;
    font-weight: 700;
    color: #003366;
}

footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# ============================
# CLASSIFICATION LOGIC
# ============================
def classify(img):
    """Smart color-based dummy classifier"""
    arr = np.array(img.resize((64, 64)))
    r, g, b = np.mean(arr[:,:,0]), np.mean(arr[:,:,1]), np.mean(arr[:,:,2])

    if (r > 150 and g > 150 and b < 120) or (g > 120 and r > 100 and b < 100):
        return "Biodegradable Waste", random.randint(90, 100)
    if b > 150 and g > 150:
        return "Recyclable Waste", random.randint(85, 98)
    if max(r,g,b) > 200 and min(r,g,b) < 80:
        return "Non-Biodegradable Waste", random.randint(88, 100)

    return random.choice([
        "Biodegradable Waste",
        "Recyclable Waste",
        "Non-Biodegradable Waste"
    ]), random.randint(60, 95)


INFO = {
    "Biodegradable Waste": "Breaks down naturally and is compost-friendly.",
    "Recyclable Waste": "Can be processed again and reused.",
    "Non-Biodegradable Waste": "Does not decompose and harms the environment."
}

DISPOSE = {
    "Biodegradable Waste": "Use **GREEN BIN** — Best for composting.",
    "Recyclable Waste": "Use **BLUE BIN** — Clean before disposal.",
    "Non-Biodegradable Waste": "Use **RED BIN** — Avoid burning."
}

# ============================
# POP-UP DASHBOARD UI
# ============================

st.markdown('<div class="popup-dashboard">', unsafe_allow_html=True)

st.markdown('<div class="header">✨ AI Waste Classifier</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Smart classification inside a beautiful pop-up dashboard</div>', unsafe_allow_html=True)

uploaded = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, caption="Uploaded Image", use_container_width=True)

    label, percent = classify(img)

    st.markdown('<div class="prediction-box">', unsafe_allow_html=True)
    st.markdown(f'<div class="pred-percent">{percent}%</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="pred-label">{label}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">📘 Explanation</div>', unsafe_allow_html=True)
    st.write(INFO[label])

    st.markdown('<div class="section-title">🗑 Disposal</div>', unsafe_allow_html=True)
    st.success(DISPOSE[label])

else:
    st.info("Upload an image to begin.")

st.markdown('</div>', unsafe_allow_html=True)  # close popup dashboard
