from django.contrib import admin
from .models import Category, Course


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'category', 'price', 'discount_price', 'level', 'is_published', 'is_approved', 'created_at']
    list_filter = ['is_published', 'is_approved', 'level', 'language', 'category', 'created_at']
    search_fields = ['title', 'description', 'instructor__username']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published', 'is_approved']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'description', 'thumbnail')
        }),
        ('Pricing', {
            'fields': ('price', 'discount_price')
        }),
        ('Details', {
            'fields': ('category', 'level', 'language', 'instructor', 'requirements', 'outcomes')
        }),
        ('Status', {
            'fields': ('is_published', 'is_approved', 'total_duration', 'total_lessons')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
