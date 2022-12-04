from datetime import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, ListView, CreateView, DetailView, UpdateView, DeleteView
from mainapp import models as mainapp_models
from mainapp import forms as mainapp_forms


class MainPageView(TemplateView):
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
            mainapp_models.Courses, pk=pk
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
    template_name = 'mainapp/contacts.html'


class DocSitePageView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class LoginPageView(TemplateView):
    template_name = 'mainapp/login.html'
