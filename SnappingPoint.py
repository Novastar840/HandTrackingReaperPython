from Tools import normalize_range
class SnappingPoint:
    def __init__(self, music_scale, current_location=(0, 0), y_coordinates=None):
        self.current_location = current_location
        self.target_location = current_location
        self.y_coordinates = y_coordinates
        self.music_scale = music_scale
    def set_target_location(self, target_location):
        self.target_location = target_location

    def update_location(self):
        y_section_size = self.y_coordinates[0] - self.y_coordinates[1]
        # checks for which division the target is located
        for i in range(0, len(self.y_coordinates)):
            if self.y_coordinates[i] - y_section_size < self.target_location[1] < self.y_coordinates[i] + y_section_size:
                self.current_location = (self.current_location[0], self.y_coordinates[i])
                break

    def GetLocation(self):
        return self.current_location

    def SetYCoordinates(self, y_coordinates):
        self.y_coordinates = y_coordinates

    def GetMacroValue(self):
        semitones = self.music_scale.GetSemitones(self.y_coordinates, self.current_location)
        self.macro_value = normalize_range(0,24,semitones, 1, False)
        return self.macro_value