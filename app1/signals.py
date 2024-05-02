# In your signals.py file
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User

# @receiver(post_save, sender=User)
# def send_activation_email(sender, instance, created, **kwargs):
#     if created or (not instance.is_active and instance._previous_is_active):
#         if instance.is_active:
#             subject = 'Your account has been activated'
#             message = 'Dear {}, your account has been activated.'.format(instance.username)
#             send_mail(subject, message, 'xtharxman@gmail.com', [instance.email])



# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def send_activation_email(sender, instance, **kwargs):
    if instance.is_active:
        subject = 'Account Activated'
        message = f'Dear {instance.first_name} {instance.last_name},\nYour MyTask account is approved by the admin. You can now login to your MyTask account with the following detail:\n\nusername:{instance.username}\n\n\nThankYou\nMyTaskAdmin'
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, [instance.email], fail_silently=False)