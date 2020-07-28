from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView
from django.conf import settings
from django.contrib.auth.decorators import login_required
import requests
import json
import logging
from datetime import date
from .models import WatchlistItem, Movie

logger = logging.getLogger(__name__)


def helper(movies, user):
    """Create lists of all titles, genres and actors in database
    This will be used for populating dropdowns and search functionality"""
    list_by_type = {}
    titles = []
    genres = []
    actors = []
    for movie in movies:
        movie_genres = movie.genre.split(", ")
        movie_actors = movie.cast.split(", ")
        title = movie.title
        if title not in titles:
            titles.append(title)
        for genre in movie_genres:
            if genre not in genres:
                genres.append(genre)
        for actor in movie_actors:
            if actor not in actors:
                actors.append(actor)              
    genres_alphabetical = sorted(genres)
    actors_alphabetical = sorted(actors, key=lambda x: x.split(" ")[-1])
    list_by_type.update({"titles": titles,
                         "actors": actors_alphabetical,
                         "genres": genres_alphabetical})
    logger.info("List by type generated for user " + user.username + ":\n" + str(list_by_type))
    return list_by_type


@login_required
def Watchlist(request):
    """Show all watchlist items saved by user"""
    movies_in_watchlist = []
    user_watchlist = WatchlistItem.objects.select_related('movie').filter(user=request.user)
    for item in user_watchlist:
        movies_in_watchlist.append(item.movie)
    list_by_type = helper(movies_in_watchlist, request.user)
    movies = [
        {
            "pk": entry.id,
            "title": entry.movie.title,
            "cast": entry.movie.cast,
            "genre": entry.movie.genre,
            "watched": entry.watched} for entry in WatchlistItem.objects.filter(
            user=request.user)]
    context = {
        "queryset": movies,
        "titles": list_by_type["titles"],
        "genres": list_by_type["genres"],
        "actors": list_by_type["actors"]
    }
    template_name = "watchlist.html"
    logger.info(request.user.username + " accessed their Watchlist page")
    return render(request, template_name, context)


@login_required
def watchlist_detail(request, primary_key):
    """Shows details for a specific watchlist item"""
    template_name = 'watchlist-detail.html'
    if request.method == "POST":
        obj = WatchlistItem.objects.get(pk=primary_key)
        obj.watched = not obj.watched
        obj.save()
        logger.info("Watchlist item status is updated")
        return redirect('watchlist:watchlist_detail', primary_key=primary_key)
    try:
        obj = WatchlistItem.objects.get(pk=primary_key)
        logger.info("Rendering watchlist detail page for " + obj.movie.title)
        context = {
            "object": obj
        }
    except WatchlistItem.DoesNotExist:
        logger.warning('No movie in watchlist with this id: ' +
                       str(primary_key) + '.')
        return redirect("watchlist:watchlist")
    return render(request, template_name=template_name, context=context)


class CreateWatchlistItem(CreateView):
    """Create watchlist item with movie already saved in database"""
    model = WatchlistItem
    fields = ["movie", "watched"]

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        date_added = date.today()
        obj.save()
        print(obj)
        return redirect("watchlist:watchlist_detail", primary_key=obj.pk)


@login_required
def delete_watchlist_item(request, primary_key):
    item = WatchlistItem.objects.get(pk=primary_key)
    item.delete()
    return redirect("watchlist:watchlist")


@login_required
def add_movie(request):
    """Add movie and save it as to the user's watchlist"""
    if request.method == "POST":
        try:
            Movie.objects.get(api_id=request.POST.get("id"))
            logger.warning("Movie already in database")
        except Movie.DoesNotExist:
            logger.info("Adding movie to database")
            Movie.objects.create(
                api_id=request.POST.get("id"),
                title=request.POST.get("title"),
                cast=request.POST.get("cast"),
                genre=request.POST.get("genre")
            )
        movie = Movie.objects.get(api_id=request.POST.get("id"))
        try:
            WatchlistItem.objects.get(movie=movie, user=request.user)
            logger.warning("Watchlist item for this movie and user already exists")
        except WatchlistItem.DoesNotExist:
            logger.info("Creating new Watchlist item")
            WatchlistItem.objects.create(
                user=request.user,
                movie=movie,
                date_added=date.today(),
            )
        return redirect('watchlist:watchlist')
    return render(request, "new-movie.html")
