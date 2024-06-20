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
        self.fps = song.bpm / 60

    def play(self):
        self.status = 'playing'
        self.start_timer()
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

    def next_frame(self):
        self.curr_time = self.song.beats[self.curr_beat].curr_beat_time

    def timer_callback(self):
        if self.status == 'playing':
            self.next_frame()
            self.next_beat()

            # Emit the current beat
            self._update_timecode()

            # call the next beat every 4 frames
            self.start_timer()

    def start_timer(self):
        self.timer = threading.Timer(1/self.fps, self.timer_callback)
        self.timer.start()

    def stop_timer(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None
    
    def _update_timecode(self):
        print(f".. click [{self.curr_beat} -> {self.song.beats[self.curr_beat].curr_beat_time}]")
        self.socketio.emit('curr', {'time': self.curr_time, 'beat': self.curr_beat})

    def _update_status(self):
        self.socketio.emit('status', self.status)
        print(f'{self.status}')