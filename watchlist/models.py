from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=50)
    cast = models.CharField(max_length=150)
    genre = models.CharField(max_length=150)
    api_id = models.CharField(max_length=10)

    def __str__(self):
        return self.title

class WatchlistItem(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateField(default = date.today)
    watched = models.BooleanField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ['movie','user'], name="watchlist_item"),
        ]

    def __str__(self):
        return self.movie.title + " on " + self.user.username + "'s Watchlist"