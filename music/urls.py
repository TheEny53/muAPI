from django.urls import path
from .views import *


urlpatterns = [
    path('songs/', ListSongsView.as_view(), name="songs-all"),
    path('albums/', ListAlbumsView.as_view(), name="albums-all"),
    path('artists/', ListArtistsView.as_view(), name="artists-all"),
    path('genres/', ListGenresView.as_view(), name="genres-all"),
    path('songs/<int:pk>/', DetailSongView.as_view(), name="song-detail"),
    path('albums/<int:pk>/', DetailAlbumView.as_view(), name="album-detail"),
    path('artists/<int:pk>/', DetailArtistView.as_view(), name="artist-detail"),
    path('genres/<int:pk>/', DetailGenreView.as_view(), name="genre-detail")
]