import select
import sys
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import mysql.connector
from tabulate import tabulate
user = input("Enter your MySQL username:")
password = input("Enter your MySQL password:")

mydb = mysql.connector.connect(
    host='localhost',
    user=user,
    password=password
)

cursor = mydb.cursor()

client_id = input("Enter your client id for Spotify API:")
client_secret = input("Enter your client secret for Spotify API:")
redirect_uri = input("Enter the redirect uri for Spotify API:")

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

scope = 'user-modify-playback-state user-read-playback-state'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))


insert_artist_query = "INSERT INTO Artist (artist_id, artist_name, followers, popularity) VALUES (%s, %s, %s, %s)"
insert_album_query = "INSERT INTO Album (album_id, album_name, artist_id, total_tracks, release_date, popularity) VALUES (%s, %s, %s, %s, %s, %s)"
insert_genre_query = "INSERT INTO Genre (genre_name) VALUES (%s)"
insert_artist_genre_query = "INSERT INTO ArtistGenre (artist_id, genre_id) VALUES (%s, %s)"
insert_track_query = "INSERT INTO Track (track_id, track_name, artist_id, album_id, duration, popularity) VALUES (%s, %s, %s, %s, %s, %s)"
insert_single_query = "INSERT INTO Track (track_id, track_name, artist_id, duration, popularity) VALUES (%s, %s, %s, %s, %s)"
insert_user_query = "INSERT INTO User (user_id) VALUES (%s)"

select_artist_query = "SELECT COUNT(*) FROM Artist WHERE artist_id = %s"
select_album_query = "SELECT COUNT(*) FROM Album WHERE album_id = %s"
select_track_query = "SELECT COUNT(*) FROM Track WHERE track_id = %s"

def execute_script(filename):
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')
    for command in sqlCommands:
        try:
            if command.strip() != '':
                cursor.execute(command)
        except IOError as msg:
            print("Command skipped: ", msg)

def create_database():
    cursor.execute("SHOW DATABASES LIKE 'spotidb'")
    database_exists = cursor.fetchone()
    mydb.commit()
    if not database_exists:
        cursor.execute("CREATE DATABASE spotidb")
        cursor.execute("USE spotidb")
        execute_script('sql/create_schema.sql')
    else:
        cursor.execute("USE spotidb")
def search_in_sp(name, type):
    return sp.search(q=name, type=type)[type+'s']['items'][0]
def artist_in_database(artist_name):
    artist_name = sp.search(q=artist_name, type='artist')['artists']['items'][0]['name']
    select_artist_query = "SELECT COUNT(*) FROM Artist WHERE artist_name = %s"
    cursor.execute(select_artist_query, (artist_name,))
    result = cursor.fetchone()
    if (result[0] == 0):
        return False
    return True

    
def album_in_database(album_name):
    album = sp.search(q=album_name, type='album')['albums']['items'][0]
    if not artist_in_database(album['artists'][0]['name']):
        return False
    else:
        select_album_query = "SELECT COUNT(*) FROM Album WHERE album_name = %s"
        cursor.execute(select_album_query, (album['name'],))
        result = cursor.fetchone()
        if result[0] == 0:
            return False
        return True
    
def albumid_in_database(album_id):
    album = sp.album(album_id)
    if not artist_in_database(album['artists'][0]['name']):
        return False
    else:
        select_album_query = "SELECT COUNT(*) FROM Album WHERE album_name = %s"
        cursor.execute(select_album_query, (album['name'],))
        result = cursor.fetchone()
        if result[0] == 0:
            return False
        return True  
def track_in_database(track_name):
    track = sp.search(q=track_name, type='track')['tracks']['items'][0]
    if not artist_in_database(track['artists'][0]['name']):
        return False
    else:
        if not album_in_database(track['album']['name']):
            return False
        else:
            select_track_query = "SELECT COUNT(*) FROM Track WHERE track_name = %s"
            cursor.execute(select_track_query, (track_name,))
            result = cursor.fetchone()
            if result[0] == 0:
                return False
            return True
def trackid_in_database(track_id):
    track = sp.track(track_id)
    if not artist_in_database(track['artists'][0]['name']):
        return False
    else:
        if not album_in_database(track['album']['name']):
            return False
        else:
            select_track_query = "SELECT COUNT(*) FROM Track WHERE track_name = %s"
            cursor.execute(select_track_query, (track['name'],))
            result = cursor.fetchone()
            if result[0] == 0:
                return False
            return True

def playlist_in_database(playlist_id):
    select_playlist_query = "SELECT COUNT(*) FROM Playlist WHERE playlist_id = %s"
    cursor.execute(select_playlist_query, (playlist_id,))
    result = cursor.fetchone()
    if result[0] == 0:
        return False
    return True
def playlist_track_in_database(playlist_track_id):
    select_playlist_track_query = "SELECT COUNT(*) FROM PlaylistTrack WHERE playlisttrack_id = %s"
    cursor.execute(select_playlist_track_query, (playlist_track_id,))
    result = cursor.fetchone()
    if result[0] == 0:
        return False
    return True
def user_in_database(user_id):
    select_user_query = "SELECT COUNT(*) FROM User WHERE user_id = %s"
    cursor.execute(select_user_query, (user_id,))
    result = cursor.fetchone()
    if result[0] == 0:
        return False
    return True
def insert_user(user_id):
    user_data = (user_id)  
    if not user_in_database(user_id):
        cursor.execute(insert_user_query, (user_data,))
        mydb.commit()
    while cursor.nextset():
        pass
  
def insert_artist(artist):
    artist_data = (str(artist['id']), artist['name'],int(artist['followers']['total']), int(artist['popularity']))  
    if not artist_in_database(artist['name']):
        cursor.execute(insert_artist_query, artist_data)
        mydb.commit()
    while cursor.nextset():
        pass

def insert_album(album_id):
    album = sp.album(album_id)
    artist_name = album['artists'][0]['name']
    if (artist_name == "Various Artists"):
        artist_name = "Placeholder"
        artist = sp.search(q=artist_name,type='artist')['artists']['items'][0]
        artist_id = artist['id']
    else:
        artist_id = album['artists'][0]['id']
    try:
        album_data = (album['id'], album['name'], artist_id, album['total_tracks'], album['release_date'], album['popularity'])
    except:
        album_data = (album['id'], album['name'], artist_id, album['total_tracks'], album['release_date'], 0)
    print(album_data)

    if not artist_in_database(artist_name):
        print("NO artist?")
        insert_artist(artist) 
    cursor.execute(insert_album_query, album_data)
    mydb.commit()
    while cursor.nextset():
        pass

def insert_track(track):
    track_data = (track['id'],
                track['name'],
                track['artists'][0]['id'],
                track['album']['id'],
                track['duration_ms'],
                track['popularity']
                )
    print(track_data)
    # print(track['album']['name'])
    if not artist_in_database(track['artists'][0]['name']):
        print("actually no artists")
        artist = sp.search(q=track['artists'][0]['name'], type='artist')['artists']['items'][0]
        insert_artist(artist)
    if not albumid_in_database(track['album']['id']):
        print("NO album?")
        # album = sp.search(q=track['album']['name'], type='album')['albums']['items'][0]
        insert_album(track['album']['id'])
    cursor.execute(select_track_query, (track_data[0],))#4pEJoIkBIhNRzkFXnZybc4
    result = cursor.fetchone()
    if result[0] == 0:
        cursor.execute(insert_track_query, track_data)
        mydb.commit()
    while cursor.nextset():
        pass
def insert_playlist(playlist):
    insert_playlist_query = "INSERT INTO Playlist (playlist_id, playlist_name, user_id, followers, total_tracks, description) VALUES (%s, %s, %s, %s, %s, %s)"
    if not user_in_database(playlist['owner']['id']):
        insert_user(playlist['owner']['id'])
    playlist_data = (playlist['id'], 
                     playlist['name'], 
                     playlist['owner']['id'], 
                     playlist['followers']['total'], 
                     playlist['tracks']['total'], 
                     playlist['description'])
    cursor.execute(insert_playlist_query, playlist_data)

def insert_playlist_tracks(playlist_id, playlist_tracks):
    insert_playlist_tracks_query = "INSERT INTO PlaylistTrack (playlisttrack_id, playlist_id, track_id, track_order) VALUES (%s, %s, %s, %s)"
    for order, track in enumerate(playlist_tracks, start = 1):
        track_data = (track['track']['id'],
                      playlist_id,
                      track['track']['id'],
                      order)
        print(track_data)
        if not trackid_in_database(track['track']['id']):
            print("YO")
            track = sp.track(track['track']['id'])
            insert_track(track)
            print("Yayy")
        if not playlist_track_in_database(track_data[0]):
            cursor.execute(insert_playlist_tracks_query, track_data)

def print_artist_songs(artist_name):
    if artist_in_database(artist_name):
        artist_id = sp.search(q=artist_name, type='artist')['artists']['items'][0]['id']
        select_track_query = """SELECT track_name,duration,Track.popularity,Album.album_name, Artist.artist_name
                                FROM Track 
                                JOIN Album on Track.album_id = Album.album_id 
                                JOIN Artist on Track.artist_id = Artist.artist_id
                                WHERE Track.artist_id = %s"""
        cursor.execute(select_track_query, (artist_id,))
        result = cursor.fetchall()

        headers = ['Track Name', 'Duration', 'Popularity', 'Album', 'Artist']
        rows = []
        for row in result:
            rows.append(list(row))

        print(tabulate(rows, headers, tablefmt='grid'))
    else:
        print("Artist not in database")

def print_album_songs(album_name):
    if album_in_database(album_name):
        album_id = sp.search(q=album_name, type='album')['albums']['items'][0]['id']
        select_track_query = """SELECT track_name,duration,Track.popularity,Album.album_name,Artist.artist_name 
                                FROM Track 
                                JOIN Album on Track.album_id = Album.album_id 
                                JOIN Artist on Track.artist_id = Artist.artist_id
                                WHERE Track.album_id = %s"""
        cursor.execute(select_track_query, (album_id,))
        result = cursor.fetchall()
        headers = ['Track Name', 'Duration', 'Popularity', 'Album', 'Artist']
        rows = []
        for row in result:
            rows.append(list(row))

        print(tabulate(rows, headers, tablefmt='grid'))
    else:
        print("Album not in database")
    
def print_playlist(playlist_id):
    if playlist_in_database(playlist_id):
        select_track_query = """SELECT Track.track_name, Track.duration, Track.popularity, Album.album_name, Artist.artist_name
                               FROM PlaylistTrack
                               JOIN Track ON PlaylistTrack.track_id = Track.track_id
                               JOIN Album ON Track.album_id = Album.album_id
                               JOIN Artist ON Track.artist_id = Artist.artist_id
                               WHERE PlaylistTrack.playlist_id = %s"""
        cursor.execute(select_track_query, (playlist_id,))
        result = cursor.fetchall()
        headers = ['Track Name', 'Duration', 'Popularity', 'Album', 'Artist']
        rows = []
        for row in result:
            rows.append(list(row))

        print(tabulate(rows, headers, tablefmt='grid'))
    else:
        print("Playlist not in database")
def get_top_100_artists():
    artists = ['Taylor Swift', 'Lil Uzi Vert', 'Morgan Wallen', 'Luke Combs', 'aespa', 'SZA', 'Peso Pluma', 'Olivia Rodrigo', 'Ed Sheeran', 'Miley Cyrus', 'Jelly Roll', 'Drake', 'The Weeknd', 'Post Malone', 'Stray Kids', 'Dua Lipa', 'Zach Bryan', 'Bad Bunny', 'Harry Styles', 'Gunna', 'Bailey Zimmerman', 'Metallica', 'Kendrick Lamar', 'Lana Del Rey', 'J. Cole', 'Chris Stapleton', 'Fleetwood Mac', 'Tyler, The Creator', 'Lil Durk', 'Jordan Davis', 'Metro Boomin', '21 Savage', 'Lainey Wilson', 'Phish', 'ATEEZ', 'Fuerza Regida', 'Kane Brown', 'Karol G', 'Bruno Mars', 'Grupo Frontera', 'Miguel', 'Grateful Dead', 'Old Dominion', 'Melanie Martinez', 'Toosii', 'Lil Baby', 'Nicki Minaj', 'Future', 'Tyler Hubbard', 'ENHYPEN', 'Selena Gomez', 'Kelly Clarkson', 'Rema', 'Lucinda Williams', 'Fall Out Boy', 'Creedence Clearwater Revival', 'Queen', 'Ice Spice', 'Cole Swindell', 'Coi Leray', 'Michael Jackson', 'Foo Fighters', 'Kesha', 'Lewis Capaldi', 'Kanye West', 'TWICE', 'Mac Miller', 'Fifty Fifty', 'Nirvana', 'Beyonce', 'Chris Brown', 'AC\\/DC', 'Jon Pardi', 'Madonna', 'Doja Cat', 'HARDY', 'Latto', 'Travis Scott', 'Justin Bieber', 'Lynyrd Skynyrd', 'Jung Kook', 'Imagine Dragons', 'Young Thug', 'OneRepublic', 'TOMORROW X TOGETHER', 'Lizzo', 'Eagles', 'Adele', 'Tyler Childers', 'SEVENTEEN', 'The Beatles', 'Rihanna', 'Journey', 'Junior H', 'Noah Kahan', 'Lauren Daigle', 'Ariana Grande', 'Luke Bryan', 'Pink Floyd', 'Katy Perry']
    return artists

def get_all_songs(artist_name):
    artist = sp.search(q=artist_name, type='artist')['artists']['items'][0]
    albums = sp.artist_albums(artist['id'], album_type='album')['items']
    singles = sp.artist_albums(artist['id'], album_type='single')['items']

    insert_artist(artist)
    all_tracks =[]
    songs_obtained = 0 
    for album in albums:
        album = sp.album(album['id'])
        album_tracks = sp.album_tracks(album['id'])['items']
        all_tracks.extend(album_tracks)
        songs_obtained += len(album_tracks)
        print(f"Songs obtained: {songs_obtained}", end='\r')
        insert_album(album)
        
    for single in singles:
        single_name = single['name']
        # print(single)
        single_track = sp.search(q=single_name, type='track')['tracks']['items'][0]
        single['popularity'] = single_track['popularity']
        insert_album(single)
        # print("Got {}".format(single['uri']))
        all_tracks.append(single_track)
        songs_obtained += 1
        print(f"Songs obtained: {songs_obtained}", end='\r')
        
    
    for i, track in enumerate(all_tracks):
        track = sp.track(track['id'])
        try:
            insert_track(track)
            print(f"Put {i} / {songs_obtained} songs in Datbase", end='\r')
        except:
            pass
    genres = artist['genres']
    for genre in genres:
        genre_data = (genre,)
        cursor.execute(insert_genre_query, genre_data)
        while cursor.nextset():
            pass
    
    for genre_name in genres:
        select_genre_query = "SELECT genre_id FROM Genre WHERE genre_name = %s"
        cursor.execute(select_genre_query, (genre_name,))
        genre_id = cursor.fetchone()[0]
        artist_genre_data = (artist['id'], genre_id)
        cursor.execute(insert_artist_genre_query, artist_genre_data)
        mydb.commit()
        while cursor.nextset():
            pass

    return all_tracks
def get_playlist(playlist_id):
    playlist = sp.playlist(playlist_id, additional_types=['track'])

    if not playlist_in_database(playlist_id):
        insert_playlist(playlist)
    insert_playlist_tracks(playlist_id, playlist['tracks']['items'])
    
def get_artist_songs_popularity(artist_name, reverse):
    # artist_name   = "Olivia Rodrigo"

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
    album = sp.search(q=album_name, type='album')['albums']['items'][0]
    artist_name = album['artists'][0]['name']
    if not artist_in_database(artist_name):
        artist = sp.search(q=artist_name, type='artist')['artists']['items'][0]
        insert_artist(artist)
        insert_album(album)
    # album = results['albums']['items'][0]
    album_id = album['id']
    tracks = sp.album_tracks(album_id)['items']
    for track in tracks:
        track = sp.track(track['id'])
        insert_track(track)
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


def main():
    create_database()
    # mydb.commit()
    get_playlist("3420QnjcjHhybjpMO5wglu")
    print_playlist("3420QnjcjHhybjpMO5wglu")
    # while True:
    #     print("SpotiDB - Music Database Management")
    #     print("1. Seach for an artist")
    #     print("2. Search for an album")
    #     print("3. Search for an playlist")
    #     choice = input("Enter your choice:")
    #     if choice == "1":
    #         artist_name = input("Enter artist name: ")
    #         if not artist_in_database(artist_name):
    #             print(f"Artist {artist_name} is not in our database, please wait while we collect the artist data:")
    #             get_all_songs(artist_name)
    #         print_artist_songs(artist_name)
    #     elif choice == "2":
    #         album_name = input("Enter album name:")
    #         if not album_in_database(album_name):
    #             print(f"Album {album_name} is not in our database, please wait while we collect the album data:")
    #             get_album_songs(album_name)
            
    #         print_album_songs(album_name)

    # tracks = get_artists_songs_between("Taylor Swift", '2022-01-01', '2022-12-31')
    # print(tracks)
    # tracks = get_genre_songs("Old")
    # play_songs(tracks)
    # track = get_longest_song("Olivia Rodrigo")
    # track = get_fastest_song("Taylor Swift")
    # print(track['name'])
    # tracks = get_all_songs("Taylor Swift")
    # get_acoustic("Olivia Rodrigo")
    # get_songs_by_written_by("Taylor Swift", "Ed Sheeran")

main()