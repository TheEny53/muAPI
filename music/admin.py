from django.contrib import admin
from .models import Song, Album, Artist, Genre, Playlist

class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'rating', 'release_date', 'genre')
    list_filter = ('rating',)
    search_fields = ['name', 'artist']
    filter_horizontal = ('album',)

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'rating', 'release_date')
    list_filter = ('rating',)
    search_fields = ['name', 'artist']

class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'founding_country', 'rating', 'is_active')
    list_filter = ('rating', 'founding_country', 'is_active')
    search_fields = ('name', 'founding_country')

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'country_of_origin', 'year_of_establishment')
    list_filter = ('country_of_origin', 'year_of_establishment')
    search_fields = ('name', 'country_of_origin', 'year_of_establishment')

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'user')
    filter_horizontal = ('songs',)

admin.site.register(Song, SongAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Playlist, PlaylistAdmin)
