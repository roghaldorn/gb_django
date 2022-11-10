from django.db import models


class BaseClass(models.Model):
    deleted = models.BooleanField(default=False, verbose_name='Удален')
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.title}, {self.created_at}'

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class News(BaseClass):
    """
    News model
    """

    preamble = models.CharField(max_length=1024, verbose_name='Описание')
    body = models.TextField(verbose_name='Содержимое')

    body_as_markdown = models.BooleanField(default=False, verbose_name='Разметка Markdown')

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'


class Course(BaseClass):
    description = models.TextField(verbose_name='Описание')
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Стоимость', default=0)
    img_source = models.FilePathField(default='NULL', verbose_name='Путь к медиа')

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(BaseClass):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    num = models.PositiveIntegerField(default=0, verbose_name='Номер урока')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class CourseTeacher(models.Model):
    courses = models.ManyToManyField(Course)
    first_name = models.CharField(max_length=256, verbose_name='Имя')
    last_name = models.CharField(max_length=256, verbose_name='Фамилия')

    class Meta:
        verbose_name = 'курс к учителю'
        verbose_name_plural = 'курсы к учителям'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    delete = BaseClass.delete
