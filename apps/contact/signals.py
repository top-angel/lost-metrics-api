from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from apps.contact.models import Interest


@receiver(post_save, sender=Interest)
def update_contact_last_updated_datetime(sender, instance, created, *args, **kwargs):
    if created:
        contact = instance.contact
        contact.last_interest_datetime = timezone.now()
        contact.save()