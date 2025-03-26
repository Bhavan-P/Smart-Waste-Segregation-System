from flask import Flask, request, jsonify
import cv2
import numpy as np
from ultralytics import YOLO
from flask_cors import CORS  # Enable CORS for frontend-backend communication

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Load YOLO model
model = YOLO("waste_yolo.pt")

# Classification function
def classify_waste(label):
    waste_classes = {
        "paper": "Recyclable",
        "plastic": "Non-Recyclable",
        "glass": "Non-Recyclable",
        "metal": "Non-Recyclable",
        "food": "Recyclable"
    }
    return waste_classes.get(label, "Unknown")

@app.route("/")
def home():
    return "Waste Classification API is running!"

@app.route("/classify", methods=["POST"])
def classify():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files["image"]
    image = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    
    # Process image through YOLO
    results = model(image)
    detections = []
    
    for result in results:
        for box in result.boxes:
            label = model.names[int(box.cls)]
            category = classify_waste(label)
            detections.append({"label": label, "category": category})
    
    return jsonify(detections[0] if detections else {"label": "Unknown", "category": "Unknown"})

if __name__ == "__main__":
    app.run(debug=True)
