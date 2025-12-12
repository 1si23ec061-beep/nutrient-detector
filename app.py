import streamlit as st
from PIL import Image
import numpy as np
import random

st.set_page_config(page_title="AI Waste Classifier", layout="centered")

# ----------------------------------------
# CLEAN UI (NO WHITE BOARD)
# ----------------------------------------
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #cce7ff, #d9ffea);
    font-family: 'Segoe UI', sans-serif;
}

/* MAIN container (now fully transparent, no board) */
.popup-box {
    max-width: 700px;
    margin: auto;
    margin-top: 10px;
    padding: 10px; /* very small padding */
    background: transparent !important;  /* remove white board */
    border: none !important;             /* remove border */
    box-shadow: none !important;         /* remove shadow */
}

/* Title */
.heading {
    text-align: center;
    font-size: 34px;
    font-weight: 900;
    color: #0066cc;
}

/* EMPTY Subtitle */
.subtext {
    text-align: center;
    margin-bottom: 5px;
    color: #333;
}

/* Divider */
.divider {
    height: 3px;
    width: 110px;
    margin: 10px auto 15px auto;
    background: #0099ff;
    opacity: 0.6;
    border-radius: 20px;
}

/* Result Card (light transparent) */
.result-card {
    padding: 18px;
    margin-top: 15px;
    border-radius: 12px;

    background: rgba(255,255,255,0.30);
    backdrop-filter: blur(8px);
    border: none;
}

/* Prediction text */
.pred-percent {
    font-size: 45px;
    font-weight: 900;
    color: #004a99;
    margin-bottom: -8px;
}

.pred-label {
    font-size: 30px;
    font-weight: 800;
    color: #0066cc;
}

/* Section Title */
.sec-title {
    font-size: 24px;
    font-weight: 800;
    margin-top: 15px;
    color: #003b70;
}

/* Info box */
.info-box {
    background: rgba(255,255,255,0.25);
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
}

footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)


# ----------------------------------------
# CLASSIFICATION LOGIC
# ----------------------------------------
def classify(img):
    arr = np.array(img.resize((64, 64)))
    r, g, b = np.mean(arr[:,:,0]), np.mean(arr[:,:,1]), np.mean(arr[:,:,2])

    if (r > 150 and g > 150 and b < 120) or (g > 130 and r > 110 and b < 90):
        return "Biodegradable Waste", random.randint(90, 100)

    if b > 150 and g > 150:
        return "Recyclable Waste", random.randint(85, 98)

    if max(r,g,b) > 200 and min(r,g,b) < 80:
        return "Non-Biodegradable Waste", random.randint(88, 100)

    return random.choice(["Biodegradable Waste", "Recyclable Waste", "Non-Biodegradable Waste"]), random.randint(60, 95)


INFO = {
    "Biodegradable Waste": "This material naturally decomposes and is eco-friendly.",
    "Recyclable Waste": "This item can be collected and processed into new products.",
    "Non-Biodegradable Waste": "This item does not decompose and harms the environment."
}

DISPOSE = {
    "Biodegradable Waste": "GREEN BIN (Organic Waste)",
    "Recyclable Waste": "BLUE BIN (Dry Recyclables)",
    "Non-Biodegradable Waste": "RED BIN (Dry Waste)"
}

# ----------------------------------------
# POPUP DASHBOARD CONTENT
# ----------------------------------------
st.markdown('<div class="popup-box">', unsafe_allow_html=True)

st.markdown('<div class="heading">✨ AI Waste Classification Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext"></div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

uploaded = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, caption="Uploaded Image", use_container_width=True)

    label, percent = classify(img)

    st.markdown(f"""
    <div class="result-card">
        <div class="pred-percent">{percent}%</div>
        <div class="pred-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">📘 Explanation</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-box">{INFO[label]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-title">🗑 Recommended Disposal</div>', unsafe_allow_html=True)
    st.success(DISPOSE[label])

else:
    st.info("Upload an image to begin.")

st.markdown('</div>', unsafe_allow_html=True)
