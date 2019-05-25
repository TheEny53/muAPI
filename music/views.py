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


class DetailSongView(generics.RetrieveUpdateDestroyAPIView):
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


class DetailAlbumView(generics.RetrieveUpdateDestroyAPIView):
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
                    "message": "Song with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class DetailArtistView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET artists/:id/
    """


class DetailGenreView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET genres/:id/
    """