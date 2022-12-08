import os

from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from authapp import models, forms


class CustomLoginView(LoginView):
    template_name = 'authapp/login.html'

    def form_valid(self, form):
        ret = super().form_valid(form)
        message = f'Login success <br>Hi, {self.request.user.get_username()}'  # TODO
        messages.add_message(self.request, messages.INFO, mark_safe(message))
        return ret

    def form_invalid(self, form):
        for _, msg in form.error_messages.items():
            messages.add_message(
                self.request,
                messages.WARNING,
                mark_safe(f"Something goes wrong:<br>{msg}"),
            )
        return self.render_to_response(self.get_context_data(form=form))


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, _('See you'))
        return super().dispatch(request, *args, **kwargs)


"""
Форма регистрации через POST:

class RegisterView(TemplateView):
    template_name = 'authapp/register.html'

    def post(self, request, *args, **kwargs):
        try:
            if request.POST.get('username') and request.POST.get('email') and request.POST.get('password1') == request.POST.get('password2'):
                # почему то при использовании all() ошибка all() takes exactly one argument, 3 given
                new_user = models.CustomUser.objects.create(
                    username=request.POST.get('username'),
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    age=request.POST.get('age') if request.POST.get('age') else 0,
                    avatar=request.FILES.get('avatar'),
                    email=request.POST.get('email'),
                )
                new_user.set_password(request.POST.get('password1'))
                new_user.save()
                messages.add_message(request, messages.INFO, _('Registration sucess'))
                return HttpResponseRedirect(reverse_lazy('authapp:login'))
        except Exception as exp:
            messages.add_message(
                request,
                messages.WARNING,
                mark_safe(f'Something goes wrong:<br>{exp}')
            )
            return HttpResponseRedirect(reverse_lazy('authapp:register'))
"""


class RegisterView(CreateView):
    # по умолчанию template_name будет равен customuser_form.html
    template_name = 'authapp/register.html'
    model = get_user_model()  # указываем модель пользователя для тек.проекта
    form_class = forms.CustomUserCreationForm  # указываем нашу форму
    success_url = reverse_lazy('authapp:login')  # при успехе, reverse_lazy наверное выдает полный путь


class ProfileEditView(UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = forms.CustomUserChangeForm

    def test_func(self):
        return True if self.request.user.pk == self.kwargs.get("pk") else False

    def get_success_url(self):
        return reverse_lazy("authapp:profile_edit", args=[self.request.user.pk])


"""
class ProfileEditView(LoginRequiredMixin, TemplateView):
    template_name = 'authapp/profile_edit.html'
    login_url = reverse_lazy('authapp:login')

    def post(self, request, *args, **kwargs):
        try:
            if request.POST.get("username"):
                request.user.username = request.POST.get("username")
            if request.POST.get("first_name"):
                request.user.first_name = request.POST.get("first_name")
            if request.POST.get("last_name"):
                request.user.last_name = request.POST.get("last_name")
            if request.POST.get("age"):
                request.user.age = request.POST.get("age")
            if request.POST.get("email"):
                request.user.email = request.POST.get("email")
            if request.FILES.get("avatar"):
                if request.user.avatar and os.path.exists(
                        request.user.avatar.path
                ):
                    os.remove(request.user.avatar.path)
                request.user.avatar = request.FILES.get("avatar")
            request.user.save()
            messages.add_message(request, messages.INFO, _("Saved!"))
        except Exception as exp:
            messages.add_message(
                request,
                messages.WARNING,
                mark_safe(f"Something goes worng:<br>{exp}"),
            )
        return HttpResponseRedirect(reverse_lazy("authapp:profile_edit"))
"""