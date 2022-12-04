from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class ObjectManager(models.Manager):
    """
    для фильтрации удаленных обьектов с методички #TODO
    """

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class News(models.Model):
    objects = ObjectManager()
    title = models.CharField(max_length=256, verbose_name='Title')
    preamble = models.CharField(max_length=1024, verbose_name='Preamble')
    body = models.TextField(verbose_name='Body', **NULLABLE)
    as_markdown = models.BooleanField(default=False, verbose_name='As markdown')
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Created')
    updated = models.DateTimeField(auto_now=True, editable=False, verbose_name='Edited')
    deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.pk} {self.title}'  # видимо pk это primary key - id таблицы

    def delete(self):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'


class Course(models.Model):
    title = models.CharField(max_length=256, verbose_name='Title')
    description = models.TextField(verbose_name='Description', **NULLABLE)
    as_markdown = models.BooleanField(default=False, verbose_name='As markdown')
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Cost', default=0)
    image_path = models.CharField(max_length=1024, verbose_name='Image', **NULLABLE)

    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Created')
    updated = models.DateTimeField(auto_now=True, editable=False, verbose_name='Edited')
    deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title  # видимо pk это primary key - id таблицы

    def delete(self):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    num = models.PositiveIntegerField(verbose_name='Lesson number')

    title = models.CharField(max_length=256, verbose_name='Title')
    description = models.TextField(verbose_name='Description', **NULLABLE)
    as_markdown = models.BooleanField(default=False, verbose_name='As markdown')

    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Created')
    updated = models.DateTimeField(auto_now=True, editable=False, verbose_name='Edited')
    deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.pk} {self.title}'  # видимо pk это primary key - id таблицы

    def delete(self):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class CourseTeacher(models.Model):
    course = models.ManyToManyField(Course)
    first_name = models.CharField(max_length=128, verbose_name='Name')
    second_name = models.CharField(max_length=128, verbose_name='Surname')
    day_birth = models.DateTimeField(verbose_name='Birth date')

    deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.pk} {self.first_name} {self.second_name}'  # видимо pk это primary key - id таблицы

    def delete(self):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = 'учитель'
        verbose_name_plural = 'учителя'


class CourseFeedback(models.Model):
    RATING = ((5, "⭐⭐⭐⭐⭐"), (4, "⭐⭐⭐⭐"), (3, "⭐⭐⭐"), (2, "⭐⭐"), (1, "⭐"))
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name=_("Course")
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name=_("User")
    )
    feedback = models.TextField(
        default=_("No feedback"), verbose_name=_("Feedback")
    )
    rating = models.SmallIntegerField(
        choices=RATING, default=5, verbose_name=_("Rating")
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course} ({self.user})"
