import math

def normalize_vector(vector):
    x, y = vector
    magnitude = math.sqrt(x**2 + y**2)
    normalized_x = x / magnitude
    normalized_y = y / magnitude
    return normalized_x, normalized_y


class SnappingPoint:
    def __init__(self, current_location=(0, 0), max_change_rate=1, y_coordinates=None):
        self.current_location = current_location
        self.target_location = current_location
        self.max_change_rate = max_change_rate
        self.initial_max_change_rate = max_change_rate
        self.y_coordinates = y_coordinates
    def set_target_location(self, target_location):
        self.target_location = target_location

    def update_location(self):
        y_diff = self.target_location[1] - self.current_location[1]
        y_section_size = self.y_coordinates[0] - self.y_coordinates[1]

        if self.y_coordinates[0] - y_section_size < self.target_location[1]:
            self.current_location = (self.current_location[0], self.y_coordinates[0])
        elif self.y_coordinates[1] - y_section_size < self.target_location[1] < self.y_coordinates[1] + y_section_size:
            self.current_location = (self.current_location[0], self.y_coordinates[1])
        elif self.y_coordinates[2] - y_section_size < self.target_location[1] < self.y_coordinates[2] + y_section_size:
            self.current_location = (self.current_location[0], self.y_coordinates[2])
        elif self.y_coordinates[3] - y_section_size < self.target_location[1] < self.y_coordinates[3] + y_section_size:
            self.current_location = (self.current_location[0], self.y_coordinates[3])
        elif self.y_coordinates[4] - y_section_size < self.target_location[1] < self.y_coordinates[4] + y_section_size:
            self.current_location = (self.current_location[0], self.y_coordinates[4])
        elif self.y_coordinates[5] - y_section_size < self.target_location[1] < self.y_coordinates[5] + y_section_size:
            self.current_location = (self.current_location[0], self.y_coordinates[5])

        if abs(y_diff) < 5:
            self.max_change_rate = 1
        elif abs(y_diff) < 10:
            self.max_change_rate = 3
        elif abs(y_diff) < 30:
            self.max_change_rate = 6
        else:
            self.max_change_rate = self.initial_max_change_rate

        #if self.target_location[1] > self.current_location[1]:
            #new_y = self.current_location[1] + self.max_change_rate
            #self.current_location = (self.current_location[0], new_y)
        #elif self.target_location[1] < self.current_location[1]:
            #new_y = self.current_location[1] - self.max_change_rate
            #self.current_location = (self.current_location[0], new_y)

    def GetLocation(self):
        return self.current_location

    def SetYCoordinates(self, y_coordinates):
        self.y_coordinates = y_coordinates
