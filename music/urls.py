from django.urls import path
from .views import *


urlpatterns = [
    path('songs/', ListSongsView.as_view(), name="songs-all"),
    path('albums/', ListAlbumsView.as_view(), name="albums-all"),
    path('artists/', ListArtistsView.as_view(), name="artists-all"),
    path('genres/', ListGenresView.as_view(), name="genres-all")
]