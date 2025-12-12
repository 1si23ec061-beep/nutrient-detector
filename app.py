import streamlit as st
from PIL import Image
import numpy as np

st.set_page_config(page_title="Waste Classifier", layout="centered")

# -------------------------------------------------------------
# BLUE BACKGROUND + CLEAN UI
# -------------------------------------------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #4da6ff; }
[data-testid="stHeader"] { background: rgba(0,0,0,0); }
[data-testid="stToolbar"] { display: none; }

.heading {
    text-align: center;
    font-size: 36px;
    font-weight: 900;
    color: white;
}
.divider {
    height: 4px;
    width: 110px;
    margin: 10px auto;
    background: white;
    border-radius: 12px;
}
.result-card {
    padding: 20px;
    margin-top: 20px;
    border-radius: 15px;
    background: rgba(255,255,255,0.35);
    text-align: center;
    backdrop-filter: blur(8px);
}
.pred-percent {
    font-size: 50px;
    font-weight: 900;
    color: #00264d;
}
.pred-label {
    font-size: 32px;
    font-weight: 800;
    color: #003d99;
}
.sec-title {
    font-size: 25px;
    font-weight: 800;
    margin-top: 20px;
    color: white;
}
.info-box {
    background: rgba(255,255,255,0.40);
    padding: 14px;
    border-radius: 12px;
    border-left: 4px solid white;
    color: black;
}
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------------------
# IMPROVED IMAGE CLASSIFIER
# -------------------------------------------------------------
def classify_image(img):
    img = img.resize((160, 160))
    arr = np.array(img).astype(np.float32)

    # Extract channels
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    r_mean, g_mean, b_mean = r.mean(), g.mean(), b.mean()

    hsv = np.array(img.convert("HSV")).astype(np.float32)
    h, s, v = hsv[:,:,0], hsv[:,:,1], hsv[:,:,2]

    total = arr.shape[0] * arr.shape[1]

    # Masks (fractions)
    yellow = (r > 150) & (g > 130) & (b < 110)
    green = (g > r) & (g > b) & (g > 120)
    blue = (b > 150) & (b > r + 15)
    gray = (np.abs(r-g)<15) & (np.abs(g-b)<15) & ((r+g+b)/3 > 110)

    yellow_frac = yellow.sum() / total
    green_frac = green.sum() / total
    blue_frac = blue.sum() / total
    gray_frac = gray.sum() / total

    variation = arr.std()
    bright_frac = (v > 230).sum() / total
    sat_frac = (s > 180).sum() / total

    # ---------------------------------------------------------
    # CLASSIFICATION RULES
    # ---------------------------------------------------------

    # 1) NON-BIO (shiny wrappers, high variation, glossy)
    if (variation > 60) or (bright_frac > 0.12 and sat_frac > 0.12):
        confidence = min(100, int(85 + variation / 3))
        return "Non-Biodegradable Waste", confidence

    # 2) RECYCLABLE (blue plastics, metals, glass)
    if blue_frac > 0.06 or gray_frac > 0.05:
        confidence = min(100, int(75 + (blue_frac + gray_frac) * 180))
        return "Recyclable Waste", confidence

    # 3) BIODEGRADABLE (fruits, vegetables, organic tones)
    if yellow_frac > 0.03 or green_frac > 0.04:
        confidence = min(100, int(80 + (yellow_frac + green_frac) * 150))
        return "Biodegradable Waste", confidence

    # Brownish organic tones
    if r_mean > 120 and g_mean > 90 and b_mean < 100:
        return "Biodegradable Waste", 85

    # Default fallback
    return "Biodegradable Waste", 75


# -------------------------------------------------------------
# DISPLAY INFORMATION
# -------------------------------------------------------------
INFO = {
    "Biodegradable Waste": "Biodegradable items break down naturally (food waste, leaves, paper).",
    "Recyclable Waste": "Recyclable items can be processed and reused (bottles, cans, glass).",
    "Non-Biodegradable Waste": "Non-biodegradable items do not decompose (wrappers, packets)."
}

DISPOSE = {
    "Biodegradable Waste": "Use the GREEN BIN.",
    "Recyclable Waste": "Use the BLUE BIN.",
    "Non-Biodegradable Waste": "Use the RED BIN."
}


# -------------------------------------------------------------
# MAIN UI
# -------------------------------------------------------------
st.markdown('<div class="heading">♻ Smart Waste Classification</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, use_column_width=True)

    label, confidence = classify_image(img)

    st.markdown(f"""
    <div class="result-card">
        <div class="pred-percent">{confidence}%</div>
        <div class="pred-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">📘 Explanation</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-box">{INFO[label]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-title">🗑 Disposal Method</div>', unsafe_allow_html=True)
    st.success(DISPOSE[label])

else:
    st.info("📤 Upload an image to begin.")
