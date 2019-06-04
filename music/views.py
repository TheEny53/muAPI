from rest_framework.views import status
from rest_framework import generics
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions
from rest_framework.response import Response
from .models import Artist, Album, Genre, Song, Playlist
from .serializers import (TokenSerializer, SongSerializer, AlbumSerializer,
                          GenreSerializer, ArtistSerializer, PlaylistSerializer,
                          SingleSongSerializer, SingleAlbumSerializer)


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class RegisterUsersView(generics.CreateAPIView):
    """
    POST auth/register/
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        if request.data.get("username", "") and request.data.get("password", "") and request.data.get("email", ""):
            username = request.data.get("username", "")
            password = request.data.get("password", "")
            email = request.data.get("email", "")
        else:
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        User.objects.create_user(
            username=username, password=password, email=email
        )
        return Response(status=status.HTTP_201_CREATED)


class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            r = Response(serializer.data)
            return r
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ListSongsView(generics.ListAPIView):
    """
    GET songs/
    POST songs/
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

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
            for i in request.data["album"]:
                a_song.album.add(Album.objects.get(pk=i))
            return Response(
                data=SingleSongSerializer(a_song).data,
                status=status.HTTP_201_CREATED
            )
        if self.request.version == 'v2':
            return Response(
                status=status.HTTP_501_NOT_IMPLEMENTED
            )


class ListAlbumsView(generics.ListAPIView):
    """
    GET albums/
    POST albums/
    """
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

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
    """
    GET artists/
    POST artists/
    """
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        if self.request.version == 'v1':
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
        if self.request.version == 'v2':
            return Response(
                status=status.HTTP_501_NOT_IMPLEMENTED
            )


class ListGenresView(generics.ListAPIView):
    """
    GET genres/
    POST genres/
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        if self.request.version == 'v1':
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
        if self.request.version == 'v2':
            return Response(
                status=status.HTTP_501_NOT_IMPLEMENTED
            )


class DetailSongView(generics.RetrieveAPIView):
    """
    GET songs/:id/
    DELETE songs/:id/
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        if self.request.version == 'v1':
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
        if self.request.version == 'v2':
            return Response(
                status=status.HTTP_501_NOT_IMPLEMENTED
            )

    def delete(self, request, *args, **kwargs):
        if self.request.version == 'v1':
            try:
                a_song = self.queryset.get(pk=kwargs["pk"])
                a_song.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Song.DoesNotExist:
                return Response(
                    data={
                        "message": "Song with id: {} does not exist".format(kwargs["pk"])
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        if self.request.version == 'v2':
            return Response(
                status=status.HTTP_501_NOT_IMPLEMENTED
            )


class DetailAlbumView(generics.RetrieveAPIView):
    """
    GET albums/:id/
    DELETE albums/:id/
    """

    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        if self.request.version == 'v1':
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
        if self.request.version == 'v2':
            return Response(
                status=status.HTTP_501_NOT_IMPLEMENTED
            )

    def delete(self, request, *args, **kwargs):
        if self.request.version == 'v1':
            try:
                a_album = self.queryset.get(pk=kwargs["pk"])
                a_album.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Album.DoesNotExist:
                return Response(
                    data={
                        "message": "Album with id: {} does not exist".format(kwargs["pk"])
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        if self.request.version == 'v2':
            return Response(
                status=status.HTTP_501_NOT_IMPLEMENTED
            )


class DetailArtistView(generics.RetrieveAPIView):
    # View is non-editable
    """
    GET artists/:id/
    DELETE artists/:id/
    """
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        if self.request.version == 'v1':
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
        if self.request.version == 'v2':
            return Response(
                status=status.HTTP_501_NOT_IMPLEMENTED
            )

    def delete(self, request, *args, **kwargs):
        if self.request.version == 'v1':
            try:
                a_artist = self.queryset.get(pk=kwargs["pk"])
                a_artist.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Artist.DoesNotExist:
                return Response(
                    data={
                        "message": "Artist with id: {} does not exist".format(kwargs["pk"])
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        if self.request.version == 'v2':
            return Response(
                status=status.HTTP_501_NOT_IMPLEMENTED
            )


class DetailGenreView(generics.RetrieveAPIView):
    """
    GET genres/:id/
    DELETE genres/:id/
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        if self.request.version == 'v1':
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
        if self.request.version == 'v2':
            return Response(
                status=status.HTTP_501_NOT_IMPLEMENTED
            )

    def delete(self, request, *args, **kwargs):
        if self.request.version == 'v1':
            try:
                a_genre = self.queryset.get(pk=kwargs["pk"])
                a_genre.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Genre.DoesNotExist:
                return Response(
                    data={
                        "message": "Genre with id: {} does not exist".format(kwargs["pk"])
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        if self.request.version == 'v2':
            return Response(
                status=status.HTTP_501_NOT_IMPLEMENTED
            )


class PlaylistView(generics.ListAPIView):
    """
    GET playlists/
    POST playlists/
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = PlaylistSerializer
   
    def get_queryset(self):
        user = self.request.user
        return Playlist.objects.filter(user=user)


    def post(self, request, *args, **kwargs):
        if self.request.version == 'v1':
            try:
                a_playlist = Playlist.objects.create(
                    description = request.data["description"],
                    name = request.data["name"],
                    rating = request.data["rating"],
                    user = request.user
                )
                for i in request.data["songs"]:
                    a_playlist.songs.add(Song.objects.get(pk=i))
                return Response(
                    data = PlaylistSerializer(a_playlist).data,
                    status=status.HTTP_201_CREATED
                )
            except IntegrityError:
                return Response(
                    data={
                        "message":"""Error creating playlist, name {} already exists.""".format(request.data["name"])
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )
        if self.request.version == 'v2':
            return Response(
                status=status.HTTP_501_NOT_IMPLEMENTED
            )


class DetailPlaylistView(generics.ListAPIView):
    """
    UPDATE playlists/:name/
    DELETE playlists/:name/
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        user = self.request.user
        return Playlist.objects.filter(user=user)

    def get(self, request, *args, **kwargs):
        if self.request.version == 'v1':
            try:
                a_playlist = self.get_queryset().get(name=kwargs["name"])
                return Response(PlaylistSerializer(a_playlist).data)
            except Playlist.DoesNotExist:
                return Response(
                    data={
                        "message" : "Playlist with name {} does not exist".format(kwargs["name"])
                    },
                    status = status.HTTP_404_NOT_FOUND
                )
        
