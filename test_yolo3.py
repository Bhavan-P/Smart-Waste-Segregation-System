import cv2
import torch
import numpy as np
import matplotlib.pyplot as plt
from ultralytics import YOLO

# Load the trained YOLO model
model = YOLO("waste_yolo.pt")

# Waste classification categories
def classify_waste(label):
    waste_classes = {
        "paper": "Recyclable",
        "plastic": "Non-Recyclable",
        "glass": "Non-Recyclable",
        "metal": "Non-Recyclable",
        "food": "Recyclable"
    }
    return waste_classes.get(label, "Unknown")

# Preprocessing steps
def preprocess_image(image):
    image = cv2.resize(image, (640, 640))  # Resize for model compatibility
    image = cv2.GaussianBlur(image, (5, 5), 0)  # Noise reduction
    return image

# AI Processing Layer
def detect_waste(image):
    results = model(image)  # Object detection
    detections = []
    
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
            label = model.names[int(box.cls)]  # Class label
            confidence = box.conf.item()  # Confidence score
            category = classify_waste(label)  # Get classification
            detections.append((x1, y1, x2, y2, label, confidence, category))
    
    return detections

# Output Layer
def display_results(image, detections):
    for (x1, y1, x2, y2, label, confidence, category) in detections:
        color = (0, 255, 0) if category == "Recyclable" else (0, 0, 255)
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, f"{label} ({category})", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        print(f"🔹 Detected: {label} ({confidence:.2f}) → {category}")
    
    cv2.imshow("Waste Classification", image)
    cv2.waitKey(3000)  # Display results for 3 seconds
    cv2.destroyAllWindows()

# Capture image from camera
def capture_image():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow("Press Space to Capture", frame)
        if cv2.waitKey(1) & 0xFF == ord(' '):  # Capture on spacebar press
            break
    cap.release()
    cv2.destroyAllWindows()
    return frame

# Main function
def main():
    print("Press Space to capture an image...")
    image = capture_image()  # Input Layer
    image = preprocess_image(image)  # Preprocessing layer
    detections = detect_waste(image)  # AI processing layer
    display_results(image, detections)  # Output layer

# Run the classification
if __name__ == "__main__":
    main()
