from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.conf import settings
from django.contrib import messages
from rest_framework import viewsets, filters
from django.http import Http404

import re
import requests
from pathlib import Path
from sys import platform
from kawasemi.django import send
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


from .models import Playlist, Movie
from .forms import PlaylistForm
from .serializer import PlaylistSerializer, MovieSerializer

from logging import getLogger
logger = getLogger(__name__)


LOGIN_EMAIL = '1mit4t10n@gmail.com'
LOGIN_PASS = 'BxWrf60UoG'

NICO_MYLIST_BASE = 'http://www.nicovideo.jp/mylist/'


class RegistView(View):
    def get(self, request, *args, **kwargs):
        playlist_form = PlaylistForm()

        return render(
            request,
            'base.html',
            {
                'playlist_form': playlist_form,
            }
        )

    def post(self, request, *args, **kwargs):
        playlist_form = PlaylistForm(request.POST)

        if playlist_form.is_valid():
            mylist_url = playlist_form.cleaned_data['url']

            logger.info(f'it was posted {mylist_url}')

            mylist_id = re.search(r'(\d+)', mylist_url)[0]

            playlist = Playlist.objects.filter(
                url=NICO_MYLIST_BASE + mylist_id
            )

            if not playlist:
                self.driver = self.set_driver()
                self.login_nico()
                params = self.get_mylist_info(mylist_id)
                self.driver.close()

                if params:
                    playlist = self.save_playlist(params)
                    logger.info(
                        f'generated shorturl of {playlist.url}'
                    )
                else:
                    messages.error(
                        request,
                        'マイリストを取得できませんでした'
                    )
            else:
                playlist = get_object_or_404(
                    Playlist,
                    url=NICO_MYLIST_BASE + mylist_id
                )

        return render(
            request,
            'base.html',
            {
                'playlist_form': playlist_form,
                'playlist': playlist,
            }
        )

    def save_playlist(self, params: dict):
        playlist = Playlist(
            url=params['playlist_url'],
            title=params['playlist_title'],
        )
        playlist.save()

        latest_movie = Movie(
            url=params['latest_movie_url'],
            title=params['latest_movie_title'],
            playlist=playlist,
        )
        latest_movie.save()

        logger.info(
            f'saved {latest_movie.url} into {playlist.url}'
        )

        return playlist

    def get_mylist_info(self, mylist_id: str):
        if not self.driver:
            raise 'Driver Not Found'

        playlist_url = NICO_MYLIST_BASE + mylist_id
        sort_param = '#+sort=1'

        self.driver.get(playlist_url + sort_param)

        try:
            playlist_title = self.driver.title

            latest_movie_url = self.driver.find_element_by_xpath(
                '//table/tbody/tr/td[2]/p[2]/a').get_attribute('href')
            latest_movie_title = self.driver.find_element_by_xpath(
                '//table/tbody/tr/td[2]/p[2]/a').text.strip()

            return {
                'playlist_url': playlist_url,
                'playlist_title': playlist_title,
                'latest_movie_url': latest_movie_url,
                'latest_movie_title': latest_movie_title,
            }
        except:
            logger.error('incorrect mylist')

    def set_driver(self):
        driver = webdriver.PhantomJS(
            executable_path=Path(
                settings.BASE_DIR, 'bin',
                'mac' if platform == 'darwin'
                else 'linux',
                'phantomjs'
            ),
            service_args=[
                "--ignore-ssl-errors=true",
                "--ssl-protocol=any",
                "--disk-cache=false",
                "--load-images=false",
            ]
        )
        driver.set_page_load_timeout(10)
        return driver

    def login_nico(self):
        self.driver.get('https://account.nicovideo.jp/login?site=niconico')

        mail_tel = self.driver.find_element_by_xpath(
            '//*[@id="input__mailtel"]')
        mail_tel.send_keys(LOGIN_EMAIL)

        password = self.driver.find_element_by_xpath(
            '//*[@id="input__password"]')
        password.send_keys(LOGIN_PASS)

        login_button = self.driver.find_element_by_xpath(
            '//*[@id="login__submit"]')
        login_button.click()

        return True


class RedirectView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            pl = get_object_or_404(Playlist, pk=pk)
            pl.total_count += 1
            pl.save()

            latest_movie = pl.movies.order_by('-created_at')[0]
            latest_movie.count += 1
            latest_movie.save()

            logger.info(f'access {latest_movie} in {pl}')

            return redirect(latest_movie.url)
        else:
            raise Http404


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
