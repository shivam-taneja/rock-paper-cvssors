import cv2
from detector import get_gesture

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    gesture, img = get_gesture(img)
    print(f"Gesture: {gesture}")

    label = gesture if gesture else "No hand"
    cv2.putText(img, label, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

    cv2.imshow("RockPaperCVssors", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
