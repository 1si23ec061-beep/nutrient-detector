import streamlit as st
from PIL import Image
import numpy as np
import random

st.set_page_config(page_title="Advanced Waste Classifier", layout="centered")

st.title("♻ Advanced AI Waste Classification Dashboard")
st.write("Upload any image to get classification, environmental impact, and disposal guidance.")

# ===========================
# EDUCATIONAL CONTENT
# ===========================

DETAIL_INFO = {
    "Biodegradable Waste": """
### 🌿 Why It’s Biodegradable
These materials naturally break down through microorganisms.  
Biodegradable waste reduces pollution and can be turned into **nutrient-rich compost**.

### ♻ Environmental Impact
- Reduces landfill volume  
- Supports soil health  
- Low carbon footprint  

### 🧭 Examples
Banana peel, vegetable scraps, leaves, paper towels.

### 💡 Eco Tip
Start a home compost bin! Your biodegradable waste can turn into fertilizer.
""",

    "Recyclable Waste": """
### 🔁 Why It’s Recyclable
Recyclable materials can be **processed and reused**, reducing the need for raw materials.

### ♻ Environmental Impact
- Saves energy  
- Reduces pollution  
- Prevents resource depletion  

### 🧭 Examples
Plastic bottles, cardboard, paper, metal cans.

### 💡 Eco Tip
Always **clean and dry** recyclables before putting them in the blue bin.
""",

    "Non-Biodegradable Waste": """
### ⚠️ Why It’s Non-Biodegradable
These materials do **not** break down naturally.  
They may persist in the environment for **hundreds of years**.

### ♻ Environmental Impact
- Land & water pollution  
- Harmful to animals  
- Blocks drainage systems  

### 🧭 Examples
Plastic wrappers, chips packets, styrofoam, laminated covers.

### 💡 Eco Tip
Try to **avoid single-use plastics**. Carry reusable bags & bottles.
""",

    "Not Waste": """
### ⭐ This Item is Not Waste
This item appears reusable or not meant for disposal.

### 🧭 Examples
Clothes, toys, tools, gadgets, books.

### 💡 Eco Tip
Donate or upcycle instead of throwing away.
"""
}

DISPOSAL = {
    "Biodegradable Waste": "Dispose in **GREEN BIN** — Compost if possible.",
    "Recyclable Waste": "Dispose in **BLUE BIN** — Clean & dry first.",
    "Non-Biodegradable Waste": "Dispose in **RED BIN** — Avoid burning.",
    "Not Waste": "Do NOT throw away — Reuse or donate."
}

def smart_image_predict(image):
    """Advanced dummy classifier using image color patterns."""
    img = image.resize((64, 64))
    arr = np.array(img)

    r, g, b = np.mean(arr[:,:,0]), np.mean(arr[:,:,1]), np.mean(arr[:,:,2])

    # Biodegradable: yellows, greens, browns
    if (r > 150 and g > 150 and b < 110) or (g > 120 and r > 100 and b < 100):
        return "Biodegradable Waste", random.randint(90,100)

    # Recyclable: bluish/transparent colors
    if b > 150 and g > 150:
        return "Recyclable Waste", random.randint(85,98)

    # Non-biodegradable: saturated bright colors, reds, metallic
    if max(r, g, b) > 200 and min(r, g, b) < 80:
        return "Non-Biodegradable Waste", random.randint(88,100)

    # Unknown → guess
    return random.choice(["Biodegradable Waste", "Recyclable Waste", "Non-Biodegradable Waste"]), random.randint(60,95)


uploaded = st.file_uploader("📤 Upload an image", type=["jpg","jpeg","png"])

if uploaded:

    img = Image.open(uploaded).convert("RGB")
    st.image(img, use_column_width=True)

    # Prediction
    label, percent = smart_image_predict(img)

    # Classification Card
    st.markdown(f"""
        <div style="padding:18px; border-radius:10px; background:#f3faff; border-left:6px solid #0077cc;">
            <h2 style="margin:0;">🔍 AI Prediction</h2>
            <h1 style="color:#0077cc; margin-top:10px;">{percent}% {label}</h1>
        </div>
    """, unsafe_allow_html=True)

    # Confidence progress bar
    st.progress(percent / 100)

    # Environmental Explanation
    st.markdown("## 🌍 Detailed Environmental Information")
    st.write(DETAIL_INFO[label])

    # Proper Disposal
    st.markdown("## 🗑 Recommended Disposal")
    st.success(DISPOSAL[label])

    # Did You Know section
    st.markdown("---")
    st.markdown("### 💡 Did You Know?")
    st.write(random.choice([
        "Recycling 1 plastic bottle saves enough energy to power a light bulb for 3 hours.",
        "Composting reduces methane emissions from landfills.",
        "India generates more than 3.4 million tonnes of plastic waste every year.",
        "Banana peels enrich soil with potassium and nitrogen when composted.",
        "Non-biodegradable plastics remain in the environment for over 500 years."
    ]))

    st.markdown("---")
    st.info("This is a **simulated AI classifier** designed for educational and hackathon demos.")

else:
    st.info("📤 Upload an image to begin.")
