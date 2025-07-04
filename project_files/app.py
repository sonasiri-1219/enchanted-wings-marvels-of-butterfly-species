import tensorflow as tf
from tensorflow.keras.models import load_model
import joblib
import numpy as np
import cv2
import os

# ------------------ CONFIG ------------------ #
MODEL_PATH = "best_model_mobilenet.keras"
ENCODER_PATH = "label_encoder.pkl"
IMG_SIZE = (224, 224)

# ------------------ LOAD MODEL AND ENCODER ------------------ #
print("🔄 Loading model and label encoder...")
model = load_model(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)

# ------------------ PREDICTION FUNCTION ------------------ #
def predict_image(img_path):
    image = cv2.imread(img_path)
    if image is None:
        print(f"❌ Error: Could not read image from {img_path}")
        return None, None
    image = cv2.resize(image, IMG_SIZE)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)

    preds = model.predict(image)
    class_index = np.argmax(preds)
    class_name = label_encoder.inverse_transform([class_index])[0]
    confidence = np.max(preds)

    return class_name, confidence

# ------------------ TEST ------------------ #
if __name__ == "__main__":
    test_img = input("📷 Enter path to butterfly image: ").strip()

    if os.path.exists(test_img):
        label, conf = predict_image(test_img)
        if label is not None:
            print(f"\n🦋 Predicted Species: {label} (Confidence: {conf:.2f})")
    else:
        print("❌ File not found. Please check the path.")