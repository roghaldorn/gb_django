from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _  # транслитерация
from authapp.models_validators import AgeValidator

NULLABLE = {'blank': True, 'null': True}


class CustomUser(AbstractUser):
    username_validator = ASCIIUsernameValidator()  # валидатор - только ASCII символы
    age_validator = AgeValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text='Не больше 150 символов',
        validators=[username_validator],
        error_messages={'unique': _('User with that username already exists')})
    first_name = models.CharField(_('first name'), max_length=150, **NULLABLE)
    last_name = models.CharField(_('last name'), max_length=150, **NULLABLE)
    age = models.PositiveIntegerField(_('age'), validators=[age_validator], **NULLABLE)
    avatar = models.ImageField(upload_to='users', **NULLABLE)
    email = models.CharField(
        _('email address'),
        max_length=256,
        unique=True,
        error_messages={
            'unique': _('User with that email address already exists.')
        }
    )
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
