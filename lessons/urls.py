from django.urls import path
from . import views

urlpatterns = [
    path('course/<slug:course_slug>/lesson/<int:lesson_id>/', views.lesson_player, name='lesson_player'),
    path('api/mark-lesson-complete/<int:lesson_id>/', views.mark_lesson_complete, name='mark_lesson_complete'),
    path('instructor/module/create/<int:course_id>/', views.instructor_module_create, name='instructor_module_create'),
    path('instructor/module/<int:module_id>/edit/', views.instructor_module_edit, name='instructor_module_edit'),
    path('instructor/lesson/create/<int:module_id>/', views.instructor_lesson_create, name='instructor_lesson_create'),
    path('instructor/lesson/<int:lesson_id>/edit/', views.instructor_lesson_edit, name='instructor_lesson_edit'),
    path('instructor/lesson/<int:lesson_id>/delete/', views.instructor_lesson_delete, name='instructor_lesson_delete'),
]
