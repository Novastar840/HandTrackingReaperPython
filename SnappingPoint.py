from Tools import normalize_range
class SnappingPoint:
    def __init__(self, music_scale, current_location=(0, 0), max_change_rate=1, y_coordinates=None):
        self.current_location = current_location
        self.target_location = current_location
        self.max_change_rate = max_change_rate
        self.initial_max_change_rate = max_change_rate
        self.y_coordinates = y_coordinates
        self.music_scale = music_scale
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
        semitones = self.music_scale.GetSemitones(self.y_coordinates, self.current_location)
        self.macro_value = normalize_range(0,24,semitones, 1, False)
        return self.macro_value