from django.contrib import admin
from mainapp import models as mainapp_models

META_COLUMNS = ['created', 'updated', 'deleted']


@admin.register(mainapp_models.News)  # регистрация модели в админке
class NewsAdmin(admin.ModelAdmin):  # логика отображения
    pass


@admin.register(mainapp_models.Course)  # регистрация модели в админке
class CourseAdmin(admin.ModelAdmin):  # логика отображения
    list_display = ['title', 'cost', *META_COLUMNS]  # что будет отображаться в админке
    ordering = ['-title']  # сортировка по
    list_per_page = 5  # строк на странице
    list_filter = ['title', 'cost']  # фильтр справа
    search_fields = ['title', 'description']  # регистронезависисый поиск по полям


@admin.register(mainapp_models.Lesson)  # регистрация модели в админке
class LessonAdmin(admin.ModelAdmin):  # логика отображения
    list_display = ['num', 'title', 'course', *META_COLUMNS]  # что будет отображаться в админке
    ordering = ['course', 'num']  # сортировка по
    list_per_page = 5  # строк на странице
    list_filter = ['course']  # фильтр справа
    search_fields = ['title', 'description']  # регистронезависисый поиск по полям
    actions = ['mark_restore']  # доп.действия, реализуются тут же в виде функций

    def mark_restore(self, request, queryset):
        """
        Убирает пометку удаления
        :param request: непонятно
        :param queryset: непонятно
        """
        queryset.update(deleted=False)
    mark_restore.short_description = 'Снять пометку удаления'  # имя, будет отображаться в админке


@admin.register(mainapp_models.CourseTeacher)  # регистрация модели в админке
class CourseTeacherAdmin(admin.ModelAdmin):  # логика отображения
    pass
