import cv2
import time
from datetime import datetime, timedelta

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
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Determine if it's an ENTRY or EXIT
                if data not in user_logs or user_logs[data]["status"] == "EXIT":
                    # Mark as ENTRY
                    user_logs[data] = {"status": "ENTRY", "entry_time": datetime.now()}
                    print(f"ENTRY: {data} at {timestamp}")
                else:
                    # Mark as EXIT
                    entry_time = user_logs[data]["entry_time"]
                    exit_time = datetime.now()
                    time_spent = int((exit_time - entry_time).total_seconds() / 60)  # In minutes
                    user_logs[data] = {"status": "EXIT"}
                    print(f"EXIT: {data} at {timestamp} | Time spent: {time_spent:.2f} minutes")

                    # Save data to a log file
                    with open("punch_clock_log.csv", "a") as log_file:
                        log_file.write(f"{data},{entry_time.strftime('%Y-%m-%d %H:%M:%S')},{timestamp},{time_spent:.2f}\n")

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
        with open("punch_clock_log.csv", "x") as log_file:
            log_file.write("User ID,Entry Time,Exit Time,Time Spent (minutes)\n")
    except FileExistsError:
        pass

scan_qr_with_opencv()