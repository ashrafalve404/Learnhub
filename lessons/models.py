from django.db import models
from courses.models import Course


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    def get_lessons_count(self):
        return self.lessons.count()
    
    def get_total_duration(self):
        return sum(lesson.duration for lesson in self.lessons.all())


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    video_id = models.CharField(max_length=100, blank=True, help_text='YouTube video ID')
    duration = models.IntegerField(default=0, help_text='Duration in minutes')
    order = models.PositiveIntegerField(default=0)
    is_preview = models.BooleanField(default=False)
    resources = models.TextField(blank=True, help_text='Links to resources, one per line')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title
    
    def get_duration_display(self):
        hours = self.duration // 60
        minutes = self.duration % 60
        if hours:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"
