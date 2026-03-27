# helmet_detect.py
from ultralytics import YOLO
import cv2

# ✅ Path to your trained YOLOv8 model
model_path = r"C:\Users\poosh\Downloads\env\best.pt"
model = YOLO(model_path)

# ✅ Open the default webcam (change 0 if you have multiple cameras)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Optional: set resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Starting live helmet detection. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Run YOLOv8 detection
    results = model.predict(frame, conf=0.5, verbose=False)  # conf=0.5 threshold

    # Extract predictions
    for r in results:
        boxes = r.boxes.xyxy.cpu().numpy()  # Bounding boxes: [x1, y1, x2, y2]
        scores = r.boxes.conf.cpu().numpy()  # Confidence
        classes = r.boxes.cls.cpu().numpy()  # Class IDs

        for box, score, cls in zip(boxes, scores, classes):
            x1, y1, x2, y2 = map(int, box)
            label = f"{model.names[int(cls)]} {score:.2f}"
            color = (0, 255, 0) if int(cls) == 0 else (0, 0, 255)  # Green=Helmet, Red=No Helmet
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # Show the frame
    cv2.imshow("Helmet Detection", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
