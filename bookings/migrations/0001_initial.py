# Generated by Django 5.2.2 on 2025-06-24 19:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('language', models.CharField(max_length=50)),
                ('genre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Theater',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Showtime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('showtime', models.TimeField()),
                ('date', models.DateField()),
                ('format_tag', models.CharField(blank=True, max_length=20)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.movie')),
                ('theater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.theater')),
            ],
        ),
    ]
