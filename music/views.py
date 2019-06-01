from django.shortcuts import render
from rest_framework.views import status
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from .serializers import SongSerializer, AlbumSerializer, GenreSerializer, ArtistSerializer, SingleSongSerializer, SingleAlbumSerializer


class ListSongsView(generics.ListAPIView):
    """
    GET songs/
    POST songs/
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def post(self, request, *args, **kwargs):
        if self.request.version == 'v1':
            a_song = Song.objects.create(
                artist=Artist.objects.get(pk=request.data["artist"]),
                name=request.data["name"],
                rating=request.data["rating"],
                release_date=request.data["release_date"],
                length=request.data["length"],
                wiki_link=request.data["wiki_link"],
                picture_link=request.data["picture_link"],
                genre=Genre.objects.get(pk=request.data["genre"]))
            a_song.album.add(Album.objects.get(pk=request.data["album"]))
            return Response(
                data=SingleSongSerializer(a_song).data,
                status=status.HTTP_201_CREATED
            )
        if self.request.version == 'v2':
             return Response(
                status=status.HTTP_501_NOT_IMPLEMENTED
            )


class ListAlbumsView(generics.ListAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def post(self, request, *args, **kwargs):
        if self.request.version == 'v1':
            a_album = Album.objects.create(
                name=request.data["name"],
                release_date=request.data["release_date"],
                artist=Artist.objects.get(pk=request.data["artist"]),
                length=request.data["length"],
                produced_at=request.data["produced_at"],
                producer=request.data["producer"],
                rating=request.data["rating"],
                label=request.data["label"],
                wiki_link=request.data["wiki_link"],
                picture_link=request.data["picture_link"]
            )
            return Response(
                data=SingleAlbumSerializer(a_album).data,
                status=status.HTTP_201_CREATED
            )
        if self.request.version == 'v2':
             return Response(
                status=status.HTTP_501_NOT_IMPLEMENTED
            )


class ListArtistsView(generics.ListAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def post(self, request, *args, **kwargs):
        a_artist = Artist.objects.create(
            name=request.data["name"],
            founding_year=request.data["founding_year"],
            founding_country=request.data["founding_country"],
            is_active=request.data["is_active"],
            rating=request.data["rating"],
            wiki_link=request.data["wiki_link"],
            picture_link=request.data["picture_link"]
        )
        return Response(
            data=ArtistSerializer(a_artist).data,
            status=status.HTTP_201_CREATED
        )


class ListGenresView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def post(self, request, *args, **kwargs):
        a_genre = Genre.objects.create(
            name=request.data["name"],
            country_of_origin=request.data["country_of_origin"],
            year_of_establishment=request.data["year_of_establishment"],
            wiki_link=request.data["wiki_link"]
        )
        return Response(
            data=GenreSerializer(a_genre).data,
            status=status.HTTP_201_CREATED
        )


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
