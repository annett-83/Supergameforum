from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver  # импортируем нужный декоратор
from django.contrib.auth.models import User
from django.template.loader import render_to_string
#from .views import EMAIL_LINK_DOMAIN

from .models import Post,Answer

@receiver(post_save, sender=Post)
def sendnewpostnotification(sender, instance, created, **kwargs):
        subject = f'There is a new Post in ' + instance.category.name
        html_content = render_to_string(  # Erstellen der email
        'flatpages/send_new_post_notification.html',
        {
        'post': instance,
        }
        )
        msg = EmailMultiAlternatives(  # Zusammebasteln der Mail
        subject=subject,
        to=instance.category.get_subscriber_mail_adresses(),  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()  # отсылаем und weg damit

@receiver(post_save, sender=Answer)
def sendnewanswernotification(sender, instance, created, **kwargs):
        if not instance.post.user==instance.user:
                subject = f'There is a new answer on your post  ' + instance.post.title
                html_content = render_to_string(  # Erstellen der email
                'flatpages/send_new_answer_notification.html',
                {
                'answer': instance,
                }
                )
                msg = EmailMultiAlternatives(  # Zusammebasteln der Mail
                subject=subject,
                to=[instance.post.user.email],  # это то же, что и recipients_list
                )
                msg.attach_alternative(html_content, "text/html")  # добавляем html
                msg.send()  # отсылаем und weg damit


