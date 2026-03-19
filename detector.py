import cv2
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(maxHands=1, detectionCon=0.8)

GESTURES = {
    (0, 0, 0, 0, 0): "Rock",
    (1, 1, 1, 1, 1): "Paper",
    (0, 1, 1, 0, 0): "Scissors",
}


def get_gesture(img):
    """
    Takes a frame, detects hand, returns (gesture, img)
    gesture is "Rock", "Paper", "Scissors", "Unknown", or None (no hand)
    """
    hands, img = detector.findHands(img)

    if not hands:
        return None, img

    hand = hands[0]
    fingers = detector.fingersUp(hand)
    gesture = GESTURES.get(tuple(fingers), "Unknown")

    return gesture, img
