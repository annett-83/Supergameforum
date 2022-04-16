from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscriber = models.ManyToManyField(User, through='SubUser')

    def get_subscriber_mail_adresses(
            self):  # Methode die alle Benutzer-emails sucht, die diese Kategorie abbobiert haben
        a = User.objects.filter(category=self).values_list('email', flat=True).distinct()
        return list(a)

    def __str__(self):
        return self.name

    def posts(self):
        return Post.objects.filter(category=self)

    def get_newpost_url(self):
        from django.urls import reverse
        return reverse('edit_post', kwargs={'pk': self.pk,'action':'new'})

    def is_subscribed_by_user(self, user):
        return User.objects.filter(category=self)



class SubUser(models.Model):
    sub_user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=64, unique=False)
    text = models.CharField(max_length=256, unique=False)
    def media_attachments(self):
        return MediaAttachment.objects.filter(post=self)

    def answers(self):
        return Answer.objects.filter(post=self)

    def acceptedAnswers(self):
        return Answer.objects.filter(post=self, isAccepted=True) # zeigt gleichnur akzeptierte antworts, muss nichtin HTML extra beschreiben

    def unacceptedAnswers(self):
        return Answer.objects.filter(post=self, isAccepted=False) # zeigt gleichnur akzeptierte antworts, muss nichtin HTML extra beschreiben

    def get_newanswer_url(self):
        from django.urls import reverse
        return reverse('edit_answer', kwargs={'pk': self.pk, 'action':'new'})

    def get_edit_url(self):
        from django.urls import reverse
        return reverse('edit_post', kwargs={'pk': self.pk, 'action':'edit'})

    def get_delete_url(self):
        from django.urls import reverse
        return reverse('edit_post', kwargs={'pk': self.pk, 'action':'delete'})

class MediaAttachment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    fileName = models.CharField(max_length=256)
    fileType= models.CharField(max_length=256)

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    text = models.CharField(max_length=256)
    isAccepted = models.BooleanField(default=False)

    def get_edit_url(self):
        from django.urls import reverse
        return reverse('edit_answer', kwargs={'pk': self.pk, 'action':'edit'})

    def get_delete_url(self):
        from django.urls import reverse
        return reverse('edit_answer', kwargs={'pk': self.pk, 'action':'delete'})

    def get_accept_url(self):
        from django.urls import reverse
        return reverse('edit_answer', kwargs={'pk': self.pk, 'action':'accept'})



