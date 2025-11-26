import cv2
import mediapipe as mp
import random

# -------- إعدادات Mediapipe --------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# -------- إعدادات اللعبة --------
ball_x = 300
ball_y = 50
ball_radius = 30
ball_speed = 10
game_over = False

# -------- الكاميرا --------
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("الكاميرا مش شغالة!")
        break

    frame = cv2.flip(frame, 1)  # صورة المراية
    h, w, _ = frame.shape

    # معالجة اليد
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    hand_x, hand_y = None, None

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            cx = int(hand_landmarks.landmark[9].x * w)
            cy = int(hand_landmarks.landmark[9].y * h)
            hand_x, hand_y = cx, cy
            cv2.circle(frame, (cx, cy), 20, (255, 0, 0), -1)

    # حركة الكورة
    if not game_over:
        ball_y += ball_speed
        cv2.circle(frame, (ball_x, ball_y), ball_radius, (0, 0, 255), -1)

        # لو الكورة خبطت في اليد
        if hand_x and hand_y:
            if abs(ball_x - hand_x) < 50 and abs(ball_y - hand_y) < 50:
                ball_y = 50
                ball_x = random.randint(50, w-50)

        # لو الكورة وصلت لتحت
        if ball_y > h:
            game_over = True

    else:
        cv2.putText(frame, "Game Over!", (150, 250), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 4)

    cv2.imshow("Hand Ball Game", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # زر ESC للخروج
        break

# بعد الحلقة
cap.release()
cv2.destroyAllWindows()
