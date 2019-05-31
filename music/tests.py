from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Artist, Genre
from .serializers import ArtistSerializer, GenreSerializer

# tests for views


class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_artist(name="", founding_year="", founding_country="", is_active="",
    rating="", wiki_link="", picture_link=""):
        if name != "" and founding_year != "" and founding_country != "" and rating != "" and is_active != "" and wiki_link != "":
            return Artist.objects.create(name=name, founding_year=founding_year, founding_country=founding_country,
            is_active=is_active, rating=rating, wiki_link=wiki_link, picture_link=picture_link)

    @staticmethod
    def create_genre(name="", country_of_origin="", year_of_establishment="", wiki_link=""):
        if name!="" and country_of_origin!="" and wiki_link!="":
            return Genre.objects.create(name=name, country_of_origin=country_of_origin,
            year_of_establishment=year_of_establishment, wiki_link=wiki_link)

    def setUp(self):
        # add test data
        # 1. Artists
        dummy_artist = self.create_artist("Sean Paul", "1987", "JA", "True", "3", "wiki.com", "wiki.com")
        self.create_artist("Michael Jackson", "1976", "US", "False", "4", "wiki.com/us", "wiki.com/pic")

        # 2. Genres
        dummy_genre = self.create_genre("Rock", "US", "1950", "wiki.com")
        self.create_genre("Blues", "US", "1895", "wiki.com")

class GetAllArtistsTest(BaseViewTest):

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

class GetAllGenresTest(BaseViewTest):

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