import cv2
import time
from detector import get_gesture
from game import Game

game = Game()
game.set_difficulty("easy")  # default difficulty

# states: "waiting", "countdown", "result"
state = "waiting"
countdown_start = None
COUNTDOWN_SEC = 3
result_shown_at = None
RESULT_DISPLAY_SEC = 2

captured_gesture = None


def draw_score(img, score):
    cv2.putText(
        img,
        f"W:{score['wins']}  L:{score['losses']}  D:{score['draws']}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
    )


def draw_difficulty(img, difficulty):
    cv2.putText(
        img,
        f"Mode: {difficulty.upper()}",
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (200, 200, 0),
        2,
    )


def draw_controls(img):
    cv2.putText(
        img,
        "SPACE: play  1:Easy  2:Medium  3:Hard  Q:quit",
        (10, img.shape[0] - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (180, 180, 180),
        1,
    )


cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    gesture, img = get_gesture(img)

    if state == "waiting":
        label = gesture if gesture else "No hand - show your hand!"
        cv2.putText(
            img, label, (30, 110), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3
        )
        cv2.putText(
            img,
            "Press SPACE to start round",
            (30, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (200, 200, 200),
            2,
        )

    elif state == "countdown":
        elapsed = time.time() - countdown_start
        remaining = COUNTDOWN_SEC - int(elapsed)

        if remaining > 0:
            cv2.putText(
                img,
                str(remaining),
                (img.shape[1] // 2 - 30, img.shape[0] // 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                4,
                (0, 200, 255),
                6,
            )
        else:
            # countdown done, capture gesture right now
            captured_gesture = gesture
            if captured_gesture and captured_gesture != "Unknown":
                result = game.play_round(captured_gesture)
                info = game.get_last_round()
                state = "result"
                result_shown_at = time.time()
            else:
                # no valid gesture detected, go back to waiting
                state = "waiting"

    elif state == "result":
        info = game.get_last_round()
        score = game.get_score()

        result_color = {
            "win": (0, 255, 0),
            "loss": (0, 0, 255),
            "draw": (0, 200, 255),
        }.get(info["result"], (255, 255, 255))

        cv2.putText(
            img,
            f"You: {info['player']}  AI: {info['ai']}",
            (30, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (255, 255, 255),
            2,
        )
        cv2.putText(
            img,
            info["result"].upper(),
            (30, 170),
            cv2.FONT_HERSHEY_SIMPLEX,
            2.0,
            result_color,
            4,
        )

        if time.time() - result_shown_at > RESULT_DISPLAY_SEC:
            state = "waiting"

    # always draw score, difficulty, controls
    draw_score(img, game.get_score())
    draw_difficulty(img, game.ai.difficulty)
    draw_controls(img)

    cv2.imshow("RockPaperCVssors", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord(" ") and state == "waiting":
        state = "countdown"
        countdown_start = time.time()
    elif key == ord("1"):
        game.set_difficulty("easy")
    elif key == ord("2"):
        game.set_difficulty("medium")
    elif key == ord("3"):
        game.set_difficulty("hard")

cap.release()
cv2.destroyAllWindows()
