from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.user.models import KYC

User = get_user_model()


@receiver(pre_save, sender=User)
def send_account_creation_email(sender, instance, created, *args, **kwargs):
    if created:
        # send email here
        pass

@receiver(pre_save, sender=KYC)
def send_kyc_creation_email(sender, instance, created, *args, **kwargs):
    if created:
        # send email here
        pass
