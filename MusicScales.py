
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