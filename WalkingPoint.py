import math
from Tools import normalize_vector

class WalkingPoint:
    def __init__(self, current_location=(0, 0), max_change_rate=1):
        self.current_location = current_location
        self.target_location = current_location
        self.max_change_rate = max_change_rate
        self.initial_max_change_rate = max_change_rate

    def set_target_location(self, target_location):
        self.target_location = target_location

    def update_location(self):
        x_diff = self.target_location[0] - self.current_location[0]
        y_diff = self.target_location[1] - self.current_location[1]
        magnitude = math.sqrt(x_diff ** 2 + y_diff ** 2)

        if magnitude < 5:
            self.max_change_rate = 1
        elif magnitude < 10:
            self.max_change_rate = 3
        elif magnitude < 30:
            self.max_change_rate = 6
        else:
            self.max_change_rate = self.initial_max_change_rate
        # Calculate the maximum change allowed based on the max change rate
        normalized_vector = normalize_vector((x_diff, y_diff))
        max_change_x = normalized_vector[0] * self.max_change_rate
        max_change_y = normalized_vector[1] * self.max_change_rate

        # Calculate the new coordinates
        new_x = self.current_location[0] + max_change_x
        new_y = self.current_location[1] + max_change_y

        self.current_location = (new_x, new_y)

    def GetLocation(self):
        return self.current_location
