-- ALTER TABLE ArtistGenre DROP FOREIGN KEY ArtistGenre_ibfk_2;
-- ALTER TABLE Genre MODIFY COLUMN genre_id INT AUTO_INCREMENT;
-- ALTER TABLE ArtistGenre MODIFY COLUMN genre_id INT;
-- ALTER TABLE ArtistGenre ADD FOREIGN KEY (genre_id) REFERENCES Genre(genre_id) ON DELETE CASCADE;
-- ALTER TABLE Playlist 
-- ADD followers BIGINT,
--     description VARCHAR(255),
--     total_tracks BIGINT;
-- ALTER TABLE User
-- DROP COLUMN username, 
-- DROP COLUMN email,
-- DROP COLUMN password;