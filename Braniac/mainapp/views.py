from datetime import datetime
import logging

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.contrib.sessions.backends import cache
from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView

from Braniac import settings
from mainapp import models as mainapp_models
from mainapp import forms as mainapp_forms

from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from mainapp import tasks as mainapp_tasks

logger = logging.getLogger(__name__)  # создаем экземпляр логгера


class MainPageView(TemplateView):
    logger.debug('main_page_log')
    template_name = 'mainapp/index.html'


# NEW раздел от урока 6
class NewsListView(ListView):
    model = mainapp_models.News  # выбранная модель для списка
    paginate_by = 5  # разбивка по элементам

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)  # вывод без пометки удаления


class NewsDetailView(DetailView):
    model = mainapp_models.News  # выводимая модель


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    """
    UpdateView - как CreateView, но ворма уже заполнена данными
    """
    model = mainapp_models.News  # выводимая модель
    fields = "__all__"  # выводимые поля
    success_url = reverse_lazy("mainapp:news")  # перенаправление после отправки form
    permission_required = ("mainapp.change_news",)  # список разрешений


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = mainapp_models.News  # выводимая модель
    success_url = reverse_lazy("mainapp:news")  # перенаправление после отправки form
    permission_required = ("mainapp.delete_news",)  # список разрешений


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = mainapp_models.News  # выводимая модель
    fields = "__all__"  # выводимые поля
    success_url = reverse_lazy("mainapp:news")  # перенаправление после отправки form
    permission_required = ("mainapp.add_news",)  # тут указан список permission для пользователя, который хочет
    # воспользоваться формой, аттрибут от PermissionRequiredMixin


# END NEW
""" OLD
class NewsPageView(TemplateView):
    template_name = 'mainapp/news.html'

    def get_context_data(self, **kwargs):  # для шаблонов верстки
        context = super().get_context_data(**kwargs)
        context['news_title'] = 'Новостной заголовок.'
        context['news_preview'] = 'Краткое описание новости'
        context['news_db'] = mainapp_models.News.objects.all()[:5]
        context['range'] = range(5)
        context['datetime'] = datetime.now()
        return context

"""
""" OLD
class NewsWithPaginatorView(NewsPageView):
    def get_context_data(self, page, **kwargs):
        context = super().get_context_data(page=page, **kwargs)
        context['page_num'] = page
        return context
"""

""" OLD
class NewsDetailView(TemplateView):
    template_name = 'mainapp/news_detail.html'

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)  # иначе рекурсия
        context['news_object'] = get_object_or_404(mainapp_models.News, pk=pk)
        return context
"""


class CoursesPageView(TemplateView):
    template_name = 'mainapp/courses_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses_db'] = mainapp_models.Course.objects.all()
        return context


class CourseDetailView(TemplateView):
    template_name = "mainapp/courses_detail.html"

    def get_context_data(self, pk=None, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context["course_object"] = get_object_or_404(
            mainapp_models.Course, pk=pk
        )
        context["lessons"] = mainapp_models.Lesson.objects.filter(
            course=context["course_object"]
        )
        context["teachers"] = mainapp_models.CourseTeacher.objects.filter(
            course=context["course_object"]
        )
        if not self.request.user.is_anonymous:
            if not mainapp_models.CourseFeedback.objects.filter(
                    course=context["course_object"], user=self.request.user
            ).count():
                context["feedback_form"] = mainapp_forms.CourseFeedbackForm(
                    course=context["course_object"], user=self.request.user
                )
        context["feedback_list"] = mainapp_models.CourseFeedback.objects.filter(
            course=context["course_object"]
        ).order_by("-created", "-rating")[:5]
        return context


class CourseFeedbackFormProcessView(LoginRequiredMixin, CreateView):
    model = mainapp_models.CourseFeedback
    form_class = mainapp_forms.CourseFeedbackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_card = render_to_string(
            "mainapp/includes/feedback_card.html", context={"item": self.object}
        )
        return JsonResponse({"card": rendered_card})


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"

    def get_context_data(self, **kwargs):

        context = super(ContactsPageView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["form"] = mainapp_forms.MailFeedbackForm(
                user=self.request.user
            )
        return context

    def post(self, *args, **kwargs):

        if self.request.user.is_authenticated:
            cache_lock_flag = cache.get(
                f"mail_feedback_lock_{self.request.user.pk}"
            )

        if not cache_lock_flag:
            cache.set(
                f"mail_feedback_lock_{self.request.user.pk}",
                "lock",
                timeout=300,
            )
            messages.add_message(
                self.request, messages.INFO, _("Message sended")
            )
            mainapp_tasks.send_feedback_mail.delay(
                {
                    "user_id": self.request.POST.get("user_id"),
                    "message": self.request.POST.get("message"),
                }
            )
        else:
            messages.add_message(
                self.request,
                messages.WARNING,
                _("You can send only one message per 5 minutes"),
            )

        return HttpResponseRedirect(reverse_lazy("mainapp:contacts"))


class DocSitePageView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class LoginPageView(TemplateView):
    template_name = 'mainapp/login.html'


class LogView(TemplateView):
    template_name = 'mainapp/log_view.html'

    def get_context_data(self, **kwargs):
        context = super(LogView, self).get_context_data(**kwargs)
        log_slice = []
        with open(settings.LOG_FILE, 'r') as log_file:
            for line_index, line in enumerate(log_file):
                if line_index == 1000:
                    break
                log_slice.insert(0, line)
            context['log'] = ''.join(log_slice)
        return context


class LogDownloadView(UserPassesTestMixin, View):  # UserPassesTestMixin - проверка привилегий
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, 'rb'))
