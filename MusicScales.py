from Tools import normalize_range
class Cmajor():
    def __init__(self):
        self.notes_count = 7
        self.midi_notes = [48, 50, 52, 53, 55, 57, 59]
    def GetNotesCount(self):
        return self.notes_count
    def GetMidiNotes(self):
        return self.midi_notes
    def GetMidiNote(self,border_y_coordinates, walking_point_y_coordinate):
        if walking_point_y_coordinate > border_y_coordinates[0]:
            return self.midi_notes[0]
        elif walking_point_y_coordinate > border_y_coordinates[1]:
            return self.midi_notes[1]
        elif walking_point_y_coordinate > border_y_coordinates[2]:
            return self.midi_notes[2]
        elif walking_point_y_coordinate > border_y_coordinates[3]:
            return self.midi_notes[3]
        elif walking_point_y_coordinate > border_y_coordinates[4]:
            return self.midi_notes[4]
        elif walking_point_y_coordinate > border_y_coordinates[5]:
            return self.midi_notes[5]

    def GetSemitones(self, y_coordinates, current_location):
        # C & D
        semitones = normalize_range(y_coordinates[1], y_coordinates[0], current_location[1], 2, True)
        # E
        semitones += normalize_range(y_coordinates[2], y_coordinates[1], current_location[1], 2, True)
        # F
        semitones += normalize_range(y_coordinates[3], y_coordinates[2], current_location[1], 1, True)
        # G
        semitones += normalize_range(y_coordinates[4], y_coordinates[3], current_location[1], 2, True)
        # A
        semitones += normalize_range(y_coordinates[5], y_coordinates[4], current_location[1], 2, True)
        # B
        semitones += normalize_range(y_coordinates[6], y_coordinates[5], current_location[1], 2, True)
        # C high
        semitones += normalize_range(y_coordinates[7], y_coordinates[6], current_location[1], 1, True)
        # D high
        semitones += normalize_range(y_coordinates[8], y_coordinates[7], current_location[1], 2, True)
        # E high
        semitones += normalize_range(y_coordinates[9], y_coordinates[8], current_location[1], 2, True)
        # F high
        semitones += normalize_range(y_coordinates[10], y_coordinates[9], current_location[1], 1, True)
        # G high
        semitones += normalize_range(y_coordinates[11], y_coordinates[10], current_location[1], 2, True)
        # A high
        semitones += normalize_range(y_coordinates[12], y_coordinates[11], current_location[1], 2, True)
        # B high
        semitones += normalize_range(y_coordinates[13], y_coordinates[12], current_location[1], 2, True)
        # C top
        semitones += normalize_range(y_coordinates[14], y_coordinates[13], current_location[1], 1, True)
        return semitones