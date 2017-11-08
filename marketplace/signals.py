from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from .models import UserMarketplaceInfo

@receiver(post_save, sender=User)
def create_info_for_user(sender, raw, instance, **kwargs):
    if raw: return
    if not len(UserMarketplaceInfo.objects.filter(user=instance)):
        info = UserMarketplaceInfo(user=instance)
        info.save()
