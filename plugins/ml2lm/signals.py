import logging
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Playlist


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Playlist)
def notify_created_playlist(sender, instance, created, **kwargs):
    if created:
        logger.debug(
            f"created shorturl of {instance.url}"
        )
    else:
        logger.debug(
            f"updated shorturl of {instance.url}"
        )
