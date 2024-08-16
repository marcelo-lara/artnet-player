import json

class Beat:
    def __init__(self, beat_data):
        self.curr_beat_time = beat_data['curr_beat_time']
        self.curr_beat = beat_data['curr_beat']
        self.prev_chord = beat_data.get('prev_chord')
        self.bass = beat_data.get('bass')
        self.bar_num = beat_data.get('bar_num')
        self.beat_num = beat_data.get('beat_num')
        self.chord_complex_jazz = beat_data.get('chord_complex_jazz')
        self.chord_simple_jazz = beat_data.get('chord_simple_jazz')
        self.chord_complex_pop = beat_data.get('chord_complex_pop')
        self.chord_simple_pop = beat_data.get('chord_simple_pop')
    def __str__(self) -> str:
        return f'{self.chord_complex_pop} [{self.curr_beat_time} | {self.bar_num}:{self.beat_num}]'


class Segment:
    def __init__(self, segment_data):
        self.start = segment_data['start']
        self.end = segment_data['end']
        self.label = segment_data['label']
        self.bars = []
    def __str__(self) -> str:
        return f'{self.label} [{self.start}-{self.end}]'

class Bar:
    def __init__(self, bar_num = 0,  beats=[]):
        self.num = bar_num
        self.beats = beats

class Song:
    def __init__(self, song_data, segments_data, bpm=120):
        self.bpm = bpm
        self.beats = [Beat(beat) for beat in song_data]
        self.segments = [Segment(segment) for segment in segments_data]

    def get_music_sheet(self):
        for segment in self.segments:
            segment.bars = []
            selected_bars = set()
            selected_beats = []
            for beat in self.beats:
                if beat.curr_beat_time >= segment.start and beat.curr_beat_time <= segment.end:
                    selected_bars.add(beat.bar_num)
                    selected_beats.append(beat)

            for bar_num in selected_bars:
                segment.bars.append(Bar(bar_num,[beat for beat in selected_beats if beat.bar_num == bar_num]))

        # for segment in self.segments:
        #     print(segment)
        #     for bar in segment.bars:
        #         print(f'Bar {bar.num}')
        #         for beat in bar.beats:
        #             print(beat)

        return self.segments


    @classmethod
    def from_json_file(cls, song_title):
        chords_file = f'songbook/{song_title}.chords.json'
        segments_file = f'songbook/{song_title}.segments.json'

        with open(segments_file, 'r') as f:
            segments_data = json.load(f)

        with open(chords_file, 'r') as f:
            song_data = json.load(f)
        return cls(song_data, segments_data)
    
    @property
    def song_duration(self):
        return self.beats[-1].curr_beat_time
    
    @property
    def song_num_of_beats(self):
        return len(self.beats)
    
    @property
    def bpm(self):
        return self._bpm
    
    @bpm.setter
    def bpm(self, value):
        self._bpm = value