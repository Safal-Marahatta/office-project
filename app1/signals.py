
#app1/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def send_activation_email(sender, instance,update_fields,created,**kwargs):
        print("Signal triggered for user:", instance.username)
        if not created and (update_fields is None or 'is_active' in update_fields):
            print("is_active field updated to:", instance.is_active)
            if instance.is_active:
                print("Sending activation email to:", instance.email)
                subject = 'Account Activated'
                message = f'Dear {instance.first_name} {instance.last_name},\nYour MyTask account is approved by the admin. You can now login to your MyTask account with the following detail:\n\nusername:{instance.username}\n\n\nThankYou\nMyTaskAdmin'
                from_email = settings.EMAIL_HOST_USER
                send_mail(subject, message, from_email, [instance.email], fail_silently=False)

