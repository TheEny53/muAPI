from django.contrib import admin
from .models import Song, Album, Artist, Genre

admin.site.register(Song)
admin.site.register(Album)
admin.site.register(Artist)
admin.site.register(Genre)
