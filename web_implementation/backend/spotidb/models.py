from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True, default='')
    created_on = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
    def save(self, *args, **kwargs):
        # Check if the user is being created for the first time
        if not self.pk:
            pass
        super().save(*args, **kwargs)


class Song(models.Model):
    title = models.CharField(max_length=255)
    duration = models.DurationField()
    release_date = models.DateField()
    play_count = models.IntegerField(default=0)
    genres = models.CharField(max_length=255)
    lyrics = models.TextField()
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)
    album = models.ForeignKey('Album', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Songs"

    def __str__(self):
        return self.title



class Album(models.Model):
    name = models.CharField(max_length=255)
    release_date = models.DateField()
    record_label = models.CharField(max_length=255)
    artists = models.ManyToManyField('Artist')
    songs = models.ManyToManyField('Song', through='Tracklist', related_name='albums')

    def __str__(self):
        return self.name
class Artist(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField()
    genres = models.CharField(max_length=255)
    songs = models.ManyToManyField('Song', through='ArtistSongs', related_name='artists')
    albums = models.ManyToManyField('Album')

    def __str__(self):
        return self.name
    
class Playlist(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField('Song', through='PlaylistSongs', related_name='playlists')

    def __str__(self):
        return self.name
    
class PlaylistSongs(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.playlist)

class ArtistSongs(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.artist)

class Tracklist(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    track_number = models.PositiveIntegerField()

    def __str__(self):
        return str(self.album)