from flask import Flask, render_template, request, url_for, flash, redirect
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

app = Flask(__name__)

app.config['SECRET_KEY'] = '2759a23989cc914302c8d0911736d9d32ee1d25d8bf508d4'

cid = 'b693038074e9496a843379e02bd8acc7'
secret = '8f4bdc9afb324191b9eaf1b1a31f4eea'

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            artist = request.form['artist']
            mood = request.form['mood']
            energy = request.form['energy']
            dance = request.form['dance']

        except:
            return redirect(url_for('index'))
        
        if artist == '':
            return redirect(url_for('index'))

        else:
            searchResults = sp.search(q="artist:" + artist, type="track")
            
            artist_id = []
            artist_id.append(searchResults['tracks']['items'][0]['artists'][0]['id'])

            songs = []
            song_ids = []
            for i, t in enumerate(searchResults['tracks']['items']):
                songs.append(t['name'])
                song_ids.append(t['id'])

            features = sp.audio_features(song_ids)
            average_valence = 0
            average_energy = 0
            average_danceability = 0
            
            for i, f in enumerate(features):
                average_valence += f['valence']
                average_energy += f['energy']
                average_danceability += f['danceability']

            average_valence /= len(features)
            average_energy /= len(features)
            average_danceability /= len(features)

            if mood == 'happy':
                mood = 1

            elif mood == 'sad':
                mood = 0

            elif mood == 'angry':
                mood = 0.5

            if energy == 'high':
                energy = 1
            
            elif energy == 'medium':
                energy = 0.5

            elif energy == 'low':
                energy = 0

            if dance == 'yes':
                dance = 1
            
            elif dance == 'no':
                dance = 0
               
            average_valence = (average_valence + mood) / 2
            average_energy = (average_energy + energy) / 2
            average_danceability = (average_danceability + dance) / 2

            track_ids = sp.recommendations(seed_artists=artist_id, target_valence=average_valence, target_energy=average_energy, target_danceability=average_danceability, limit=20)
            playlist = []

            for song in track_ids['tracks']:
                artist = song['artists'][0]['name']
                song = song['name']
                string = artist + ' -- ' + song
                playlist.append(string)

            query_string = '_'.join(playlist)

            return redirect(url_for('playlist', songs=query_string))

    return render_template('index.html')

@app.route('/playlist')
def playlist():
    return render_template('playlist.html', songs=request.args.get('songs'))

app.run(debug=True)