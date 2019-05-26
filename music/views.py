from django.shortcuts import render
from rest_framework.views import status
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import *


class ListSongsView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class ListAlbumsView(generics.ListAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer


class ListArtistsView(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class ListGenresView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class DetailSongView(generics.RetrieveAPIView):
    """
    GET songs/:id/
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_song = self.queryset.get(pk=kwargs["pk"])
            return Response(SongSerializer(a_song).data)
        except Song.DoesNotExist:
            return Response(
                data={
                    "message": "Song with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class DetailAlbumView(generics.RetrieveAPIView):
    """
    GET albums/:id/
    """

    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_album = self.queryset.get(pk=kwargs["pk"])
            return Response(AlbumSerializer(a_album).data)
        except Album.DoesNotExist:
            return Response(
                data={
                    "message": "Album with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class DetailArtistView(generics.RetrieveAPIView):
    # View is non-editable
    """
    GET artists/:id/
    """
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_artist = self.queryset.get(pk=kwargs["pk"])
            return Response(ArtistSerializer(a_artist).data)
        except Artist.DoesNotExist:
            return Response(
                data={
                    "message": "Artist with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class DetailGenreView(generics.RetrieveAPIView):
    """
    GET genres/:id/
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get(self, request, *args, **kwargs):
        try:
            a_genre = self.queryset.get(pk=kwargs["pk"])
            return Response(GenreSerializer(a_genre).data)
        except Genre.DoesNotExist:
             return Response(
                data={
                    "message": "Genre with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )