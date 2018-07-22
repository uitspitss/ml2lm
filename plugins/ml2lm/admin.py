# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.forms import widgets

from .models import Playlist, Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'playlist',
        'url',
        'title',
        'created_at',
        'count',
    )
    list_filter = ('playlist', 'created_at')
    date_hierarchy = 'created_at'
    formfield_overrides = {
        models.TextField: {
            'widget': widgets.TextInput
        }
    }


class MovieInline(admin.TabularInline):
    model = Movie
    formfield_overrides = {
        models.TextField: {
            'widget': widgets.TextInput
        }
    }


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'url',
        'title',
        'created_at',
        'updated_at',
        'count',
    )
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    formfield_overrides = {
        models.TextField: {
            'widget': widgets.TextInput
        }
    }

    inlines = (MovieInline,)
