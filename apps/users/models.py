from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    email = models.EmailField(unique=True)

    avatar = models.ImageField(
        upload_to='users/avatars/',
        blank=True,
        null=True,
    )

    phone_number = models.CharField(
        max_length=16,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^(?:09\d{9}|\+[1-9]\d{7,14})$',
                message="Enter a valid international phone number, e.g. +989123456789.",
            ),
        ],
    )
    
    mantra = models.TextField(
        blank=True,
        max_length=300,
    )

    def __str__(self):
        return self.username