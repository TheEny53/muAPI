from rest_framework import serializers
from .models import Song, Album, Artist, Genre


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ("name", "artist", "album",  "release_date", "length", "rating", "wiki_link", "picture_link", "genre")


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ("name", "artist", "label", "release_date", "length",
                  "produced_at", "producer", "rating", "wiki_link", "picture_link")


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ("name", "founding_date", "founding_country", "is_active", "rating",
                  "wiki_link", "picture_link")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "country_of_origin", "year_of_establishment", "influencing_genres",
        "wiki_link")
