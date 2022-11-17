from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    email = models.EmailField(blank=True, verbose_name='Email', unique=True)  # переопределяем email от AbstractUser
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', **NULLABLE)
    avatar = models.ImageField(upload_to='users', **NULLABLE)  #

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
