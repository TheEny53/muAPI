import json
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

    def fetch_single(self, pk=0, revUrl=""):
        if revUrl != "":
            return self.client.get(
                reverse(
                    revUrl,
                    kwargs={
                        "version": "v1",
                        "pk": pk
                    }
                )
            )

    def post_request(self, revUrl, **kwargs):
        return self.client.post(
            reverse(
                revUrl,
                kwargs={
                    "version": kwargs["version"]
                }
            ),
            data=json.dumps(kwargs["data"]),
            content_type='application/json'
        )

    def delete_single(self, pk=0,  revUrl="", **kwargs):
        return self.client.delete(
            reverse(revUrl,
                    kwargs={
                        "version": kwargs["version"],
                        "pk": pk
            })
        )

    def setUp(self):
        # create test data
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

        self.valid_song_id = 1
        self.valid_album_id = 1
        self.valid_artist_id = 1
        self.valid_genre_id = 1

        self.invalid_id = 100

        self.valid_song_data = {
            "name": "Paradise City",
            "artist": self.valid_artist_id,
            "album": self.valid_album_id,
            "rating": "3",
            "wiki_link": "wiki.com/gnr",
            "picture_link": "wiki.com/gnr",
            "release_date": "1970-05-18",
            "length": "4.53",
            "genre": self.valid_genre_id
        }

        self.valid_artist_data = {
            "name": "Guns'n'Roses",
            "founding_year": 1985,
            "founding_country": "US",
            "is_active": True,
            "rating": "3",
            "wiki_link": "w.com",
            "picture_link": "p.com"
        }

        self.valid_genre_data = {
            "name": "Rock",
            "country_of_origin": "US",
            "year_of_establishment": 1950,
            "wiki_link": "w.com"
        }

        self.valid_album_data = {
            "name": "Welcome to the Jungle",
            "release_date": "1987-05-04",
            "artist": self.valid_artist_id,
            "length": "56.57",
            "produced_at": "NYC",
            "producer": "Rick Rubin",
            "rating": "4",
            "label": "American Recordings",
            "wiki_link": "w.com",
            "picture_link": "p.com"
        }


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


class GetSingleTest(BaseViewTest):
    def test_get_single_album(self):
        response = self.fetch_single(self.valid_album_id, "album-detail")
        expected = Album.objects.get(pk=self.valid_album_id)
        serialized = AlbumSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.fetch_single(self.invalid_id, "album-detail")
        self.assertEqual(
            response.data["message"],
            "Album with id: {} does not exist".format(self.invalid_id)
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_single_song(self):
        response = self.fetch_single(self.valid_song_id, "song-detail")
        expected = Song.objects.get(pk=self.valid_song_id)
        serialized = SongSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.fetch_single(self.invalid_id, "song-detail")
        self.assertEqual(
            response.data["message"],
            "Song with id: {} does not exist".format(self.invalid_id)
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_single_artist(self):
        response = self.fetch_single(self.valid_artist_id, "artist-detail")
        expected = Artist.objects.get(pk=self.valid_artist_id)
        serialized = ArtistSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.fetch_single(self.invalid_id, "artist-detail")
        self.assertEqual(
            response.data["message"],
            "Artist with id: {} does not exist".format(self.invalid_id)
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_single_genre(self):
        response = self.fetch_single(self.valid_genre_id, "genre-detail")
        expected = Genre.objects.get(pk=self.valid_artist_id)
        serialized = GenreSerializer(expected)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.fetch_single(self.invalid_id, "genre-detail")
        self.assertEqual(
            response.data["message"],
            "Genre with id: {} does not exist".format(self.invalid_id)
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PostSingleTest(BaseViewTest):
    def test_create_song(self):
        response = self.post_request(
            version="v1",
            data=self.valid_song_data,
            revUrl="songs-all"
        )
        jso = json.loads(response.content)
        jso.pop("pk", None)
        jso.pop("album", None)
        self.valid_song_data.pop("album", None)
        self.assertEqual(jso, self.valid_song_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_artist(self):
        response = self.post_request(
            version="v1",
            data=self.valid_artist_data,
            revUrl="artists-all"
        )
        jso = json.loads(response.content)
        jso.pop("pk", None)
        self.assertEqual(jso, self.valid_artist_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_genre(self):
        response = self.post_request(
            version="v1",
            data=self.valid_genre_data,
            revUrl="genres-all"
        )
        jso = json.loads(response.content)
        jso.pop("pk", None)
        self.assertEqual(jso, self.valid_genre_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_album(self):
        response = self.post_request(
            version="v1",
            data=self.valid_album_data,
            revUrl="albums-all"
        )
        jso = json.loads(response.content)
        jso.pop("pk", None)
        self.assertEqual(jso, self.valid_album_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class DeleteSingleTest(BaseViewTest):
    def test_delete_song(self):
        response = self.delete_single(
            pk=self.valid_song_id,
            revUrl="song-detail",
            version="v1"
        )
        response_invalid = self.delete_single(
            pk=self.invalid_id,
            revUrl="song-detail",
            version="v1"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_invalid.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_album(self):
        response = self.delete_single(
            pk=self.valid_album_id,
            revUrl="album-detail",
            version="v1"
        )
        response_invalid = self.delete_single(
            pk=self.invalid_id,
            revUrl="album-detail",
            version="v1"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_invalid.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_genre(self):
        response = self.delete_single(
            pk=self.valid_genre_id,
            revUrl="genre-detail",
            version="v1"
        )
        response_invalid = self.delete_single(
            pk=self.invalid_id,
            revUrl="genre-detail",
            version="v1"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_invalid.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_artist(self):
        response = self.delete_single(
            pk=self.valid_artist_id,
            revUrl="artist-detail",
            version="v1"
        )
        response_invalid = self.delete_single(
            pk=self.invalid_id,
            revUrl="artist-detail",
            version="v1"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_invalid.status_code, status.HTTP_404_NOT_FOUND)