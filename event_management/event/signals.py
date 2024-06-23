# signals.py
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Event
from .tasks import send_event_creation_email, send_event_updation_email

@receiver(post_save, sender=Event)
def CreateEvent(sender, instance, created, **kwargs):
    if created:
        users = User.objects.exclude(role__in=['Admin', 'Organizer'])
        recipient_list = [user.email for user in users if user.email]
        send_event_creation_email.delay(recipient_list)  # Use .delay() to call the task asynchronously

@receiver(post_save, sender=Event)
def UpdateEvent(sender, instance, created, **kwargs):
    if not created:
        users = User.objects.exclude(role__in=['Admin', 'Organizer'])
        recipient_list = [user.email for user in users if user.email]
        send_event_updation_email.delay(recipient_list)  # Use .delay() to call the task asynchronously
