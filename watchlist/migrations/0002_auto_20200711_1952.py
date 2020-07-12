# Generated by Django 3.0.8 on 2020-07-11 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='watchlistitem',
            constraint=models.UniqueConstraint(fields=('movie', 'user'), name='watchlist_item'),
        ),
    ]