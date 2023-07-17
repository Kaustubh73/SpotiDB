# Generated by Django 4.2.3 on 2023-07-13 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("spotidb", "0002_remove_user_solved_count_remove_user_solved_puzzles"),
    ]

    operations = [
        migrations.CreateModel(
            name="Album",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("release_date", models.DateField()),
                ("record_label", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Artist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("biography", models.TextField()),
                ("genres", models.CharField(max_length=255)),
                ("albums", models.ManyToManyField(to="spotidb.album")),
            ],
        ),
        migrations.CreateModel(
            name="Playlist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Song",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("duration", models.DurationField()),
                ("release_date", models.DateField()),
                ("play_count", models.IntegerField(default=0)),
                ("genres", models.CharField(max_length=255)),
                ("lyrics", models.TextField()),
                (
                    "album",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="spotidb.album"
                    ),
                ),
                (
                    "artist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="spotidb.artist"
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Songs",
            },
        ),
        migrations.AddField(
            model_name="user",
            name="created_on",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="user",
            name="username",
            field=models.CharField(default="", max_length=255, unique=True),
        ),
        migrations.CreateModel(
            name="Tracklist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("track_number", models.PositiveIntegerField()),
                (
                    "album",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="spotidb.album"
                    ),
                ),
                (
                    "song",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="spotidb.song"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PlaylistSongs",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "playlist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="spotidb.playlist",
                    ),
                ),
                (
                    "song",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="spotidb.song"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="playlist",
            name="songs",
            field=models.ManyToManyField(
                related_name="playlists",
                through="spotidb.PlaylistSongs",
                to="spotidb.song",
            ),
        ),
        migrations.AddField(
            model_name="playlist",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.CreateModel(
            name="ArtistSongs",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "artist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="spotidb.artist"
                    ),
                ),
                (
                    "song",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="spotidb.song"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="artist",
            name="songs",
            field=models.ManyToManyField(
                related_name="artists", through="spotidb.ArtistSongs", to="spotidb.song"
            ),
        ),
        migrations.AddField(
            model_name="album",
            name="artists",
            field=models.ManyToManyField(to="spotidb.artist"),
        ),
        migrations.AddField(
            model_name="album",
            name="songs",
            field=models.ManyToManyField(
                related_name="albums", through="spotidb.Tracklist", to="spotidb.song"
            ),
        ),
    ]