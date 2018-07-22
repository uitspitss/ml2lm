import re
import logging
from django.db import models
from django.utils.translation import gettext_lazy as _


logger = logging.getLogger(__name__)
mp = re.compile(r'\d+?$')


class Playlist(models.Model):
    url = models.URLField(
        db_index=True,
        verbose_name=_('プレイリストURL'),
    )
    title = models.TextField(
        verbose_name=_('プレイリストタイトル'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('生成日時'),
    )
    count = models.IntegerField(
        default=0,
        verbose_name=_('アクセス回数'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('更新日時'),
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
        'Playlist',
        related_name='movies',
        on_delete=models.CASCADE,
        verbose_name=_('プレイリスト'),
    )
    url = models.URLField(
        verbose_name=_('動画URL'),
    )
    title = models.TextField(
        verbose_name=_('動画タイトル'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('生成日時'),
    )
    count = models.IntegerField(
        default=0,
        verbose_name=_('アクセス回数'),
    )

    def __str__(self):
        return mp.search(self.url)[0]
