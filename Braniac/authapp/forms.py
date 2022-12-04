from django import forms
from django.contrib.auth import get_user_model
from mainapp import models as mainapp_models
from django.contrib.auth.forms import UserCreationForm, UsernameField


class CustomUserCreationForm(
    UserCreationForm):  # форма регистрации пользователя(от модели), все данные указываются в классе Meta
    field_order = [  # порядок отображения на странице
        "username",
        "password1",
        "password2",
        "email",
        "first_name",
        "last_name",
        "age",
        "avatar",
    ]

    class Meta:
        model = get_user_model()  # возвращает модель пользователя для текущего проекта

        fields = (  # заполняемые поля, в порядке из таблицы
            "username",
            "email",
            "first_name",
            "last_name",
            "age",
            "avatar",
        )
        field_classes = {"username": UsernameField}  # тип поля формы


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()

        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "age",
            "avatar",
        )
        field_classes = {"username": UsernameField}
