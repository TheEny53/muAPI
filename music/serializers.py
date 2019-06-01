from rest_framework import serializers
from .models import Song, Album, Artist, Genre




class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ("pk", "name", "founding_year", "founding_country", "is_active", "rating",
                  "wiki_link", "picture_link")

class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()

    class Meta:
        model = Album
        fields = ("pk", "name",  "label", "release_date", "length",
                  "produced_at", "producer", "rating", "wiki_link", "picture_link", "artist")

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("pk", "name", "country_of_origin", "year_of_establishment",
                  "wiki_link")

class SongSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()
    album = AlbumSerializer(many=True)

    class Meta:
        model = Song
        fields = ("pk", "name", "release_date",
                  "length", "rating", "wiki_link", "picture_link", "genre", "artist", "album")

class SingleSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ("pk", "name", "release_date",
                  "length", "rating", "wiki_link", "picture_link", "genre", "artist", "album")

class SingleAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ("pk", "name",  "label", "release_date", "length",
                  "produced_at", "producer", "rating", "wiki_link", "picture_link", "artist")
