import yaml

from lib.fixtures.channel import Channel


class Chaser:
    def __init__(self, song_name):
        self.song_name = song_name
        self.chase_file = f'songbook/{song_name}.yaml'
        self.cues = self.load_cues()

    def load_cues(self):
        with open(self.chase_file, 'r') as file:
            return yaml.safe_load(file)

    def save_cues(self):
        with open(self.chase_file, 'w') as file:
            yaml.dump(self.cues, file)

    def store_beat(self, beat: int, channels: list[Channel]):
        ## check if beat exists in song/beats
        print(self.cues)

        if 'song' not in self.cues:
            self.cues['song'] = {}
        if 'beats' not in self.cues['song']:
            self.cues['song']['beats'] = {}
        if beat not in self.cues['song']['beats']:
            self.cues['song']['beats'].update({beat: {}})

        ## store the channels
        self.cues['song']['beats'][beat] = channels
        self.save_cues()

    def store_note(self, note: str, channels: list[Channel]):
        ## check if note exists in song/beats
        if 'song' not in self.cues:
            self.cues['song'] = {}
        if 'notes' not in self.cues['song']:
            self.cues['song']['notes'] = {}
        if note not in self.cues['song']['notes']:
            self.cues['song']['notes'].update({note: {}})

        ## store the channels
        self.cues['song']['beats'][note] = channels
        self.save_cues()

    def get_beat(self, beat: int):
        # first check if the beat exists

        # if not, cheack if the beat is a note

        return self.cues['song']['beats'][beat]