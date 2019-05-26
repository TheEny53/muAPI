from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
RATING = (
    ("0", "*"),
    ("1", "**"),
    ("2", "***"),
    ("3", "****"),
    ("4", "*****")
)

YEAR_VALIDATORS = [
        MaxValueValidator(2999),
        MinValueValidator(1000)
        ]

class Artist(models.Model):
    """Describing an Artist, containing all necessary metadata"""
    name = models.CharField(max_length=255, null=False, blank=False)
    founding_year = models.IntegerField(null=True, blank=True, validators=YEAR_VALIDATORS)
    founding_country = models.CharField(max_length=2, blank=True, null=True)
    is_active = models.BooleanField(null=False, blank=False)
    rating = models.CharField(max_length=1, choices=RATING, blank=False, null=False)
    wiki_link = models.URLField(blank=False, null=False)
    picture_link = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return "{}".format(self.name)


class Album(models.Model):
    """Describing an Album, containing all necessary metadata"""
    name = models.CharField(max_length=255, null=False, blank=False)
    release_date = models.DateField(null=True, blank=True)
    artist = models.ForeignKey(to=Artist, on_delete=models.CASCADE, blank=False, null=True)
    length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    produced_at = models.CharField(max_length=255, null=True, blank=True)
    producer = models.CharField(max_length=255, null=True, blank=True)
    rating = models.CharField(max_length=1, choices=RATING, null=False, blank=False)
    label = models.CharField(max_length=255, null=True, blank=True)
    wiki_link = models.URLField(blank=False, null=False)
    picture_link = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
       return "{} - {}".format(self.artist, self.name)


class Genre(models.Model):
    """Describing a Genre, containing all necessary metadata"""
    name = models.CharField(max_length=255, null=False, blank=False)
    country_of_origin = models.CharField(max_length=2, null=True, blank=True)
    year_of_establishment = models.IntegerField(null=True, blank=True, validators=YEAR_VALIDATORS)
    wiki_link = models.URLField(blank=False, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return "{}".format(self.name)


class Song(models.Model):
    """Describing a Song, containing all necessary metadata"""
    name = models.CharField(max_length=255, null=False, blank=False)
    artist = models.ForeignKey(to=Artist, on_delete=models.CASCADE, blank=False)
    album = models.ManyToManyField(Album, blank=True, null=True)
    rating = models.CharField(max_length=1, choices=RATING, blank=False, null=False)
    release_date = models.DateField(null=True, blank=True)
    length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    wiki_link = models.URLField(blank=False, null=False)
    picture_link = models.URLField(blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return "{} - {}".format(self.name, self.artist)
