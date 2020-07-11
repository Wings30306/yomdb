
from django.urls import path, reverse_lazy
from .views import WatchList

app_name = "watchlist"
urlpatterns = [
    path("", watchlist_view, name="watchlist")
]