from rest_framework import serializers
from .models import Song, Album, Artist, Genre, Playlist




class ArtistSerializer(serializers.ModelSerializer):
    """Serializes the Artist Data"""
    class Meta:
        model = Artist
        fields = ("pk", "name", "founding_year", "founding_country", "is_active", "rating",
                  "wiki_link", "picture_link")

class AlbumSerializer(serializers.ModelSerializer):
    """Serializes the Album Data with the corresponding Artist"""
    artist = ArtistSerializer()

    class Meta:
        model = Album
        fields = ("pk", "name",  "label", "release_date", "length",
                  "produced_at", "producer", "rating", "wiki_link", "picture_link", "artist")

class GenreSerializer(serializers.ModelSerializer):
    """Serializes the Genre Data"""
    class Meta:
        model = Genre
        fields = ("pk", "name", "country_of_origin", "year_of_establishment",
                  "wiki_link")

class SongSerializer(serializers.ModelSerializer):
    """Serializes the Song Data with the corresponding Artist and Album(s)"""
    artist = ArtistSerializer()
    album = AlbumSerializer(many=True)

    class Meta:
        model = Song
        fields = ("pk", "name", "release_date",
                  "length", "rating", "wiki_link", "picture_link", "genre", "artist", "album")

class SingleSongSerializer(serializers.ModelSerializer):
    """Serializes the Song Data without additional data"""
    class Meta:
        model = Song
        fields = ("pk", "name", "release_date",
                  "length", "rating", "wiki_link", "picture_link", "genre", "artist", "album")

class SingleAlbumSerializer(serializers.ModelSerializer):
    """Serializes the Album Data without additional data"""
    class Meta:
        model = Album
        fields = ("pk", "name",  "label", "release_date", "length",
                  "produced_at", "producer", "rating", "wiki_link", "picture_link", "artist")

class PlaylistSerializer(serializers.ModelSerializer):
    """Serializes the playlist data"""
    songs = SingleSongSerializer(many=True)
    class Meta:
        model = Playlist
        fields = ("listen_count", "description", "name", "rating", "songs")

class TokenSerializer(serializers.Serializer):
    """This serializer serializes the token data"""
    token = serializers.CharField(max_length=255)
