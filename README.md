# SpotiDB
SpotiDB is a music database project inspired by Spotify, aiming to provide an enhanced music browsing and management experience. It goes beyond the basic song, album, and duration information by including artist details, album metadata, song attributes, user ratings, and playlists.

I would like to turn this into a Web App, instead of a Python program in the future, but this is Under Construction :).

# Instructions to Use

If you plan to use it, you will need the following things - 
* An active Spotify Premium Subscription to access the Spotify API
* spotipy module. You can install it by `pip install spotipy`
* mysql-connector module. You can install it by `pip install mysql-connector-python`
* Open the folder python_implementation, and run the main.py file.
* Enter your MySQL database details, and your client_id, client_secret and redirect_url for your Spotify API.

# Roadmap

## Scope of the Database

### Features
    
#### For Song
    a. Title
    b. Album
    c. Duration
    d. Artist
    e. User Ratings
    f. Play Count
    g. Song Release Date
    h. Record Label
    i. Songwriter Credits
    j. Production Credits
    k. Genres
    l. Lyrics
    m. Featured Artists
    n. Song Tags
    o. Song Recommendations

#### For Album
    a. Name
    b. Release Date
    c. Record Label
    d. Album Artwork
    e. Tracklist
    f. Album Reviews
    g. Top Tracks
    h. Collaborating Artists
    i. Album Sales
    j. Album Recommendations

#### For Artist
    a. Name
    b. Biography
    c. Genres
    d. Albums
    e. Songs
    f. Collabs
    g. Social Media
    h. Website
    i. Image
    j. Popular Songs
    k. Discography

###  User Interface

1. Python Implementation with spotipy
2. Connection with MySQL Database

## Database Schema

### Track
* TrackID (PK)
* Track Name
* Duration
* Popularity
* ArtistID (Foreign Key)
* AlbumID (Foreign Key)
### Album
* AlbumID (PK)
* Name
* Release Date
* Total Tracks
* Popularity
* ArtistID (Foreign Key)
### Artist
* ArtistID
* Name
* Followers
* Genres
* Popularity
### Genre
* GenreID
* Name
### ArtistGenre
* ArtistID FK
* GenreID FK
### Playlist
* PlaylistID
* Name
* UserID (Foreign Key)
#### PlaylistTrack
* PlaylistTrackID
* PlaylistID (Foreign Key)
* TrackID (Foreign Key)
### Users
* UserID
* Username
* Email
* Password
