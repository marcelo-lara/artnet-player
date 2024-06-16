from lib.song import Song

# load the song from the JSON file
# a song is a list of beats
song = Song.from_json_file('songbook/obsession.json')

# print the duration of the song
print(song.song_duration)