# Generated by Django 5.0.3 on 2024-06-24 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_movie_duration_minutes_movieshowtimes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='num_ratings',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='user_rating',
        ),
        migrations.DeleteModel(
            name='UserRating',
        ),
    ]
