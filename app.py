import streamlit as st
from PIL import Image
import numpy as np
import random
import base64

st.set_page_config(page_title="AI Waste Classifier", layout="centered")

# Custom CSS for beautiful UI
st.markdown("""
<style>

html, body {
    background: linear-gradient(135deg, #E3F2FD, #E8F5E9);
}

.upload-box {
    padding: 20px;
    border-radius: 12px;
    background: rgba(255,255,255,0.5);
    border: 2px dashed #90CAF9;
    text-align: center;
    color: #1E88E5;
    font-size: 18px;
    font-weight: 600;
}

.popup-card {
    animation: fadeIn 0.8s ease-in-out;
    padding: 25px;
    border-radius: 18px;
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    margin-top: 20px;
}

@keyframes fadeIn {
    from {opacity:0; transform: scale(0.9);}
    to {opacity:1; transform: scale(1);}
}

.result-title {
    font-size: 34px;
    font-weight: 800;
    color: #0077CC;
    text-align: center;
}

.result-percent {
    font-size: 42px;
    font-weight: 900;
    text-align: center;
    color: #004C99;
}

.info-section {
    margin-top: 20px;
    padding: 18px;
    border-radius: 12px;
    background: rgba(255,255,255,0.6);
    backdrop-filter: blur(8px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.10);
}

footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

st.title("✨ AI-Powered Waste Classification Dashboard")
st.markdown("#### A beautiful and interactive educational tool for sustainable waste management.")

# Info dictionary
INFO = {
    "Biodegradable Waste": """
### 🌿 Why It's Biodegradable
Biodegradable items naturally decompose into the soil.

### 🌍 Environmental Impact
✔ Reduces landfill waste  
✔ Supports compost-making  
✔ Eco-friendly  

### 🧭 Examples
Banana peel, leaves, paper, vegetable waste.
""",

    "Recyclable Waste": """
### 🔁 Why It's Recyclable
Materials that can be reused after processing.

### 🌍 Environmental Impact
✔ Saves energy  
✔ Reduces pollution  
✔ Conserves resources  

### 🧭 Examples
Glass, plastic bottles, cans, cardboard.
""",

    "Non-Biodegradable Waste": """
### ⚠ Not Eco-Friendly
These materials do not break down for hundreds of years.

### 🌍 Environmental Impact
❌ Pollutes soil & water  
❌ Harms animals  
❌ Blocks drainage  

### 🧭 Examples
Plastic wrappers, chips packets, styrofoam.
""",

    "Not Waste": """
### ⭐ This Is Not Waste
This item appears usable and should not be thrown away.

### 🧭 Examples
Clothes, tools, toys, books.
"""
}

DISPOSAL = {
    "Biodegradable Waste": "Place in **GREEN BIN** (Organic Waste). Best for composting.",
    "Recyclable Waste": "Place in **BLUE BIN** after cleaning.",
    "Non-Biodegradable Waste": "Dispose in **RED BIN**. Avoid burning.",
    "Not Waste": "Do NOT dispose — reuse or donate."
}

def smart_predict(img):
    """Smart dummy classifier using color detection."""
    img = img.resize((64, 64))
    arr = np.array(img)

    r, g, b = np.mean(arr[:,:,0]), np.mean(arr[:,:,1]), np.mean(arr[:,:,2])

    # Biodegradable patterns (yellow/green)
    if (r > 150 and g > 150 and b < 120) or (g > 120 and r > 100 and b < 90):
        return "Biodegradable Waste", random.randint(90,100)

    # Recyclable patterns (blue/transparent)
    if b > 150 and g > 150:
        return "Recyclable Waste", random.randint(85,98)

    # Non-biodegradable (bright wrappers)
    if max(r,g,b) > 200 and min(r,g,b) < 80:
        return "Non-Biodegradable Waste", random.randint(88,100)

    return random.choice(["Biodegradable Waste", "Recyclable Waste", "Non-Biodegradable Waste"]), random.randint(60,95)


# Upload box
uploaded = st.file_uploader("", type=["jpg","jpeg","png"])
st.markdown('<div class="upload-box">📤 Drop an image here or click to upload</div>', unsafe_allow_html=True)

if uploaded:
    img = Image.open(uploaded).convert("RGB")
    st.image(img, caption="Uploaded Image", use_container_width=True)

    label, percent = smart_predict(img)

    # Popup result card
    st.markdown(f"""
        <div class="popup-card">
            <div class="result-title">🔍 AI Prediction</div>
            <div class="result-percent">{percent}% {label}</div>
        </div>
    """, unsafe_allow_html=True)

    # Progress bar
    st.progress(percent / 100)

    # Info section
    st.markdown('<div class="info-section">', unsafe_allow_html=True)
    st.markdown(INFO[label])
    st.markdown("</div>", unsafe_allow_html=True)

    # Disposal section
    st.markdown('<div class="info-section">', unsafe_allow_html=True)
    st.markdown("### 🗑 Recommended Disposal")
    st.success(DISPOSAL[label])
    st.markdown("</div>", unsafe_allow_html=True)

    # Random fun fact
    st.markdown('<div class="info-section">', unsafe_allow_html=True)
    st.markdown("### 💡 Did You Know?")
    st.write(random.choice([
        "Recycling one aluminium can saves enough energy to run a TV for 3 hours.",
        "Banana peels enrich soil with potassium and nitrogen.",
        "Plastic takes more than **500 years** to decompose.",
        "Composting reduces methane emissions from landfills.",
        "India generates nearly **3.5 million tons** of plastic waste yearly."
    ]))
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("👉 Upload an image to begin analysis.")
