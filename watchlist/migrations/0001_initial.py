# Generated by Django 3.0.8 on 2020-07-11 19:34

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('cast', models.CharField(max_length=150)),
                ('genre', models.CharField(max_length=150)),
                ('api_id', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='WatchlistItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateField(default=datetime.date.today)),
                ('watched', models.BooleanField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='watchlist.Movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]