import streamlit as st
from PIL import Image
import random
import time

st.set_page_config(page_title="Waste Classifier (Educational)", layout="centered")

st.title("♻ Waste Classification — Educational Demo")
st.write("Upload an image below. This demo will simulate how an AI-based waste classifier works and also educate you about proper disposal.")

# Educational explanations for each category
EXPLANATIONS = {
    "Biodegradable Waste": """
    **Biodegradable waste** includes items that decompose naturally.
    These materials break down through bacteria and microorganisms.

    **Examples:** food scraps, fruits, vegetables, paper, leaves, garden waste.

    **Environmental Note:**  
    Biodegradable waste can be turned into **compost**, enriching the soil and reducing landfill load.
    """,

    "Recyclable Waste": """
    **Recyclable waste** includes items that can be processed and reused.

    **Examples:** plastic bottles, cardboard, paper, glass, aluminium cans.

    **Environmental Note:**  
    Recycling saves energy, reduces pollution, and conserves natural resources.
    """,

    "Non-Biodegradable Waste": """
    **Non-biodegradable waste** does NOT decompose naturally.

    **Examples:** plastic wrappers, styrofoam, chips packets, laminated packets.

    **Environmental Note:**  
    These materials pollute land and water, harm animals, and stay for **hundreds of years**.
    Reduce usage wherever possible.
    """,

    "Not Waste": """
    This item does not appear to be waste.

    **Environmental Note:**  
    Consider **reusing**, **donating**, or **repurposing** useful items rather than throwing them away.
    """
}

# Disposal suggestions
DISPOSAL = {
    "Biodegradable Waste": "Dispose in the **GREEN BIN** (Organic Waste). Suitable for composting.",
    "Recyclable Waste": "Dispose in the **BLUE BIN** (Recyclables). Ensure it is clean and dry.",
    "Non-Biodegradable Waste": "Dispose in the **RED BIN** (Dry & Non-recyclable waste).",
    "Not Waste": "Do NOT throw away. Consider reusing or donating."
}

LABELS = [
    "Biodegradable Waste",
    "Recyclable Waste",
    "Non-Biodegradable Waste",
    "Not Waste"
]

uploaded = st.file_uploader("Upload an image", type=["jpg","jpeg","png"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Simulated prediction logic (random but realistic)
    predicted_label = random.choice(LABELS)
    confidence = round(random.uniform(0.70, 1.00), 2)  # 70% – 100%

    percentage = int(confidence * 100)

    st.markdown("---")

    # DISPLAY RESULT IN BIG BOLD FORMAT
    st.markdown(
        f"""
        <div style="padding:15px; background:#f0f9ff; border-left:6px solid #1e88e5; border-radius:5px;">
            <h2 style="margin:0;">🔍 AI Prediction:</h2>
            <h1 style="color:#1e88e5; margin-top:8px;">{percentage}% {predicted_label}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # EDUCATIONAL EXPLANATION
    st.subheader("📘 What This Means")
    st.write(EXPLANATIONS[predicted_label])

    # DISPOSAL GUIDANCE
    st.subheader("🗑 Proper Disposal Method")
    st.success(DISPOSAL[predicted_label])

    st.markdown("---")

    # EXTRA EDUCATION SECTION
    st.subheader("🌍 Why Waste Segregation Matters")
    st.write("""
    Proper waste segregation helps:
    - Reduce landfill waste  
    - Prevent soil and water pollution  
    - Improve recycling efficiency  
    - Save energy and natural resources  
    - Build a cleaner, healthier environment  
    """)

    st.info("This is a **simulated AI model** for educational and hackathon demonstration purposes.")

else:
    st.info("📤 Please upload an image to begin.")
