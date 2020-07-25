from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Movie, WatchlistItem

# Create your tests here.
class ModelTests(TestCase):
    def test_movie_string_representation(self):
        """ Test admin side string representation of Movie instance """
        movie = Movie(title="The Best Movie Ever")
        self.assertEqual(str(movie), movie.title)

    def test_watchlist_item_string_representation(self):
        """ Test admin side string representation of WatchlistItem instance """
        Movie.objects.create(
            title="The Best Movie Ever",
            genre="Comedy",
            cast="A bunch of brilliant actors")
        User.objects.create(username="TestUser")
        item = WatchlistItem(movie=Movie.objects.get(pk=1), user=User.objects.get(pk=1))
        self.assertEqual(str(item), item.movie.title + " on " + item.user.username + "'s Watchlist")

class UrlTests(TestCase):
    def test_watchlist(self):
        """ Test that non-logged-in user is redirected to login when accessing watchlist """
        response = self.client.get('/watchlist/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/login/?next=/watchlist/")

    def test_watchlist_detail(self):
        """ test that watchlist item is rendered """
        response = self.client.get('/watchlist/1')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, "/watchlist/1/")
