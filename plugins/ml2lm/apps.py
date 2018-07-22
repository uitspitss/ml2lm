from django.apps import AppConfig


class Ml2lmConfig(AppConfig):
    name = 'plugins.ml2lm'
    verbose_name = 'ml2lm'

    def ready(self):
        from . import signals
