
from django.urls import path, reverse_lazy
from .views import Watchlist, watchlist_detail, CreateWatchlistItem, add_movie

app_name = "watchlist"
urlpatterns = [
    path("", Watchlist, name="watchlist"),
    path("<int:primary_key>/", watchlist_detail, name="watchlist_detail"),
    path("new/", CreateWatchlistItem.as_view(), name="create_watchlist_item"),
    path("add-movie/", add_movie, name="add_movie"),
]