import math
import cv2
import mediapipe as mp
import reapy
from SnappingPoint import SnappingPoint
from SnappingPoint import normalize_range
from WalkingPoint import WalkingPoint
from MusicScales import Cmajor

# --General Globals--
rec_x_size = 500
rec_y_size = 500
split_item_action_id = 40012
note_border_y_coordinates = []
rec_bottom_left = None
walking_point_toggle = False
# --reaper--
# get firsts track
current_project = reapy.Project()
first_track = current_project.tracks[0]
print("first track: " + first_track.name)
for item in first_track.items:
    print(item.__class__)
# get macro parameters
first_fx = first_track.fxs[0]
fx_params = first_fx.params
macro1_index = 211
macro2_index = 212
macro3_index = 213
macro4_index = 214
print("initialised parameters")

# --webcam--
cap = cv2.VideoCapture(0)
frame_height = 800
frame_width = 1200
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

has_been_calculated = False
mp_drawing = mp.solutions.drawing_utils

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

def draw_rectangle(frame, bottom_left, x_size, y_size, divisions=1, color=(0, 255, 0), thickness=2):

    top_right = (bottom_left[0] + x_size, bottom_left[1] - y_size)

    # Draw rectangle
    cv2.rectangle(frame, bottom_left, top_right, (200, 0, 0), thickness)

    # Calculate positions for horizontal divisions
    division_positions = []
    for i in range(1, divisions):
        y_coordinate = bottom_left[1] - int(i * y_size / divisions)
        division_positions.append((bottom_left[0],y_coordinate))
        if has_been_calculated == False:
            note_border_y_coordinates.append(y_coordinate)

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
if walking_point_toggle == False:
    cmajor_scale = Cmajor()

walking_point = WalkingPoint((frame_width/2,frame_height/2) , 40)

def SnappingPointUpdate():
    snapping_point.set_target_location(pixel_indexFinger_coordinate)
    snapping_point.update_location()
    cv2.circle(mirror_frame, (int(snapping_point.current_location[0]), int(snapping_point.current_location[1])), 5, (255, 0, 255), -1)

def WalkingPointUpdate():
    walking_point.set_target_location(pixel_indexFinger_coordinate)
    walking_point.update_location()
    cv2.circle(mirror_frame, (int(walking_point.current_location[0]), int(walking_point.current_location[1])), 5, (255, 0, 255), -1)
# rec_bottom_left = (int(frame_width // 2 - rec_x_size / 2), int(frame_height // 2 + rec_y_size / 2))
# frame loop
while True:
    success, frame = cap.read()
    if success:
        # center
        # cv2.line(frame, (0, frame.shape[0] // 2), (frame.shape[1], frame.shape[0] // 2), (0, 255, 0), 2)
        # cv2.line(frame, (frame.shape[1] // 2, frame.shape[0]), (frame.shape[1] // 2, 0), (0, 255, 0), 2)

        mirror_frame = cv2.flip(frame, 1)
        # one time frame calculations
        if has_been_calculated == False:
            rec_bottom_left = (int(mirror_frame.shape[1] // 2 - rec_x_size / 2), int(mirror_frame.shape[0] // 2 + rec_y_size / 2))
            if walking_point_toggle == False:
                snapping_point = SnappingPoint(cmajor_scale,current_location=(rec_bottom_left[0], 100), max_change_rate=30, y_coordinates=note_border_y_coordinates)

        if walking_point_toggle == True:
            draw_rectangle(mirror_frame, rec_bottom_left, rec_x_size, rec_y_size, 1, (0,255,0), 1)

        if walking_point_toggle == False:
            draw_rectangle(mirror_frame, rec_bottom_left, rec_x_size, rec_y_size, (cmajor_scale.notes_count * 2) + 2,(0, 255, 0), 1)

        if has_been_calculated == False:
            if walking_point_toggle == False:
                snapping_point.SetYCoordinates(note_border_y_coordinates)
            has_been_calculated = True


        rgb_img = cv2.cvtColor(mirror_frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_img)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(mirror_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                # get coordinates
                landmark_8 = hand_landmarks.landmark[8]
                ix8 = landmark_8.x
                iy8 = landmark_8.y
                if walking_point_toggle == False:
                    location = snapping_point.GetLocation()
                my12 = hand_landmarks.landmark[12].y
                mx12 = hand_landmarks.landmark[12].x
                middle_finger = [mx12, 1 - my12]

            with reapy.inside_reaper():
                # print("macro values = {:.2f} {:.2f} {:.2f} {:.2f}".format(fx_params[macro1_index], fx_params[macro2_index], fx_params[macro3_index], fx_params[macro4_index]))
                indexFinger = [ix8, 1 - iy8]
                pixel_indexFinger_coordinate = (
                indexFinger[0] * mirror_frame.shape[1], mirror_frame.shape[0] - indexFinger[1] * mirror_frame.shape[0])
                newx = (middle_finger[0] - indexFinger[0]) * mirror_frame.shape[1]
                newy = (middle_finger[1] - indexFinger[1]) * mirror_frame.shape[0]
                diff = math.sqrt(newx ** 2 + newy ** 2)
                fx_params[macro3_index] = normalize_range(10, 100, diff)
                if walking_point_toggle == False:
                    fx_params[macro1_index] = snapping_point.GetMacroValue()
                    fx_params[macro2_index] = normalize_range(rec_bottom_left[0], rec_bottom_left[0] + rec_x_size, indexFinger[0] * mirror_frame.shape[1])

                    SnappingPointUpdate()
                else:
                    WalkingPointUpdate()
                    fx_params[macro1_index] = normalize_range(rec_bottom_left[0], rec_bottom_left[0] + rec_x_size, walking_point.current_location[0])
                    fx_params[macro2_index] = normalize_range(rec_bottom_left[1], rec_bottom_left[1] - rec_y_size, walking_point.current_location[1])

        cv2.imshow('Capture image',mirror_frame )

        if cv2.waitKey(1) == ord("q"):
            break

cv2.destroyAllWindows()

