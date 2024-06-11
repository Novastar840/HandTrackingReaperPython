import math
import cv2
import mediapipe as mp
import reapy
# import the walking point class from the script called walking point
from WalkingPoint import WalkingPoint
from Tools import normalize_range

# --reaper--
#Getting a reference to the first track
current_project = reapy.Project()
first_track = current_project.tracks[0]
print("first track: " + first_track.name)

#Getting a reference to the first fx, in this case vital
first_fx = first_track.fxs[0]
#Getting a reference to the parameter list
fx_params = first_fx.params
#Setting the macro indexes
macro1_index = 211
macro2_index = 212
macro3_index = 213
macro4_index = 214

# --Webcam--
cap = cv2.VideoCapture(0)
rec_x_size = 500
rec_y_size = 500
frame_height = 800
frame_width = 1200
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

mp_drawing = mp.solutions.drawing_utils

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
#Boolean to handle one time calculations within the frame loop
has_been_calculated = False

def draw_rectangle(frame, bottom_left, x_size, y_size, divisions=1, color=(0, 255, 0), thickness=2):
#Draws a rectangle that can be devided horizontally
    top_right = (bottom_left[0] + x_size, bottom_left[1] - y_size)

    # Draw rectangle
    cv2.rectangle(frame, bottom_left, top_right, (200, 0, 0), thickness)

    # Calculate positions for horizontal divisions
    division_positions = []
    for i in range(1, divisions):
        y_coordinate = bottom_left[1] - int(i * y_size / divisions)
        division_positions.append((bottom_left[0],y_coordinate))

    # Draw horizontal division lines
    for pos in division_positions:
        cv2.line(frame, (pos[0], pos[1]), (pos[0] + x_size, pos[1]), color, thickness)

def is_point_inside_rectangle(point, bottom_left, x_size, y_size):
    top_right = (bottom_left[0] + x_size, bottom_left[1] - y_size)

    # Check if point lies within the range of x-coordinates and y-coordinates of the rectangle
    if (bottom_left[0] <= point[0] <= top_right[0]) and (top_right[1] <= point[1] <= bottom_left[1]):
        return True
    else:
        return False

walking_point = WalkingPoint((frame_width/2,frame_height/2) , 40)
def WalkingPointUpdate():
    walking_point.set_target_location(pixel_indexFinger_coordinate)
    walking_point.update_location()
    cv2.circle(mirror_frame, (int(walking_point.current_location[0]), int(walking_point.current_location[1])), 5, (255, 0, 255), -1)
while True:
    success, frame = cap.read()
    if success:
        # flipping frame to make user interaction a bit more intuitive
        mirror_frame = cv2.flip(frame, 1)
        # one time frame calculations
        if has_been_calculated == False:
            rec_bottom_left = (int(mirror_frame.shape[1] // 2 - rec_x_size / 2), int(mirror_frame.shape[0] // 2 + rec_y_size / 2))
            has_been_calculated = True

        draw_rectangle(mirror_frame, rec_bottom_left, rec_x_size, rec_y_size, 1, (0,255,0), 1)

        rgb_img = cv2.cvtColor(mirror_frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_img)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(mirror_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                # get coordinates
                landmark_8 = hand_landmarks.landmark[8]
                ix8 = landmark_8.x
                iy8 = landmark_8.y
                my12 = hand_landmarks.landmark[12].y
                mx12 = hand_landmarks.landmark[12].x
                middle_finger = [mx12, 1 - my12]

            with reapy.inside_reaper():#inside_reaper is used to improve frame rate
                indexFinger = [ix8, 1 - iy8]
                pixel_indexFinger_coordinate = (indexFinger[0] * mirror_frame.shape[1], mirror_frame.shape[0] - indexFinger[1] * mirror_frame.shape[0])
                new_x = (middle_finger[0] - indexFinger[0]) * mirror_frame.shape[1]
                new_y = (middle_finger[1] - indexFinger[1]) * mirror_frame.shape[0]
                diff = math.sqrt(new_x ** 2 + new_y ** 2)
                fx_params[macro3_index] = normalize_range(10, 100, diff)
                WalkingPointUpdate()
                fx_params[macro1_index] = normalize_range(rec_bottom_left[0], rec_bottom_left[0] + rec_x_size, walking_point.current_location[0])
                fx_params[macro2_index] = normalize_range(rec_bottom_left[1], rec_bottom_left[1] - rec_y_size, walking_point.current_location[1])

        cv2.imshow('Capture image',mirror_frame )

        if cv2.waitKey(1) == ord("q"):
            break

cv2.destroyAllWindows()