import select
import sys
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='kaustubhg73',
    password='kaustubhsql',
    database='spotidb'
)

cursor = mydb.cursor()

insert_artist_query = "INSERT INTO Artist (artist_id, artist_name, followers, popularity) VALUES (%s, %s, %s, %s)"
insert_album_query = "INSERT INTO Album (album_id, album_name, artist_id, total_tracks, release_date, popularity) VALUES (%s, %s, %s, %s, %s, %s)"
insert_genre_query = "INSERT INTO Genre (genre_name) VALUES (%s)"
insert_artist_genre_query = "INSERT INTO ArtistGenre (artist_id, genre_id) VALUES (%s, %s)"
insert_track_query = "INSERT INTO Track (track_id, track_name, artist_id, album_id, duration, popularity) VALUES (%s, %s, %s, %s, %s, %s)"
insert_single_query = "INSERT INTO Track (track_id, track_name, artist_id, duration, popularity) VALUES (%s, %s, %s, %s, %s)"

select_artist_query = "SELECT COUNT(*) FROM Artist WHERE artist_id = %s"
select_album_query = "SELECT COUNT(*) FROM Album WHERE album_id = %s"
select_track_query = "SELECT COUNT(*) FROM Track WHERE track_id = %s"

def get_top_100_artists():
    artists = ['Taylor Swift', 'Lil Uzi Vert', 'Morgan Wallen', 'Luke Combs', 'aespa', 'SZA', 'Peso Pluma', 'Olivia Rodrigo', 'Ed Sheeran', 'Miley Cyrus', 'Jelly Roll', 'Drake', 'The Weeknd', 'Post Malone', 'Stray Kids', 'Dua Lipa', 'Zach Bryan', 'Bad Bunny', 'Harry Styles', 'Gunna', 'Bailey Zimmerman', 'Metallica', 'Kendrick Lamar', 'Lana Del Rey', 'J. Cole', 'Chris Stapleton', 'Fleetwood Mac', 'Tyler, The Creator', 'Lil Durk', 'Jordan Davis', 'Metro Boomin', '21 Savage', 'Lainey Wilson', 'Phish', 'ATEEZ', 'Fuerza Regida', 'Kane Brown', 'Karol G', 'Bruno Mars', 'Grupo Frontera', 'Miguel', 'Grateful Dead', 'Old Dominion', 'Melanie Martinez', 'Toosii', 'Lil Baby', 'Nicki Minaj', 'Future', 'Tyler Hubbard', 'ENHYPEN', 'Selena Gomez', 'Kelly Clarkson', 'Rema', 'Lucinda Williams', 'Fall Out Boy', 'Creedence Clearwater Revival', 'Queen', 'Ice Spice', 'Cole Swindell', 'Coi Leray', 'Michael Jackson', 'Foo Fighters', 'Kesha', 'Lewis Capaldi', 'Kanye West', 'TWICE', 'Mac Miller', 'Fifty Fifty', 'Nirvana', 'Beyonce', 'Chris Brown', 'AC\\/DC', 'Jon Pardi', 'Madonna', 'Doja Cat', 'HARDY', 'Latto', 'Travis Scott', 'Justin Bieber', 'Lynyrd Skynyrd', 'Jung Kook', 'Imagine Dragons', 'Young Thug', 'OneRepublic', 'TOMORROW X TOGETHER', 'Lizzo', 'Eagles', 'Adele', 'Tyler Childers', 'SEVENTEEN', 'The Beatles', 'Rihanna', 'Journey', 'Junior H', 'Noah Kahan', 'Lauren Daigle', 'Ariana Grande', 'Luke Bryan', 'Pink Floyd', 'Katy Perry']
    return artists

def get_all_songs(artist_name):
    artist = sp.search(q=artist_name, type='artist')['artists']['items'][0]
    albums = sp.artist_albums(artist['id'], album_type='album')['items']
    artist_data = (str(artist['id']), artist['name'],int(artist['followers']['total']), int(artist['popularity']))  
    cursor.execute(select_artist_query, (artist_data[0],))
    result = cursor.fetchone()
    if result[0] == 0:
        cursor.execute(insert_artist_query, artist_data)
        mydb.commit()
    singles = sp.artist_albums(artist['id'], album_type='single')['items']
    all_tracks =[]
    for album in albums:
        album = sp.album(album['id'])
        album_data = (album['id'], album['name'], artist['id'], album['total_tracks'], album['release_date'], album['popularity'])
        cursor.execute(select_album_query, (album_data[0],))
        result = cursor.fetchone()
        if result[0] == 0:
            cursor.execute(insert_album_query, album_data)
            mydb.commit()
        album_tracks = sp.album_tracks(album['id'])['items']
        # print(album_tracks[0]['duration_ms'])
        all_tracks.extend(album_tracks)

    for single in singles:
        single_name = single['name']
        results = sp.search(q=single_name, type='track')
        single = results['tracks']['items'][0]
        album_data = (single['id'], single['name'], artist['id'], 1, single['album']['release_date'], single['popularity'])
        cursor.execute(select_album_query, (album_data[0],))
        result = cursor.fetchone()
        if result[0] == 0:
            cursor.execute(insert_album_query, album_data)
            mydb.commit()
        album_tracks = sp.album_tracks(album['id'])['items']

        # print("Got {}".format(single['uri']))
        all_tracks.append(single)
    
    for track in all_tracks:
        track = sp.track(track['id'])
        try:
            track_data = (track['id'],
                        track['name'],
                        artist['id'],
                        track['album']['id'],
                        track['duration_ms'],
                        track['popularity']
                        )
            cursor.execute(select_track_query, (track_data[0],))
            result = cursor.fetchone()
            if result[0] == 0:
                cursor.execute(insert_track_query, track_data)
                mydb.commit()
        except:
            track_data = (track['id'],
                        track['name'],
                        artist['id'],
                        track['duration_ms'],
                        track['popularity']
                        )
            cursor.execute(select_track_query, (track_data[0],))
            result = cursor.fetchone()
            if result[0] == 0:
                cursor.execute(insert_single_query, track_data)
                mydb.commit()

    genres = artist['genres']
    for genre in genres:
        genre_data = (genre,)
        cursor.execute(insert_genre_query, genre_data)
    
    for genre_name in genres:
        select_genre_query = "SELECT genre_id FROM Genre WHERE genre_name = %s"
        cursor.execute(select_genre_query, (genre_name,))
        genre_id = cursor.fetchone()[0]

        artist_genre_data = (artist['id'], genre_id)
        cursor.execute(insert_artist_genre_query, artist_genre_data)
        mydb.commit()

    return all_tracks
def get_artist_songs_popularity(artist_name, reverse):
    # artist_name = "Olivia Rodrigo"

    results = sp.search(q=artist_name, type='artist')
    artist = results['artists']['items'][0]

    albums = sp.artist_albums(artist['id'], album_type='album')['items']

    singles = sp.artist_albums(artist['id'], album_type='single')['items']
    all_tracks =[]
    for album in albums:
        album_tracks = sp.album_tracks(album['id'])['items']
        all_tracks.extend(album_tracks)

    tracks = []

    for single in singles:
        single_name = single['name']
        results = sp.search(q=single_name, type='track')
        single = results['tracks']['items'][0]
        tracks.append({"name":single['name'], "popularity":single['popularity'], "uri":single['uri']})
        print("Got {}".format(single['uri']))
    for track in all_tracks:
        track_data = sp.track(track['id'])
        # danceability = audio_features[0]['danceability']
        tracks.append({"name": track_data['name'], "popularity":track_data['popularity'], "uri":track_data['uri']})
        print("Got {}".format(track_data['uri']))

    sorted_tracks = sorted(tracks, key=lambda d: d['popularity'], reverse=reverse)
    [print("Song - {}, Popularity - {}".format(track['name'], track['popularity'])) for track in sorted_tracks]
    return sorted_tracks

def get_artist_newest_songs(artist_name, reverse):

    results = sp.search(q=artist_name, type='artist')
    artist = results['artists']['items'][0]

    albums = sp.artist_albums(artist['id'], album_type='album')['items']

    singles = sp.artist_albums(artist['id'], album_type='single')['items']
    all_tracks =[]
    for album in albums:
        album_tracks = sp.album_tracks(album['id'])['items']
        all_tracks.extend(album_tracks)

    tracks = []

    for single in singles:
        single_name = single['name']
        results = sp.search(q=single_name, type='track')
        single = results['tracks']['items'][0]
        tracks.append({"name":single['name'], "release_date":single['album']['release_date'], "uri":single['uri']})
        print("Got {}".format(single['uri']))
    for track in all_tracks:
        track_data = sp.track(track['id'])
        # danceability = audio_features[0]['danceability']
        tracks.append({"name": track_data['name'], "release_date":track_data['album']['release_date'], "uri":track_data['uri']})
        print("Got {}".format(track_data['uri']))

    sorted_tracks = sorted(tracks, key=lambda d: d['release_date'], reverse=reverse)
    [print("Song - {}, Release Date - {}".format(track['name'], track['release_date'])) for track in sorted_tracks]
    return sorted_tracks

def get_genre_songs(genre):
    results = sp.search(q=f'genre:"{genre}"', type='track', limit=50)
    tracks = results['tracks']['items']

    return tracks

def get_album_songs(album_name):
    results = sp.search(q=album_name, type='album')
    album = results['albums']['items'][0]
    album_id = album['id']
    tracks = sp.album_tracks(album_id)['items']
    return tracks

def get_artists_songs_between(artist_name, start_date, end_date):
    artist = sp.search(q=artist_name, type='artist')['artists']['items'][0]
    artist_id = artist['id']
    tracks = sp.artist_top_tracks(artist_id)['tracks']
    filtered_tracks = []
    for track in tracks:
        release_date = track['album']['release_date']
        if start_date <= release_date <= end_date:
            filtered_tracks.append(track)
    
    for track in filtered_tracks:
        track_name = track['name']
        release_date = track['album']['release_date']
        print(f"Track: {track_name}  |  Release Date: {release_date}")
   
    return filtered_tracks

def get_track(track_name):
    results = sp.search(q=track_name, type='track')

    tracks = results['tracks']['items']
    # print(tracks[0]['artists'][0]['name'])
    return [tracks[0]]

def get_longest_song(artist_name):
    artist = sp.search(q=artist_name, type='artist')['artists']['items'][0]
    albums = sp.artist_albums(artist['id'], album_type='album')['items']

    singles = sp.artist_albums(artist['id'], album_type='single')['items']
    all_tracks =[]
    for album in albums:
        album_tracks = sp.album_tracks(album['id'])['items']
        # print(album_tracks[0]['duration_ms'])
        all_tracks.extend(album_tracks)

    for single in singles:
        single_name = single['name']
        results = sp.search(q=single_name, type='track')
        single = results['tracks']['items'][0]
        # print("Got {}".format(single['uri']))
        all_tracks.append(single)
    return max(all_tracks, key=lambda x:x['duration_ms'])
    # return filtered_tracks

def get_loudest_song(artist_name):
    artist = sp.search(q=artist_name, type='artist')['artists']['items'][0]
    all_tracks = sp.artist_top_tracks(artist['id'])['tracks']
    tracks = []
    for track in all_tracks:
        audio_analysis = sp.audio_analysis(track['id'])
        print("Got {}".format(track['name']))
        tracks.append({"name":track['name'],"loudness":audio_analysis['track']['loudness'], "id":track['id']})
    return max(tracks, key=lambda x : x['loudness'])

def get_fastest_song(artist_name):
    artist = sp.search(q=artist_name, type='artist')['artists']['items'][0]
    all_tracks = sp.artist_top_tracks(artist['id'])['tracks']
    tracks = []
    for track in all_tracks:
        audio_analysis = sp.audio_analysis(track['id'])
        print("Got {}".format(track['name']))
        tracks.append({"name":track['name'],"tempo":audio_analysis['track']['tempo'], "id":track['id']})
    return max(tracks, key=lambda x : x['tempo'])

def get_remixes(artist_name):
    artist = sp.search(q=artist_name, type='artist')['artists']['items'][0]
    albums = sp.artist_albums(artist['id'], album_type='album')['items']

    singles = sp.artist_albums(artist['id'], album_type='single')['items']
    all_tracks =[]
    for album in albums:
        album_tracks = sp.album_tracks(album['id'])['items']
        # print(album_tracks[0]['duration_ms'])
        all_tracks.extend(album_tracks)

    for single in singles:
        single_name = single['name']
        results = sp.search(q=single_name, type='track')
        single = results['tracks']['items'][0]
        # print("Got {}".format(single['uri']))
        all_tracks.append(single)    
    remixes = [track for track in all_tracks if 'remix' in track['name'].lower() or 'version' in track['name'].lower()]
    return remixes

def get_acoustic(artist_name):
    artist = sp.search(q=artist_name, type='artist')['artists']['items'][0]
    albums = sp.artist_albums(artist['id'], album_type='album')['items']

    singles = sp.artist_albums(artist['id'], album_type='single')['items']
    all_tracks =[]
    for album in albums:
        album_tracks = sp.album_tracks(album['id'])['items']
        # print(album_tracks[0]['duration_ms'])
        all_tracks.extend(album_tracks)

    for single in singles:
        single_name = single['name']
        results = sp.search(q=single_name, type='track')
        single = results['tracks']['items'][0]
        # print("Got {}".format(single['uri']))
        all_tracks.append(single)     
    acoustic_tracks = []
    for track in all_tracks:
        audio_features = sp.audio_features([track['id']])[0]
        if (audio_features['acousticness'] > 0.5):
            print("Got {} with {} acousticness".format(track['name'], audio_features['acousticness']))
            acoustic_tracks.append(track)

def get_collaborative_songs(artist_name):
    tracks = get_all_songs(artist_name)
    collaboration_tracks = [track for track in tracks if len(track['artists']) > 1]
    return collaboration_tracks

def get_songs_by_written_by(artist_name, songwriter_name):
    tracks = get_all_songs(artist_name)

    filtered_tracks = [track for track in tracks if songwriter_name in [artist['name'] for artist in track['artists']]]
    return filtered_tracks

def play_songs(tracks):
    for track in tracks:
        sp.start_playback(uris=[track['uri']])
        is_playing = True
        print("Playing {} by {}".format(track['name'], track['artists'][0]['name']))
        sys.stdout.write("Press 's' to skip the current track or any other key to continue: ")
        sys.stdout.flush()
        while is_playing:
            time.sleep(0.5)
            current_playback = sp.current_playback()
            if current_playback is not None:
                is_playing = current_playback['is_playing']
            else:
                break
            i, o, e = select.select([sys.stdin], [], [], 0.5)
            if i:
                user_input = sys.stdin.readline().strip()
                if user_input.lower() == 's':
                    sp.next_track()
            else:
                pass


client_id = '0bd7c49c29454e0dab9e54d7b2d46ba0'
client_secret = '9e40f7a7f1044e9a9fa873f60cb2ec67'
redirect_uri = 'http://localhost:8000/callback'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

scope = 'user-modify-playback-state user-read-playback-state'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

# tracks = get_artists_songs_between("Taylor Swift", '2022-01-01', '2022-12-31')
# print(tracks)
# tracks = get_genre_songs("Old")
# play_songs(tracks)
# track = get_longest_song("Olivia Rodrigo")
# track = get_fastest_song("Taylor Swift")
# print(track['name'])
tracks = get_all_songs("Taylor Swift")
# get_acoustic("Olivia Rodrigo")
# get_songs_by_written_by("Taylor Swift", "Ed Sheeran")
