import streamlit as st
from PIL import Image
import numpy as np
import random

st.set_page_config(page_title="Attractive Waste Classifier", layout="centered")

# ===================================
# ADVANCED GLASSMORPHIC POPUP CSS
# ===================================
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #aac7ff, #c8ffd4);
}

/* Pop-up center dashboard */
.popup-box {
    max-width: 720px;
    margin: auto;
    margin-top: 40px;
    padding: 30px;
    border-radius: 22px;
    background: rgba(255,255,255,0.32);
    backdrop-filter: blur(18px);
    border: 1.5px solid rgba(255,255,255,0.45);

    /* Glow effect */
    box-shadow:
        0 0 25px rgba(30,144,255,0.45),
        0 0 40px rgba(30,144,255,0.25);

    animation: popin 0.7s ease-out;
}

@keyframes popin {
    from {opacity: 0; transform: scale(0.92);}
    to {opacity: 1; transform: scale(1);}
}

/* Title */
.heading {
    text-align: center;
    font-size: 36px;
    font-weight: 900;
    background: linear-gradient(90deg, #005bea, #00c6fb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Subheader */
.subtext {
    text-align: center;
    margin-top: -10px;
    margin-bottom: 20px;
    color: #222;
    font-weight: 500;
}

/* Result card */
.result-card {
    margin-top: 20px;
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    background: rgba(255,255,255,0.45);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.5);

    box-shadow:
        0 0 20px rgba(0, 102, 255, 0.25),
        0 0 40px rgba(0, 102, 255, 0.15);
}

.pred-percent {
    font-size: 48px;
    font-weight: 900;
    color: #003c8f;
    text-shadow: 0 0 10px rgba(0, 102, 255, 0.5);
}

.pred-label {
    font-size: 32px;
    font-weight: 800;
    color: #0066cc;
}

/* Section title */
.sec-title {
    font-size: 26px;
    font-weight: 800;
    margin-top: 25px;
    background: linear-gradient(90deg, #004e92, #000428);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Info box */
.box {
    padding: 16px;
    border-radius: 12px;
    background: rgba(255,255,255,0.35);
    border-left: 4px solid #0077ff;
    backdrop-filter: blur(10px);
    margin-bottom: 10px;
}

/* Hide footer */
footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# ===================================
# CLASSIFICATION LOGIC (Smart Dummy)
# ===================================
def classify(img):
    arr = np.array(img.resize((64, 64)))
    r, g, b = np.mean(arr[:,:,0]), np.mean(arr[:,:,1]), np.mean(arr[:,:,2])

    if (r > 150 and g > 150 and b < 120) or (g > 120 and r > 110 and b < 100):
        return "Biodegradable Waste", random.randint(90, 100)

    if b > 150 and g > 150:
        return "Recyclable Waste", random.randint(85, 98)

    if max(r,g,b) > 200 and min(r,g,b) < 80:
        return "Non-Biodegradable Waste", random.randint(88, 100)

    return random.choice(["Biodegradable Waste", "Recyclable Waste", "Non-Biodegradable Waste"]), random.randint(60, 95)

INFO = {
    "Biodegradable Waste": "Naturally decomposes. Best for composting.",
    "Recyclable Waste": "Can be reused through recycling processes.",
    "Non-Biodegradable Waste": "Does not break down. Harmful to environment."
}

DISPOSE = {
    "Biodegradable Waste": "✔ GREEN BIN (Organic Waste)",
    "Recyclable Waste": "✔ BLUE BIN (Dry Recyclables)",
    "Non-Biodegradable Waste": "✔ RED BIN (Dry Waste)",
}

# ===================================
# POP-UP DASHBOARD CONTENT
# ===================================
st.markdown('<div class="popup-box">', unsafe_allow_html=True)

st.markdown('<div class="heading">✨ AI Waste Classification Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Beautiful pop-up interface with smart waste predictions</div>', unsafe_allow_html=True)

uploaded = st.file_uploader("Upload an Image", type=["jpg","jpeg","png"])

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, caption="Uploaded Image", use_container_width=True)

    label, percent = classify(img)

    # Result Card
    st.markdown(f"""
    <div class="result-card">
        <div class="pred-percent">{percent}%</div>
        <div class="pred-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

    # Explanation
    st.markdown('<div class="sec-title">📘 Explanation</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="box">{INFO[label]}</div>', unsafe_allow_html=True)

    # Disposal
    st.markdown('<div class="sec-title">🗑 Recommended Disposal</div>', unsafe_allow_html=True)
    st.success(DISPOSE[label])

else:
    st.info("Upload an image to begin.")

st.markdown('</div>', unsafe_allow_html=True)
