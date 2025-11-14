import streamlit as st
import numpy as np
import cv2
from PIL import Image
import tensorflow as tf
from mtcnn import MTCNN

# -------------------------
# Load Model
# -------------------------
model = tf.keras.models.load_model("model/vitamin_model.h5")

# Classes (edit according to your model)
CLASSES = [
    "Vitamin A Deficiency",
    "Vitamin B12 Deficiency",
    "Vitamin C Deficiency",
    "Vitamin D Deficiency",
    "Iron Deficiency",
    "Healthy / No Deficiency"
]

# Face Detector
detector = MTCNN()

# -------------------------
# Image Preprocessing
# -------------------------
def enhance_image(img):
    """Improve lighting & quality automatically"""
    img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(img)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    enhanced = cv2.merge((cl, a, b))
    return cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

def prepare_for_model(face_img):
    """Resize + normalize image"""
    face_img = cv2.resize(face_img, (224, 224))
    face_img = face_img.astype("float32") / 255.0
    return np.expand_dims(face_img, axis=0)

# -------------------------
# Prediction Function
# -------------------------
def predict_deficiency(face_img):
    processed = prepare_for_model(face_img)
    preds = model.predict(processed)[0]
    class_id = np.argmax(preds)
    confidence = preds[class_id] * 100
    return CLASSES[class_id], confidence

# -------------------------
# Streamlit UI
# -------------------------
st.title("AI-Based Vitamin Deficiency Detector")
st.write("Upload a face image — the AI will detect nutrient deficiency.")

uploaded = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded:
    img = Image.open(uploaded)
    img_np = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    st.image(img, caption="Uploaded Image", use_column_width=True)

    # -------------------------
    # Detect Face Regions
    # -------------------------
    st.subheader("Detecting Face...")
    detected = detector.detect_faces(img_np)

    if len(detected) == 0:
        st.error("No face detected! Try another image or better lighting.")
    else:
        for i, face in enumerate(detected):
            x, y, w, h = face["box"]
            face_img = img_np[y:y+h, x:x+w]

            # Enhance face region
            enhanced_face = enhance_image(face_img)

            st.image(
                cv2.cvtColor(enhanced_face, cv2.COLOR_BGR2RGB),
                caption=f"Processed Face Region {i+1}",
                width=250
            )

            # -------------------------
            # Predict Vitamin Deficiency
            # -------------------------
            label, confidence = predict_deficiency(enhanced_face)

            st.success(f"Prediction: **{label}**")
            st.info(f"Confidence: **{confidence:.2f}%**")

            # Display probability bar
            st.progress(min(int(confidence), 100))
