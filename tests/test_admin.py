import random
import pytest
from pprint import pprint
from hamcrest import *
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command

@pytest.mark.django_db
class TestAcceptance:

    @pytest.mark.parametrize('url, status_code', [
        ('/admin/', 200),
        ('/admin/login/', 302),
        ('/admin/auth/group/', 200),
        ('/admin/auth/group/add/', 200),
        ('/admin/auth/group/add', 301),
        ('/admin/auth/user/', 200),
        ('/admin/auth/user/add/', 200),
        ('/admin/auth/user/add', 301),
        ('/admin/dsdcso', 404),
    ])
    def test_admin_views(self, admin_client, url, status_code):
        c = admin_client.get(url)
        assert c.status_code == status_code