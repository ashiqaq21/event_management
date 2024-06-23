# tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_event_creation_email(recipient_list):
    subject = 'A New Event has been created'
    message = 'A new event has been created. Please check it out on the event page.'
    from_email = 'your-email@example.com'
    
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )

@shared_task
def send_event_updation_email(recipient_list):
    subject = 'An Event has been updated'
    message = 'An event has been updated. Please check it out on the event page.'
    from_email = 'your-email@example.com'
    
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )
