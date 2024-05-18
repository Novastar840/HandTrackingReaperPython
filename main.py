import cv2
import mediapipe as mp
import reapy
from SnappingPoint import SnappingPoint
from MusicScales import Cmajor

# --General Globals--
rec_x_size = 1000
rec_y_size = 500
split_item_action_id = 40012
note_border_y_coordinates = []
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
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

has_been_calculated = False
mp_drawing = mp.solutions.drawing_utils

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()



def normalize_range(min, max, inputValue, scalar=1):
    normalized_value = ((inputValue - min) / (max - min) - 1) * scalar
    print(normalized_value)
    return normalized_value

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

cmajor_scale = Cmajor()
snapping_point = SnappingPoint(current_location=(100, 100), max_change_rate=30, y_coordinates=note_border_y_coordinates)
def SnappingPointUpdate():
    snapping_point.set_target_location(pixel_indexFinger_coordinate)
    snapping_point.update_location()
    cv2.circle(frame, (int(snapping_point.current_location[0]), int(snapping_point.current_location[1])), 5, (255, 0, 255), -1)

# frame loop
while True:
    success, frame = cap.read()
    if success:
        # center
        # cv2.line(frame, (0, frame.shape[0] // 2), (frame.shape[1], frame.shape[0] // 2), (0, 255, 0), 2)
        # cv2.line(frame, (frame.shape[1] // 2, frame.shape[0]), (frame.shape[1] // 2, 0), (0, 255, 0), 2)

        # one time frame calculations
        if has_been_calculated == False:
            rec_bottom_left = (int(frame.shape[1] // 2 - rec_x_size / 2), int(frame.shape[0] // 2 + rec_y_size / 2))


        draw_rectangle(frame, rec_bottom_left, rec_x_size, rec_y_size, cmajor_scale.notes_count + 1,(0, 255, 0), 1)

        if has_been_calculated == False:
            snapping_point.SetYCoordinates(note_border_y_coordinates)
            has_been_calculated = True



        if current_project.is_playing and is_point_inside_rectangle(snapping_point.GetLocation(),rec_bottom_left, rec_x_size, rec_y_size):
            if len(first_track.items) == 0:
                first_track.add_midi_item(current_project.cursor_position, current_project.cursor_position + 100)
                first_track.select()
            print(snapping_point.GetLocation())


        rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_img)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                # get coordinates
                landmark_8 = hand_landmarks.landmark[8]
                x8 = landmark_8.x
                y8 = landmark_8.y
                location = snapping_point.GetLocation()
            with reapy.inside_reaper():
                # print("macro values = {:.2f} {:.2f} {:.2f} {:.2f}".format(fx_params[macro1_index], fx_params[macro2_index], fx_params[macro3_index], fx_params[macro4_index]))
                indexFinger = (x8, 1 - y8)
                fx_params[macro1_index] = normalize_range(rec_bottom_left[1] + rec_y_size, rec_bottom_left[1], location[1], 1)
                fx_params[macro2_index] = indexFinger[0]

            pixel_indexFinger_coordinate = (indexFinger[0] * frame.shape[1], frame.shape[0] - indexFinger[1] * frame.shape[0])

            SnappingPointUpdate()

        cv2.imshow('Capture image', frame)

        if cv2.waitKey(1) == ord("q"):
            break

cv2.destroyAllWindows()

