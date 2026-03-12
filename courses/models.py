from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_courses', kwargs={'slug': self.slug})


class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    LANGUAGE_CHOICES = [
        ('english', 'English'),
        ('bangla', 'Bangla'),
        ('hindi', 'Hindi'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='courses/thumbnails/', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='english')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    is_published = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    total_duration = models.IntegerField(default=0, help_text='Duration in minutes')
    total_lessons = models.IntegerField(default=0)
    requirements = models.TextField(blank=True)
    outcomes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})
    
    def get_enrolled_count(self):
        from enrollments.models import Enrollment
        return Enrollment.objects.filter(course=self, completed=False).count()
    
    def get_completed_count(self):
        from enrollments.models import Enrollment
        return Enrollment.objects.filter(course=self, completed=True).count()
    
    def get_total_revenue(self):
        from payments.models import Payment
        return Payment.objects.filter(course=self, status='completed').aggregate(
            total=models.Sum('amount')
        )['total'] or 0
    
    def get_average_rating(self):
        from reviews.models import Review
        reviews = Review.objects.filter(course=self)
        if not reviews.exists():
            return 0
        return sum(r.rating for r in reviews) / reviews.count()
    
    def get_review_count(self):
        return self.reviews.count()


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='wishlist')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
