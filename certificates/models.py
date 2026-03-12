from django.db import models
from users.models import User
from courses.models import Course


class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    certificate_id = models.CharField(max_length=50, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'course']
        ordering = ['-issued_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
    
    def get_certificate_url(self):
        from django.urls import reverse
        return reverse('certificate_detail', kwargs={'certificate_id': self.certificate_id})
