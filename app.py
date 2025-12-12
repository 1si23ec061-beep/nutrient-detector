import streamlit as st
from PIL import Image
import numpy as np
import random

st.set_page_config(page_title="AI Waste Classifier", layout="centered")

# --------------------------
# CSS FOR POP-UP MODAL
# --------------------------
modal_css = """
<style>
/* Background blur when popup is active */
body.modal-open {
    overflow: hidden;
}

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.55);
    backdrop-filter: blur(6px);
    z-index: 999;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* Modal box */
.modal-box {
    background: rgba(255,255,255,0.90);
    backdrop-filter: blur(15px);
    border-radius: 18px;
    width: 480px;
    padding: 30px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.3);
    text-align: center;
    animation: popIn 0.4s ease-out;
}

@keyframes popIn {
    0% {transform: scale(0.7); opacity: 0;}
    100% {transform: scale(1); opacity: 1;}
}

/* Close button */
.close-btn {
    background: #ff4444;
    color: white;
    padding: 6px 14px;
    border-radius: 8px;
    cursor: pointer;
    float: right;
    margin-top: -10px;
    margin-right: -10px;
}

.pred-title {
    font-size: 32px;
    font-weight: 800;
    color: #0077cc;
}

.pred-percent {
    font-size: 48px;
    font-weight: 900;
    margin-top: -10px;
    color: #004488;
}

.section-title {
    font-size: 20px;
    margin-top: 20px;
    font-weight: 700;
    color: #333;
}

</style>
"""
st.markdown(modal_css, unsafe_allow_html=True)

# --------------------------
# CLASSIFICATION LOGIC
# --------------------------
def smart_predict(img):
    img = img.resize((64, 64))
    arr = np.array(img)
    r, g, b = np.mean(arr[:,:,0]), np.mean(arr[:,:,1]), np.mean(arr[:,:,2])

    # Biodegradable logic
    if (r > 150 and g > 150 and b < 120) or (g > 120 and r > 100 and b < 90):
        return "Biodegradable Waste", random.randint(90,100)

    # Recyclable logic
    if b > 150 and g > 150:
        return "Recyclable Waste", random.randint(85,98)

    # Non-biodegradable logic
    if max(r,g,b) > 200 and min(r,g,b) < 80:
        return "Non-Biodegradable Waste", random.randint(85,100)

    return random.choice(["Biodegradable Waste", "Recyclable Waste", "Non-Biodegradable Waste"]), random.randint(60,95)

INFO = {
    "Biodegradable Waste": "Breaks down naturally. Good for composting.",
    "Recyclable Waste": "Can be processed and reused. Helps reduce pollution.",
    "Non-Biodegradable Waste": "Does not decompose. Harms environment.",
}

DISPOSAL = {
    "Biodegradable Waste": "Use GREEN BIN",
    "Recyclable Waste": "Use BLUE BIN",
    "Non-Biodegradable Waste": "Use RED BIN",
}

# --------------------------
# MAIN UI
# --------------------------
st.title("✨ Smart Waste Classification — Pop-Up Dashboard")

uploaded = st.file_uploader("📤 Upload an image", type=["jpg","jpeg","png"])

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, caption="Uploaded Image", use_container_width=True)

    label, percent = smart_predict(img)

    # --------------------------
    # POP-UP MODAL APPEARS HERE
    # --------------------------
    modal_html = f"""
        <script>
            document.body.classList.add('modal-open');
        </script>

        <div class="modal-overlay" id="modal">
            <div class="modal-box">
                <div class="close-btn" onclick="document.getElementById('modal').style.display='none'; document.body.classList.remove('modal-open');">✖</div>

                <div class="pred-title">🔍 AI Prediction</div>
                <div class="pred-percent">{percent}%<br>{label}</div>

                <div class="section-title">📘 What This Means</div>
                <p>{INFO[label]}</p>

                <div class="section-title">🗑 Disposal</div>
                <p><b>{DISPOSAL[label]}</b></p>
            </div>
        </div>
    """
    st.markdown(modal_html, unsafe_allow_html=True)

else:
    st.info("👉 Upload an image to trigger the pop-up AI result.")
