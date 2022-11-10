from django.views.generic import TemplateView
from datetime import datetime


class MainPageView(TemplateView):
    template_name = 'mainapp/index.html'


class NewsPageView(TemplateView):
    template_name = 'mainapp/news.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', '')
        context_data['news_title'] = "Контекстный заголовок для страницы {}".format(page)
        context_data['news_preview'] = 'Контекстное предварительное описание {}'.format(page)
        context_data['range'] = range(1, 6)
        context_data['page'] = page
        context_data['datetime_obj'] = datetime.now()
        return context_data



class CoursesPageView(TemplateView):
    template_name = 'mainapp/courses_list.html'


class ContractsPageView(TemplateView):
    template_name = 'mainapp/contacts.html'


class DocSitePageView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class LoginPageView(TemplateView):
    template_name = 'mainapp/login.html'
