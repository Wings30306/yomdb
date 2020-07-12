from django.shortcuts import render
from django.views.generic import ListView
from django.conf import settings
import requests
import json
# from .models import Watchlist_Item

def loadApi():
    print(settings.API)
    response = json.loads(requests.get(settings.API).text)
    print(response)


def Watchlist(request):
    return render(request, "watchlist.html")



    