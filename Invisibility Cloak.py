import cv2
import numpy as np
import time

def apply_invisible_cloak(frame, background):
    # Convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Green cloak range (adjust if needed)
    lower_green = np.array([25, 40, 40])
    upper_green = np.array([95, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Clean mask using morphological operations
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=1)

    # Inverse mask to keep visible parts of frame
    mask_inv = cv2.bitwise_not(mask)

    # Segment out cloak area from background
    cloak_area = cv2.bitwise_and(background, background, mask=mask)
    visible_area = cv2.bitwise_and(frame, frame, mask=mask_inv)

    # Combine both to get final output
    final_output = cv2.addWeighted(cloak_area, 1, visible_area, 1, 0)

    # Add overlay text
    cv2.putText(final_output, "Invisible Cloak Active", (30,50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

    return final_output, mask

# ------------------ Main Program ------------------
cap = cv2.VideoCapture(0)
time.sleep(2)  # wait for camera to warm up

print("Capturing background... Please stay out of frame.")
background = None
# Capture multiple frames and take the last one as background
for i in range(60):
    ret, background = cap.read()
if not ret:
    print("Error: Cannot capture background")
    cap.release()
    exit()

print("Background captured! Start cloak effect...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    output, mask = apply_invisible_cloak(frame, background)

    # Show the output and the mask for debugging
    cv2.imshow("Cloak Effect", output)
    cv2.imshow("Mask", mask)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
