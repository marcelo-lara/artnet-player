import asyncio
from operator import is_
import os
from flask import Flask, render_template
from flask_socketio import SocketIO
from aalink import Link
from threading import Thread

# create the Flask app
app = Flask(__name__, template_folder='html')
socketio = SocketIO(app)


from lib.player import Player
from lib.song import Song

# load the song from the JSON file
# a song is a collection of beats and chords in groups of 4 beats
song = Song.from_json_file('songbook/obsession.json')

# print the duration of the song
print(song.song_duration)

## Flask routes
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', song=song)


## Player block
player = Player(song, socketio)

@socketio.on('play')
def handle_play():
    player.play()

@socketio.on('pause')
def handle_pause():
    player.pause()

@socketio.on('stop')
def handle_stop():
    player.stop()

@socketio.on('set_bpm')
def handle_set_bpm(bpm):
    player.set_bpm(bpm)

## Ableton Link callbacks
def start_stop_callback(playing):
    print(f'ableton -> playing: {playing}')
    if playing:
        player.play(auto=False)
    else:
        player.stop()

def handle_tempo_change(tempo):
    print(f'ableton -> tempo: {tempo}')
    player.set_bpm(round(tempo))
    socketio.emit('bpm', player.bpm)


link_armed = False
async def aa_link():
    global link_armed
    if link_armed == True: return
    link_armed = True

    loop = asyncio.get_running_loop()

    link = Link(0, loop)
    link.start_stop_sync_enabled = True
    link.playing = False
    await asyncio.sleep(1)
    link.set_tempo_callback(handle_tempo_change)
    link.set_start_stop_callback(start_stop_callback)
    link.enabled = True

    while True:
        await link.sync(1)
        if player.is_playing:
            print(f'sync.. beat {link.beat} | phase {link.phase} | time {link.time} | quantum {link.quantum}')
            player.next_beat()

def run_aa_link():
    asyncio.run(aa_link())

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    # start the Ableton Link
    # asyncio.run(aa_link())
    t = Thread(target=run_aa_link)
    t.start()

## Main loop
if __name__ == '__main__':
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    socketio.run(app, host="0.0.0.0", debug=DEBUG, port=5000, allow_unsafe_werkzeug=True)