# Generated by Django 5.2.2 on 2025-06-20 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_alter_movie_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='slug',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
