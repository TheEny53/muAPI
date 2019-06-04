from django.urls import path
from .views import *

# URL routing for music api
urlpatterns = [
    path('auth/register/', RegisterUsersView.as_view(), name="auth-register"),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('songs/', ListSongsView.as_view(), name="songs-all"),
    path('albums/', ListAlbumsView.as_view(), name="albums-all"),
    path('artists/', ListArtistsView.as_view(), name="artists-all"),
    path('genres/', ListGenresView.as_view(), name="genres-all"),
    path('songs/<int:pk>/', DetailSongView.as_view(), name="song-detail"),
    path('albums/<int:pk>/', DetailAlbumView.as_view(), name="album-detail"),
    path('artists/<int:pk>/', DetailArtistView.as_view(), name="artist-detail"),
    path('genres/<int:pk>/', DetailGenreView.as_view(), name="genre-detail"),
    path('playlists/', PlaylistView.as_view(), name="playlists-all"),
    path('playlists/<slug:name>/', DetailPlaylistView.as_view(), name="playlists-detail"),
    path("songs/<slug:name>/", ListSongsByArtist.as_view(), name="songs-artist")
]
