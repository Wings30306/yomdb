from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView
from django.conf import settings
from django.contrib.auth.decorators import login_required
import requests
import json
from datetime import date
from .models import WatchlistItem, Movie

@login_required
def Watchlist(request):
    context = {
        "queryset": WatchlistItem.objects.filter(user=request.user)
    }
    template_name = "watchlist.html"
    return render(request, template_name, context)

@login_required
def watchlist_detail(request, primary_key):
    """Shows details for a specific service"""
    template_name = 'watchlist-detail.html'
    if request.method == "POST":
        obj = WatchlistItem.objects.get(pk=primary_key)
        obj.watched = not obj.watched
        obj.save()
        return redirect('watchlist:watchlist_detail', primary_key=primary_key)
    try:
        obj = WatchlistItem.objects.get(pk=primary_key)
        context = {
            "object": obj
        }
    except WatchlistItem.DoesNotExist:
        messages.error(request, 'No movie in watchlist with this id: ' +
                       primary_key + '</em>.')
        return redirect("watchlist:watchlist")
    return render(request, template_name=template_name, context=context)

class CreateWatchlistItem(CreateView):
    model = WatchlistItem
    fields = ["movie", "watched"]

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        date_added = date.today()
        obj.save()
        print(obj)
        return redirect("watchlist:watchlist_detail", primary_key= obj.pk)

@login_required
def add_movie(request):
    if request.method == "POST":
        try:
            Movie.objects.get(api_id=request.POST.get("id"))
        except Movie.DoesNotExist:
            Movie.objects.create(
                api_id=request.POST.get("id"),
                title=request.POST.get("title"),
                cast=request.POST.get("cast"),
                genre=request.POST.get("genre")
            )
        movie = Movie.objects.get(api_id=request.POST.get("id"))
        try:
            WatchlistItem.objects.get(movie=movie, user=request.user)
        except WatchlistItem.DoesNotExist:
            WatchlistItem.objects.create(
                user=request.user,
                movie=movie,
                date_added = date.today(),
            )
        return redirect('watchlist:watchlist')
    return render(request, "new-movie.html")