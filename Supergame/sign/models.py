import random

from django.db import models
from django.contrib.auth.models import User

class UserValidation(models.Model):
    user = models.OneToOneField(User, related_name="UserValidation", on_delete=models.CASCADE)
    validationCode = models.CharField(max_length=6, default="000000")
    isValidated = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:  # object is being created, thus no primary key field yet
            self.validationCode = str(random.randint(000000, 999999)).zfill(6)
        super(UserValidation, self).save(*args, **kwargs)

