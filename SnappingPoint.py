import math

def normalize_vector(vector):
    x, y = vector
    magnitude = math.sqrt(x**2 + y**2)
    normalized_x = x / magnitude
    normalized_y = y / magnitude
    return normalized_x, normalized_y

def normalize_range(minValue, maxValue, inputValue, scalar=1, high_to_low=False):
    range  =(inputValue - minValue)
    normalized_value = (range / (maxValue - minValue)) * scalar
    if high_to_low:
        normalized_value = scalar - normalized_value
    return max(0, min(normalized_value, scalar))

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

        for i in range(0, len(self.y_coordinates)):
            if self.y_coordinates[i] - y_section_size < self.target_location[1] < self.y_coordinates[i] + y_section_size:
                self.current_location = (self.current_location[0], self.y_coordinates[i])
                break

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

    def GetMacroValue(self):
        # C & D
        semitones = normalize_range(self.y_coordinates[1], self.y_coordinates[0], self.current_location[1], 2,True)
        # E
        semitones += normalize_range(self.y_coordinates[2], self.y_coordinates[1], self.current_location[1], 2,True)
        # F
        semitones += normalize_range(self.y_coordinates[3], self.y_coordinates[2], self.current_location[1], 1,True)
        # G
        semitones += normalize_range(self.y_coordinates[4], self.y_coordinates[3], self.current_location[1], 2,True)
        # A
        semitones += normalize_range(self.y_coordinates[5], self.y_coordinates[4], self.current_location[1], 2,True)
        # B
        semitones += normalize_range(self.y_coordinates[6], self.y_coordinates[5], self.current_location[1], 2,True)
        # C high
        semitones += normalize_range(self.y_coordinates[7], self.y_coordinates[6], self.current_location[1], 1,True)
        # D high
        semitones += normalize_range(self.y_coordinates[8], self.y_coordinates[7], self.current_location[1], 2,True)
        # E high
        semitones += normalize_range(self.y_coordinates[9], self.y_coordinates[8], self.current_location[1], 2,True)
        # F high
        semitones += normalize_range(self.y_coordinates[10], self.y_coordinates[9], self.current_location[1], 1,True)
        # G high
        semitones += normalize_range(self.y_coordinates[11], self.y_coordinates[10], self.current_location[1], 2,True)
        # A high
        semitones += normalize_range(self.y_coordinates[12], self.y_coordinates[11], self.current_location[1], 2,True)
        # B high
        semitones += normalize_range(self.y_coordinates[13], self.y_coordinates[12], self.current_location[1], 2,True)
        # C top
        semitones += normalize_range(self.y_coordinates[14], self.y_coordinates[13], self.current_location[1], 1,True)

        self.macro_value = normalize_range(0,24,semitones, 1, False)
        return self.macro_value