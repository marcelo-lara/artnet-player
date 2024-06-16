import json

class Beat:
    def __init__(self, beat_data):
        self.curr_beat_time = beat_data['curr_beat_time']
        self.curr_beat = beat_data['curr_beat']
        self.prev_chord = beat_data.get('prev_chord')
        self.chord_complex_jazz = beat_data.get('chord_complex_jazz')
        self.chord_simple_jazz = beat_data.get('chord_simple_jazz')
        self.chord_complex_pop = beat_data.get('chord_complex_pop')
        self.chord_simple_pop = beat_data.get('chord_simple_pop')

class Song:
    def __init__(self, song_data):
        self.beats = [Beat(beat) for beat in song_data]

    @classmethod
    def from_json_file(cls, file_path):
        with open(file_path, 'r') as f:
            song_data = json.load(f)
        return cls(song_data)
    
    @property
    def song_duration(self):
        return self.beats[-1].curr_beat_time
    
    @property
    def song_num_of_beats(self):
        return len(self.beats)
    