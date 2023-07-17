CREATE TABLE Artist (
    artist_id VARCHAR(255) PRIMARY KEY,
    artist_name VARCHAR(255),
    followers INT,
    popularity INT,
    other_artist_details VARCHAR(255)
);

CREATE TABLE Genre (
    genre_id INT PRIMARY KEY AUTO_INCREMENT,
    genre_name VARCHAR(255)
);

CREATE TABLE ArtistGenre (
    artist_id VARCHAR(255),
    genre_id INT,
    PRIMARY KEY (artist_id, genre_id),
    FOREIGN KEY (artist_id) REFERENCES Artist(artist_id),
    FOREIGN KEY (genre_id) REFERENCES Genre(genre_id)
);

CREATE TABLE Album (
    album_id VARCHAR(255) PRIMARY KEY,
    album_name VARCHAR(255),
    artist_id VARCHAR(255),
    total_tracks INT,
    release_date DATE,
    popularity INT,
    other_album_details VARCHAR(255),
    FOREIGN KEY (artist_id) REFERENCES Artist(artist_id)
);

CREATE TABLE Track (
    track_id VARCHAR(255) PRIMARY KEY,
    track_name VARCHAR(255),
    artist_id VARCHAR(255),
    album_id VARCHAR(255) DEFAULT NULL,
    duration INT,
    popularity INT,
    other_track_details VARCHAR(255),
    FOREIGN KEY (artist_id) REFERENCES Artist(artist_id),
    FOREIGN KEY (album_id) REFERENCES Album(album_id)
);

CREATE TABLE User (
    user_id VARCHAR(255) PRIMARY KEY,
    username VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    other_user_details VARCHAR(255)
);

CREATE TABLE Playlist (
    playlist_id VARCHAR(255) PRIMARY KEY,
    playlist_name VARCHAR(255),
    user_id VARCHAR(255),
    other_playlist_details VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE PlaylistTrack (
  playlisttrack_id VARCHAR(255) PRIMARY KEY,
  playlist_id VARCHAR(255),
  track_id VARCHAR(255),
  track_order INT,
  FOREIGN KEY (playlist_id) REFERENCES Playlist(playlist_id),
  FOREIGN KEY (track_id) REFERENCES Track(track_id)
);

