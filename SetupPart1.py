# importing OpenCV library
import cv2
# importing mediapipe library under a different name
import mediapipe as mp

# captures the frames from the first webcam
cap = cv2.VideoCapture(0)
# sets width and height of the display window
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

# sets a reference to the drawing utilities
mp_drawing = mp.solutions.drawing_utils

# sets up reference to the handtracking modules of the library
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# frame loop
while True:
    # capture the frame
    success, frame = cap.read()
    if success:
        # converting from BGR to RGB image format
        rgb_img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # processing image
        results = hands.process(rgb_img)

        # draws hand landmarks if they are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # displays processed frame to the user
        cv2.imshow('Capture image', frame)

        # allows the user to quit the program by pressing q on the keyboard
        if cv2.waitKey(1) == ord("q"):
            break

# destroys all video windows
cv2.destroyAllWindows()