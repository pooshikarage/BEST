from ultralytics import YOLO
import cv2
import time
import requests
import random
import math


# ============================================================
# TELEGRAM SETUP
# ============================================================

BOT_TOKEN = "8905754445:AAGTxy9yb4zKDU_mbiAseMT_0hXFGVM3REs"
CHAT_ID = "7791073997"


# ============================================================
# SRI SAIRAM ENGINEERING COLLEGE LOCATION
# ============================================================

BASE_LAT = 12.9603
BASE_LON = 80.0574

# Maximum distance from the college in metres
MAX_DISTANCE = 100


# ============================================================
# ALERT SETTINGS
# ============================================================

COOLDOWN_TIME = 60
last_sent_time = 0


# ============================================================
# GENERATE RANDOM GPS LOCATION
# ============================================================

def generate_random_gps():

    # Random distance from college
    distance = random.uniform(10, MAX_DISTANCE)

    # Random direction
    angle = random.uniform(0, 2 * math.pi)

    # Convert metres to latitude degrees
    lat_offset = (
        distance * math.cos(angle)
    ) / 111320

    # Convert metres to longitude degrees
    lon_offset = (
        distance * math.sin(angle)
    ) / (
        111320 * math.cos(math.radians(BASE_LAT))
    )

    latitude = BASE_LAT + lat_offset
    longitude = BASE_LON + lon_offset

    return latitude, longitude


# ============================================================
# SEND TELEGRAM ALERT
# ============================================================

def send_telegram_alert():

    global last_sent_time

    current_time = time.time()

    # --------------------------------------------------------
    # COOLDOWN
    # --------------------------------------------------------

    if current_time - last_sent_time < COOLDOWN_TIME:

        remaining = int(
            COOLDOWN_TIME -
            (current_time - last_sent_time)
        )

        print(
            f"⏳ Telegram cooldown active."
            f" {remaining} seconds remaining."
        )

        return


    # --------------------------------------------------------
    # GENERATE RANDOM LOCATION
    # --------------------------------------------------------

    latitude, longitude = generate_random_gps()


    # --------------------------------------------------------
    # GOOGLE MAPS LINK
    # --------------------------------------------------------

    maps_link = (
        f"https://www.google.com/maps/search/"
        f"?api=1&query={latitude:.6f},{longitude:.6f}"
    )


    # --------------------------------------------------------
    # TELEGRAM MESSAGE
    # --------------------------------------------------------

    message = (
        "🚨 GARBAGE DETECTED 🚨\n\n"

        "🛰️ Drone: PX-01\n"
        "🤖 AI System: YOLO Garbage Detection\n\n"

        "🗑️ Status: Garbage Detected\n\n"

        "📍 GPS LOCATION\n"
        f"Latitude: {latitude:.6f}\n"
        f"Longitude: {longitude:.6f}\n\n"

        "🗺️ OPEN LOCATION IN GOOGLE MAPS\n"
        f"{maps_link}\n\n"

        "⚠️ Please inspect the detected location.\n\n"

        "ℹ️ GPS coordinates are simulated "
        "around Sri Sairam Engineering College "
        "for demonstration."
    )


    # --------------------------------------------------------
    # TELEGRAM API
    # --------------------------------------------------------

    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage"
    )

    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "disable_web_page_preview": False
    }


    # --------------------------------------------------------
    # SEND MESSAGE
    # --------------------------------------------------------

    try:

        response = requests.post(
            url,
            data=data,
            timeout=10
        )

        if response.status_code == 200:

            print()
            print("====================================")
            print("📨 TELEGRAM ALERT SENT")
            print("====================================")
            print(
                f"📍 Latitude  : {latitude:.6f}"
            )
            print(
                f"📍 Longitude : {longitude:.6f}"
            )
            print(
                f"🗺️ Map       : {maps_link}"
            )
            print("====================================")
            print()

            last_sent_time = current_time

        else:

            print("❌ Telegram message failed")
            print(response.text)

    except requests.RequestException as error:

        print("❌ Telegram connection error:")
        print(error)


# ============================================================
# LOAD YOLO MODEL
# ============================================================

print()
print("====================================")
print("🤖 LOADING YOLO MODEL")
print("====================================")

model = YOLO("best1.pt")

print("✅ YOLO model loaded successfully")


# ============================================================
# OPEN CAMERA
# ============================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():

    print("❌ ERROR: Could not open camera")
    exit()


print("📷 Camera started")
print("🚁 Garbage detection system running")
print()
print("📍 GPS simulation centre:")
print("Sri Sairam Engineering College")
print(f"Latitude : {BASE_LAT}")
print(f"Longitude: {BASE_LON}")
print(f"Radius   : {MAX_DISTANCE} metres")
print()
print("Press Q to quit")
print("====================================")


# ============================================================
# MAIN DETECTION LOOP
# ============================================================

while True:

    ret, frame = cap.read()

    if not ret:

        print("❌ Could not read camera frame")
        break


    # --------------------------------------------------------
    # YOLO DETECTION
    # --------------------------------------------------------

    results = model(frame)


    # --------------------------------------------------------
    # DRAW DETECTIONS
    # --------------------------------------------------------

    annotated = results[0].plot()


    # --------------------------------------------------------
    # DISPLAY CAMERA
    # --------------------------------------------------------

    cv2.imshow(
        "Garbage Detection - PX-01",
        annotated
    )


    # --------------------------------------------------------
    # CHECK IF OBJECT WAS DETECTED
    # --------------------------------------------------------

    if (
        results[0].boxes is not None
        and len(results[0].boxes) > 0
    ):

        print("🚨 GARBAGE DETECTED!")

        # Send Telegram notification
        send_telegram_alert()


    # --------------------------------------------------------
    # PRESS Q TO QUIT
    # --------------------------------------------------------

    if cv2.waitKey(1) & 0xFF == ord("q"):

        print()
        print("🛑 Stopping system...")
        break


# ============================================================
# CLEANUP
# ============================================================

cap.release()
cv2.destroyAllWindows()

print("✅ System stopped successfully")
