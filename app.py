import asyncio
from operator import is_
import os
from flask import Flask, render_template
from flask_socketio import SocketIO
from aalink import Link
from threading import Thread
from lib.chaser.chaser import Chaser
from lib.fixtures import channel, setup_artnet_fixtures, create_fixture, Channel, ArtNetNodeInstance
from lib.fixtures.artNetNodeInstance import dispatch_artnet_packet
import yaml

# create the Flask app
app = Flask(__name__, template_folder='html')
socketio = SocketIO(app)

#### Artnet Block ####################################################################
## Load Fixtures
with open('fixtures.yaml', 'r') as file:
    fixtures_data = yaml.safe_load(file)
fixtures = [create_fixture(data) for data in fixtures_data]

## setup artnet fixtures on startup
artnet_channels = []
with app.app_context():
    asyncio.run(setup_artnet_fixtures(fixtures, artnet_channels))

def get_channel_by_id(channel_id)->Channel:
    return next(c for c in artnet_channels if c['name'] == channel_id)['instance']

def dump_channels():
    return [channel['instance'].get_value_as_dict() for channel in artnet_channels]

@socketio.on('slider_change')
def handle_slider_change(data):

    # Get the channel id and value
    channel_id = data['channel_id']
    channel_value = data['value']

    # Get the channel instance
    channel = get_channel_by_id(channel_id)
    channel.next_value = channel_value

    # Dispatch the ArtNet packet
    asyncio.run(dispatch_artnet_packet(channel))

## load the cue sheet from the yaml file
song_title = "berlin_metro"
cues_file = f'songbook/{song_title}.cues.json'
chords_file =f'songbook/{song_title}.chords.json'
chaser = Chaser(song_title)

@socketio.on('save_beat')
def handle_save_beat(beat=None):
    print(beat)
    if beat is None: return
    # save beat to cue sheet
    chaser.store_beat(int(beat), dump_channels())

@socketio.on('save_note')
def handle_save_beat(note=None):
    print(note)
    if note is None: return
    # save note to cue sheet
    chaser.store_note(note, dump_channels())

def trigger_scene(scene):
    # get the channels for the scene
    print("next scene", scene)

####################################################################

from lib.player import Player
from lib.song import Song

# load the song from the JSON file
# a song is a collection of beats and chords in groups of 4 beats
song = Song.from_json_file(song_title)

## Flask routes
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', song=song, fixtures=fixtures, song_name=song_title, sheet=song.get_music_sheet())


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

## Ableton Link callbacks ##############################################################################
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

## Main loop ##############################################################################
if __name__ == '__main__':
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    socketio.run(app, host="0.0.0.0", debug=DEBUG, port=5000, allow_unsafe_werkzeug=True)