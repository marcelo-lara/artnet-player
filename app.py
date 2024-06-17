import os
from flask import Flask, render_template
from flask_socketio import SocketIO

# create the Flask app
app = Flask(__name__, template_folder='html')
socketio = SocketIO(app)


from lib.song import Song

# load the song from the JSON file
# a song is a list of beats
song = Song.from_json_file('songbook/obsession.json')

# print the duration of the song
print(song.song_duration)

## Flask routes
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', song=song)

## Main loop
if __name__ == '__main__':
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    socketio.run(app, host="0.0.0.0", debug=DEBUG, port=5000, allow_unsafe_werkzeug=True)