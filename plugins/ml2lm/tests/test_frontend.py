import pytest
from django_webtest import WebTestMixin

@pytest.mark.django_db
class TestFrontend:

    @pytest.fixture
    def app(self):
        wt = WebTestMixin()
        wt._patch_settings()
        wt.renew_app()
        return wt.app

    @pytest.mark.usefixtures('app')
    @pytest.mark.parametrize('url, status_code', [
        ('/', 200),
        ('/api/playlist/', 200)
    ])
    def test_acceptance(self, app, url, status_code):
        r = app.get(url)
        assert r.status_int == status_code
