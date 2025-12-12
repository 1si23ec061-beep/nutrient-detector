import streamlit as st
from PIL import Image
import numpy as np
import random

st.set_page_config(page_title="Waste Classifier", layout="centered")

# -------------------------------------------------------------
# WORKING BLUE BACKGROUND + CLEAN UI
# -------------------------------------------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #4da6ff;   /* Solid Blue Background */
}
[data-testid="stHeader"] { background: rgba(0,0,0,0); }
[data-testid="stToolbar"] { display: none; }

.heading { text-align: center; font-size: 36px; font-weight: 900; color: white; }
.divider { height: 4px; width: 110px; margin: 10px auto; background: white; border-radius: 12px; }

.result-card {
    padding: 20px; margin-top: 20px; border-radius: 15px;
    background: rgba(255,255,255,0.35); text-align: center; backdrop-filter: blur(8px);
}
.pred-percent { font-size: 50px; font-weight: 900; color: #00264d; }
.pred-label { font-size: 32px; font-weight: 800; color: #003d99; }

.sec-title { font-size: 25px; font-weight: 800; margin-top: 20px; color: white; }
.info-box {
    background: rgba(255,255,255,0.40); padding: 14px; border-radius: 12px; border-left: 4px solid white; color: black;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# IMPROVED CLASSIFIER - combining color, saturation, variation
# ---------------------------------------------------------
def classify_image_better(pil_img):
    """
    Return (label, confidence_percent)
    Uses combined heuristics:
      - color masks for yellow/green/blue/gray
      - HSV saturation and value metrics
      - overall color variation (std)
      - priority rules: wrapper/high-sat -> Non-bio, blue/gray -> Recyclable, yellow/green/brown -> Biodegradable
    """
    img = pil_img.resize((160, 160))  # larger than 64 to improve stats
    arr = np.array(img).astype(np.float32)

    # RGB channels mean
    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]

    r_mean = float(r.mean())
    g_mean = float(g.mean())
    b_mean = float(b.mean())

    # color variation (texture / multi-color packaging)
    variation = float(arr.std())

    # Convert to HSV (PIL's .convert) for saturation/value stats
    hsv = np.array(img.convert("HSV")).astype(np.float32)
    h = hsv[:, :, 0]    # 0-255
    s = hsv[:, :, 1]    # 0-255 saturation
    v = hsv[:, :, 2]    # 0-255 value (brightness)

    s_mean = float(s.mean())
    v_mean = float(v.mean())

    # Pixel-wise masks (fractions)
    total_pixels = arr.shape[0] * arr.shape[1]

    # Yellow mask (banana peel / organic yellow): R high, G high, B low, and R~G
    yellow_mask = (r > 150) & (g > 120) & (b < 110) & (np.abs(r - g) < 70)
    yellow_frac = float(yellow_mask.sum() / total_pixels)

    # Green mask (leaves/veg): G dominant and reasonably bright
    green_mask = (g > r) & (g > b) & (g > 110)
    green_frac = float(green_mask.sum() / total_pixels)

    # Blue mask (bottles, plastic): B dominant and greater than R by margin
    blue_mask = (b > 140) & (b > r + 20)
    blue_frac = float(blue_mask.sum() / total_pixels)

    # Gray/metal mask (recyclable cans/glass): low chroma (R≈G≈B) and moderate brightness
    gray_mask = (np.abs(r - g) < 18) & (np.abs(g - b) < 18) & ( (r+g+b)/3.0 > 110 )
    gray_frac = float(gray_mask.sum() / total_pixels)

    # High saturation / bright pixels (often wrappers, shiny packaging)
    high_sat_mask = s > 150
    high_sat_frac = float(high_sat_mask.sum() / total_pixels)

    very_bright_mask = v > 220
    very_bright_frac = float(very_bright_mask.sum() / total_pixels)

    # overall colorfulness metric
    colorfulness = float(np.mean(np.abs(arr - np.mean(arr, axis=(0,1)))))  # avg distance per channel

    # Confidence scoring helpers (clipped)
    def clip01(x): return min(max(x, 0.0), 1.0)

    # Heuristic priority:
    # 1) High variation or high saturation + bright pixels -> Non-Biodegradable (wrappers)
    if (variation > 45 and high_sat_frac > 0.10) or (colorfulness > 40 and high_sat_frac > 0.08) or very_bright_frac > 0.02:
        # Confidence increases with variation and high_sat_frac
        score = 0.6 * clip01((variation - 30) / 60.0) + 0.4 * clip01(high_sat_frac * 3.0)
        conf = int(90 + round(10 * clip01(score)))
        return "Non-Biodegradable Waste", conf

    # 2) Recyclable: blue_frac or gray_frac significant
    if blue_frac > 0.06 or gray_frac > 0.06 or (b_mean > 140 and v_mean > 110):
        # Confidence based on blue_frac and gray_frac and v_mean
        score = max(clip01(blue_frac * 8.0), clip01(gray_frac * 8.0), clip01((b_mean - 120) / 120.0))
        conf = int(75 + round(23 * score))
        return "Recyclable Waste", conf

    # 3) Biodegradable: yellow_frac or green_frac or brownish mean
    if yellow_frac > 0.03 or green_frac > 0.05 or (r_mean > 115 and g_mean > 95 and b_mean < 110):
        score = max(clip01(yellow_frac * 25.0), clip01(green_frac * 10.0), clip01((r_mean - 120) / 80.0))
        conf = int(78 + round(20 * score))
        return "Biodegradable Waste", conf

    # 4) Fallback: use balanced probabilities based on signals
    # compute soft scores for each class
    nonbio_score = 0.5 * clip01((variation - 20) / 60.0) + 0.5 * clip01(high_sat_frac * 2.5)
    rec_score = max(clip01(blue_frac * 8.0), clip01(gray_frac * 8.0))
    bio_score = max(clip01(yellow_frac * 25.0), clip01(green_frac * 10.0), clip01(((r_mean+g_mean)/2 - b_mean) / 80.0))

    scores = np.array([bio_score, rec_score, nonbio_score])
    idx = int(scores.argmax())
    label_map = ["Biodegradable Waste", "Recyclable Waste", "Non-Biodegradable Waste"]
    base_conf = int(70 + round(25 * scores[idx]))
    # ensure minimum confidence
    conf = min(98, max(base_conf, 70))
    return label_map[idx], conf


# ---------------------------------------------------------
# INFORMATION DISPLAY
# ---------------------------------------------------------
EXPLANATIONS = {
    "Biodegradable Waste": "Biodegradable items break down naturally and can be composted (food scraps, leaves, paper).",
    "Recyclable Waste": "Recyclable items can be processed and reused (plastic bottles, metal cans, glass).",
    "Non-Biodegradable Waste": "Non-biodegradable items do not decompose and harm the environment (wrappers, multilayer packets).",
}

DISPOSE = {
    "Biodegradable Waste": "Dispose in GREEN BIN (organic).",
    "Recyclable Waste": "Dispose in BLUE BIN (recyclables).",
    "Non-Biodegradable Waste": "Dispose in RED BIN (non-recyclable).",
}


# ---------------------------------------------------------
# UI LAYOUT
# ---------------------------------------------------------
st.markdown('<div class="heading">♻ Smart Waste Classification</div>', unsafe_allow_html=True)
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

uploaded = st.file_uploader("Upload an image (jpg / png)", type=["jpg", "jpeg", "png"])

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, use_column_width=True)

    label, percent = classify_image_better(img)

    st.markdown(f"""
    <div class="result-card">
        <div class="pred-percent">{percent}%</div>
        <div class="pred-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">📘 Explanation</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-box">{EXPLANATIONS[label]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-title">🗑 Disposal</div>', unsafe_allow_html=True)
    st.success(DISPOSE[label])

    # show debug stats (hidden by default) - helpful if you want to tune later
    with st.expander("Show classifier debug info (for tuning)"):
        arr = np.array(img.resize((160,160))).astype(np.float32)
        r_m, g_m, b_m = float(arr[:,:,0].mean()), float(arr[:,:,1].mean()), float(arr[:,:,2].mean())
        variation = float(arr.std())
        hsv = np.array(img.resize((160,160)).convert("HSV")).astype(np.float32)
        s_mean = float(hsv[:,:,1].mean()); v_mean = float(hsv[:,:,2].mean())
        st.write({
            "r_mean": round(r_m,1), "g_mean": round(g_m,1), "b_mean": round(b_m,1),
            "variation": round(variation,2), "s_mean": round(s_mean,1), "v_mean": round(v_mean,1)
        })

else:
    st.info("📤 Upload an image to begin.")
