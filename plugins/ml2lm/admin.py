from django.contrib import admin
from django.db import models
from django.forms import widgets
from django.contrib.auth.decorators import login_required

from .models import Playlist, Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'playlist', 'url', 'title', 'created_at', 'count')
    list_filter = ('playlist', 'created_at')
    date_hierarchy = 'created_at'
    formfield_overrides = {models.TextField: {'widget': widgets.TextInput}}


class MovieInline(admin.TabularInline):
    model = Movie
    formfield_overrides = {models.TextField: {'widget': widgets.TextInput}}


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('short_id', 'url', 'title', 'count', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    formfield_overrides = {models.TextField: {'widget': widgets.TextInput}}

    inlines = (MovieInline,)


admin.site.login = login_required(admin.site.login)
