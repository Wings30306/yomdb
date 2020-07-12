
from django.urls import path, reverse_lazy
from .views import Watchlist

app_name = "watchlist"
urlpatterns = [
    path("", Watchlist, name="watchlist")
]