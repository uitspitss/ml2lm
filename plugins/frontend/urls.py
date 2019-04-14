from django.urls import path, include
from django.views.generic import TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie

urlpatterns = [
    path(
        '',
        ensure_csrf_cookie(TemplateView.as_view(template_name='frontend/index.html')),
    )
]
