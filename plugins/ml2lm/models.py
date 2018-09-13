import re
import logging
from django.db import models
from django.utils.translation import gettext_lazy as _


logger = logging.getLogger(__name__)


class Playlist(models.Model):
    short_id = models.SlugField(
        max_length=6,
        unique=True,
    )
    url = models.URLField(
        verbose_name=_("プレイリストURL"),
        unique=True,
    )
    title = models.TextField(
        verbose_name=_("プレイリストタイトル"),
    )
    count = models.IntegerField(
        default=0,
        verbose_name=_("アクセス回数"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("生成日時"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("更新日時"),
    )

    @property
    def site(self) -> str:
        if re.search(r'https?://www.nicovideo.jp/', self.url):
            return "nicovideo"
        elif re.search(r'https?://www.youtube.com/', self.url):
            return "youtube"
        else:
            return "others"

    @property
    def latest_movie(self) -> models.Model:
        latest_movie = self.movies.order_by('-created_at').first()
        return latest_movie

    @property
    def thumbnail_url(self) -> str:
        url = ""
        if self.site == "nicovideo":
            mo = re.search(r'sm(\d+?)\/*$', self.latest_movie.url)
            if mo:
                latest_movie_id = mo[1]
                url = f"http://tn.smilevideo.jp/smile?i={latest_movie_id}"
        elif self.site == "youtube":
            mo = re.search(r'v=(.+)&', self.latest_movie.url)
            if mo:
                latest_movie_id = mo[1]
                url = f"https://i.ytimg.com/vi/{latest_movie_id}/mqdefault.jpg"

        return url

    def __str__(self) -> str:
        return self.short_id


class Movie(models.Model):
    playlist = models.ForeignKey(
        'Playlist',
        related_name='movies',
        on_delete=models.CASCADE,
        verbose_name=_("プレイリスト"),
    )
    url = models.URLField(
        verbose_name=_("動画URL"),
    )
    title = models.TextField(
        verbose_name=_("動画タイトル"),
    )
    count = models.IntegerField(
        default=0,
        verbose_name=_("アクセス回数"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("生成日時"),
    )

    def __str__(self) -> str:
        return self.url

