import cv2
import time
from datetime import datetime, timedelta
#import csv
#from collections import defaultdict

# Dictionary to track the status of each user
user_logs = {}

def scan_qr_with_opencv():
    cap = cv2.VideoCapture(1)
    detector = cv2.QRCodeDetector()

    last_detected_time = 0  # Timestamp of the last detection
    detection_delay = 1  # Time in seconds between scans

    print("Scanning for QR codes. Press 'q' to quit.")


    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not access the camera.")
            break

        # Detect and decode QR code
        data, bbox, _ = detector.detectAndDecode(frame)

        # Process detected QR code if data is found and delay has passed
        if data:
            current_time = time.time()
            if current_time - last_detected_time > detection_delay:
                # Get current datetime
                now = datetime.now()
                date = now.strftime("%Y-%m-%d")  # Extract date
                time_now = now.strftime("%H:%M:%S")  # Extract time

                # Determine if it's an ENTRY or EXIT
                if data not in user_logs or user_logs[data]["status"] == "EXIT":
                    # Mark as ENTRY
                    user_logs[data] = {"status": "ENTRY", "entry_time": now}
                    print(f"ENTRY: {data} at {date} {time_now}")
                else:
                    # Mark as EXIT
                    entry_time = user_logs[data]["entry_time"]
                    exit_time = now
                    time_spent = (exit_time - entry_time).total_seconds() / 60  # In minutes
                    user_logs[data] = {"status": "EXIT"}
                    print(f"EXIT: {data} at {date} {time_now} | Time spent: {time_spent:.2f} minutes")

                    # Save data to a log file
                    with open("punch_clock_log_v2.csv", "a") as log_file:
                        log_file.write(f"{data},{date},{entry_time.strftime('%H:%M:%S')},{time_now},{time_spent:.2f}\n")

                last_detected_time = current_time

        # Display the camera feed
        cv2.imshow("QR Scanner", frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Add CSV header if the file doesn't exist
    try:
        with open("punch_clock_log_v2.csv", "x") as log_file:
            log_file.write("User ID,Date,Entry Time,Exit Time,Time Spent (minutes)\n")
    except FileExistsError:
        pass

    scan_qr_with_opencv()