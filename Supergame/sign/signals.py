from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.contrib.auth.models import User
from django.template.loader import render_to_string
#from .views import EMAIL_LINK_DOMAIN

from .models import UserValidation


@receiver(post_save, sender=User)
def addUserValidationEntry(sender, instance, created, **kwargs):
    if not UserValidation.objects.filter(user=instance).exists():
        uv=UserValidation(user=instance)
        uv.save()
        subject = f'Sie sind registriert, hier ist ihr validation code'

        html_content = render_to_string(  # Erstellen der email
            'flatpages/send_validation_code.html',
            {
                'validationcode': uv.validationCode,
            }
        )
        msg = EmailMultiAlternatives(  # Zusammebasteln der Mail
            subject=subject,
            to=[instance.email],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()  # отсылаем und weg damit


