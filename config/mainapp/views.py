from django.views.generic import TemplateView
from datetime import datetime
from mainapp import models
from django.shortcuts import get_object_or_404


class MainPageView(TemplateView):
    template_name = 'mainapp/index.html'


class NewsPageView(TemplateView):
    template_name = 'mainapp/news.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = models.News.objects.filter(deleted=False)
        context_data['len_of_data'] = len(context_data)
        return context_data


class NewsDetail(TemplateView):
    template_name = 'mainapp/news_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object'] = get_object_or_404(models.News, pk=self.kwargs.get('pk'))
        return context_data


class CoursesPageView(TemplateView):
    template_name = 'mainapp/courses_list.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = models.Course.objects.filter(deleted=False)
        return context_data


class CoursesDetail(TemplateView):
    template_name = 'mainapp/course_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object'] = get_object_or_404(models.Course, pk=self.kwargs.get('pk'))
        return context_data


class ContractsPageView(TemplateView):
    template_name = 'mainapp/contacts.html'


class DocSitePageView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class LoginPageView(TemplateView):
    template_name = 'mainapp/login.html'
