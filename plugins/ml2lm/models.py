import re
import logging
from django.db import models
from django.utils.translation import gettext_lazy as _


logger = logging.getLogger(__name__)
mp = re.compile(r'\d+?$')


class Playlist(models.Model):
    url = models.URLField(
        _('プレイリストURL'),
        db_index=True
    )
    title = models.TextField(
        _('プレイリストタイトル'),
    )
    created_at = models.DateTimeField(
        _('生成日時'),
        auto_now_add=True,
    )
    count = models.IntegerField(
        _('アクセス回数'),
        default=0,
    )
    updated_at = models.DateTimeField(
        _('更新日時'),
        auto_now=True,
    )

    def get_absolute_url(self):
        return f'/playlist/{self.pk}/'

    def __str__(self):
        try:
            return mp.search(self.url)[0]
        except Exception as e:
            return self.url


class Movie(models.Model):
    playlist = models.ForeignKey(
        _('プレイリスト'),
        related_name='movies',
        on_delete=models.CASCADE
    )
    url = models.URLField(
        _('動画URL'),
    )
    title = models.TextField(
        _('動画タイトル'),
    )
    created_at = models.DateTimeField(
        _('生成日時'),
        auto_now_add=True,
    )
    count = models.IntegerField(
        _('アクセス回数'),
        default=0,
    )

    def __str__(self):
        return mp.search(self.url)[0]
