import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from phonenumber_field.modelfields import PhoneNumberField

def f(instance, filename):
    ext = filename.split('.')[-1]
    if instance.pk:
        if os.path.isfile('media/profile_avatar/{}.{}'.format(instance.pk, ext)):
            os.remove('media/profile_avatar/{}.{}'.format(instance.pk, ext))
        return os.path.join('profile_avatar/{}.{}'.format(instance.pk, ext))

class Account(AbstractUser):

    phone_number = PhoneNumberField(unique=True, null=True, blank=True)
    avatar = models.ImageField(_("avatar"), upload_to=f, blank=True, default='profile_avatar/default.png')
