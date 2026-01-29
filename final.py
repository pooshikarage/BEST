from ultralytics import YOLO
import cv2
import time
from twilio.rest import Client

# =========================
# TWILIO SETUP
# =========================
account_sid = "ACe1322f5e137fba1bab5d01d4e7859feb"
auth_token = "8327fad75b5cf9b2b9e00d60f7aa3d60"

client = Client(account_sid, auth_token)

TWILIO_NUMBER = "+19146771225"
USER_NUMBER   = "+919361319454"

COOLDOWN_TIME = 60  # seconds
last_sent_time = 0

def send_sms_alert():
    global last_sent_time
    current_time = time.time()

    if current_time - last_sent_time < COOLDOWN_TIME:
        return

    message = client.messages.create(
        body="🚨 Detection Alert: Garbage Detected!",
        from_=TWILIO_NUMBER,
        to=USER_NUMBER
    )

    print("📨 SMS sent:", message.sid)
    last_sent_time = current_time


# =========================
# 🔍 YOUR DETECTION CODE (UNCHANGED)
# =========================
model = YOLO("best1.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    annotated = results[0].plot()

    cv2.imshow("Garbage Detection", annotated)

    # =========================
    # ✅ ADDED LOGIC (NO CHANGE ABOVE)
    # =========================
    if results[0].boxes is not None and len(results[0].boxes) > 0:
        send_sms_alert()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
