# Generated by Django 4.2.16 on 2024-12-08 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("streaming", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="playlist",
            old_name="name",
            new_name="title",
        ),
        migrations.RemoveField(
            model_name="playlist",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="playlist",
            name="movies",
        ),
        migrations.AddField(
            model_name="playlist",
            name="movie_id",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="playlist",
            name="overview",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="playlist",
            name="poster_path",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="playlist",
            name="release_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="playlist",
            name="vote_average",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
