from django.core.management import BaseCommand
from mainapp.models import News


class Command(BaseCommand):
    def handle(self, *args, **options):
        news_objects = []
        for i in range(10):
            news_objects.append(News(
                title=f'Тестовая новость #{i}',
                preamble=f'Тестовое описание к новости #{i}',
                body=f'Текст новости #{i}'
            ))  # добавляем обьекты к списку

        News.objects.bulk_create(news_objects)  # коммит в бд
