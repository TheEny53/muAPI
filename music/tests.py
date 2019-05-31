from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Artist, Genre, Album, Song
from .serializers import ArtistSerializer, GenreSerializer, AlbumSerializer, SongSerializer

# tests for views


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_artist(name="", founding_year="", founding_country="", is_active="",
                      rating="", wiki_link="", picture_link=""):
        if (name != "" and founding_year != "" and founding_country != ""
                and rating != "" and is_active != "" and wiki_link != ""):
            return Artist.objects.create(name=name, founding_year=founding_year, 
                                         founding_country=founding_country, is_active=is_active,
                                         rating=rating, wiki_link=wiki_link, 
                                         picture_link=picture_link)

    @staticmethod
    def create_genre(name="", country_of_origin="", year_of_establishment="", wiki_link=""):
        if name != "" and country_of_origin != "" and wiki_link != "":
            return Genre.objects.create(name=name, country_of_origin=country_of_origin,
                                        year_of_establishment=year_of_establishment, 
                                        wiki_link=wiki_link)

    @staticmethod
    def create_album(name="", release_date="", artist="", length="", produced_at="", producer="",
                     rating="", label="", wiki_link="", picture_link=""):
        if name != "" and artist != "" and rating != "" and wiki_link != "":
            return Album.objects.create(name=name, release_date=release_date, artist=artist,
            length=length, produced_at=produced_at, producer=producer, rating=rating,
            label=label, wiki_link=wiki_link, picture_link=picture_link)

    @staticmethod
    def create_song(name="", release_date="",  artist="", length="",
                     rating="", wiki_link="", picture_link="", genre=""):
        if name != "" and artist != "" and rating != "" and wiki_link != "":
            return Song.objects.create(name=name, release_date=release_date,
                                       artist=artist, length=length,
                                       rating=rating, wiki_link=wiki_link,
                                       picture_link=picture_link, genre=genre)

    def setUp(self):
        # 1. Artists
        dummy_artist = self.create_artist("Sean Paul", "1987", "JA", "True", "3", 
                                          "wiki.com", "wiki.com")
        self.create_artist("Michael Jackson", "1976", "US", "False", "4", 
                           "wiki.com/us", "wiki.com/pic")

        # 2. Genres
        dummy_genre = self.create_genre("Rock", "US", "1950", "wiki.com")
        self.create_genre("Blues", "US", "1895", "wiki.com")

        # 3. Albums
        dummy_album = self.create_album("American IV", "2003-02-02", dummy_artist,
                                        "56.45", "NYC", "Rick Rubin", "4", """American
                                        Recordings""", "w.com", "p.com")

        # 4. Songs
        dummy_song = self.create_song("The man comes around", "2002-12-01",
                         dummy_artist, "4.53", "4", "w.com", "p.com", dummy_genre)
        # add album manually as it is a many-to-many relation
        dummy_song.album.add(dummy_album)


class GetAllTest(BaseViewTest):

    def test_get_all_artist(self):
        """
        This test ensures that all songs added in the setUp method
        exist when we make a GET request to the songs/ endpoint
        """
        # hit the API endpoint
        response = self.client.get(
            reverse("artists-all", kwargs={"version": "v1"})
        )
        # fetch the data from db
        expected = Artist.objects.all()
        serialized = ArtistSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_genres(self):
        """
        This test ensures that all genres added in the setUp method
        exist when we make a GET request to the genres/ endpoint
        """
         # hit the API endpoint
        response = self.client.get(
            reverse("genres-all", kwargs={"version": "v1"})
        )
         # fetch the data from db
        expected = Genre.objects.all()
        serialized = GenreSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_get_all_albums(self):
        """
        This test ensures that all albums added in the setUp method
        exist when we make a GET request to the albums/ endpoint
        """
         # hit the API endpoint
        response = self.client.get(
            reverse("albums-all", kwargs={"version": "v1"})
        )
         # fetch the data from db
        expected = Album.objects.all()
        serialized = AlbumSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_songs(self):
        """
        This test ensures that all albums added in the setUp method
        exist when we make a GET request to the albums/ endpoint
        """
         # hit the API endpoint
        response = self.client.get(
            reverse("songs-all", kwargs={"version": "v1"})
        )
         # fetch the data from db
        expected = Song.objects.all()
        serialized = SongSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
