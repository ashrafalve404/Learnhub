from django.contrib import admin
from .models import Module, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ['title', 'video_id', 'duration', 'order', 'is_preview']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'created_at']
    list_filter = ['course']
    search_fields = ['title', 'course__title']
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'order', 'duration', 'is_preview', 'created_at']
    list_filter = ['module__course', 'is_preview']
    search_fields = ['title', 'module__title']
    list_editable = ['order', 'is_preview']
