import threading
import time
import socketio

class Player:
    def __init__(self, song, socketio, next_beat_callback=None):
        self.curr_beat = 0
        self.curr_time = 0
        self.status = 'stopped'
        self.socketio = socketio
        self.timer = None
        self.song = song
        self.bpm = song.bpm
        self.fps = song.bpm / 60
        self.next_beat_callback = next_beat_callback
        self.start_time = 0
        self.play_time = 0
    
    def set_bpm(self, bpm):
        self.bpm = bpm
        self.fps = bpm / 60
        print(f'player BPM set to {bpm} -> {self.fps} FPS')

    @property
    def is_playing(self):
        return self.status == 'playing'

    def play(self, auto=True):
        self.status = 'playing'
        # if auto: self.start_timer()
        self.start_time = time.time()
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
        self._update_timecode()
        self.curr_beat += 1
        if self.next_beat_callback is not None:
            self.next_beat_callback(self.curr_beat)

    ## autoplay
    def timer_callback(self):
        if self.status == 'playing':
            self.next_beat()
            self.start_timer()

    def start_timer(self):
        print(f'[timer] starting timer..')
        self.timer = threading.Timer(1/self.fps, self.timer_callback)
        self.timer.start()

    def stop_timer(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None
    
    ## update UI
    def _update_timecode(self):
        self.play_time = time.time() - self.start_time
        self.curr_time = self.song.beats[self.curr_beat].curr_beat_time
        self.socketio.emit('curr', {'time': self.curr_time, 'beat': self.curr_beat})
        offset = self.curr_time - self.play_time
        print(f".. click [{self.curr_beat} -> {self.song.beats[self.curr_beat].curr_beat_time} ~{offset}]")

    def _update_status(self):
        self.socketio.emit('status', self.status)
        print(f'{self.status}')