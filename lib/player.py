import threading

import socketio

class Player:
    def __init__(self, song, socketio):
        self.curr_beat = 0
        self.curr_time = 0
        self.status = 'stopped'
        self.socketio = socketio
        self.timer = None
        self.song = song
        self.bpm = song.bpm
        self.fps = song.bpm / 60
    
    def set_bpm(self, bpm):
        self.bpm = bpm
        self.fps = bpm / 60
        print(f'player BPM set to {bpm} -> {self.fps} FPS')

    @property
    def is_playing(self):
        return self.status == 'playing'

    def play(self, auto=True):
        self.status = 'playing'
        if auto: self.start_timer()
        self._update_status()

    def pause(self):
        self.status = 'paused'
        self.stop_timer()
        self._update_status()

    def stop(self):
        self.status = 'stopped'
        self.curr_beat = 0
        self.curr_time = 0
        self.stop_timer()
        self._update_status()
        self._update_timecode()

    def next_beat(self):
        self.curr_beat += 1
        self._update_timecode()

    ## autoplay
    def timer_callback(self):
        if self.status == 'playing':
            self.next_beat()
            self.start_timer()

    def start_timer(self):
        self.timer = threading.Timer(1/self.fps, self.timer_callback)
        self.timer.start()

    def stop_timer(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None
    
    ## update UI
    def _update_timecode(self):
        self.curr_time = self.song.beats[self.curr_beat].curr_beat_time
        self.socketio.emit('curr', {'time': self.curr_time, 'beat': self.curr_beat})
        print(f".. click [{self.curr_beat} -> {self.song.beats[self.curr_beat].curr_beat_time}]")

    def _update_status(self):
        self.socketio.emit('status', self.status)
        print(f'{self.status}')