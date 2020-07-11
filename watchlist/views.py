from django.shortcuts import render
from django.views.generic import ListView
from .models import Watchlist_Item

# Create your views here.
class WatchList(ListView):
    template_name="watchlist.html"
    queryset = Watchlist_Item.objects.all()