from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path('category/<slug:slug>/', views.category_courses, name='category_courses'),
    path('instructor/courses/', views.instructor_course_list, name='instructor_course_list'),
    path('instructor/courses/create/', views.instructor_course_create, name='instructor_course_create'),
    path('instructor/courses/<int:course_id>/edit/', views.instructor_course_edit, name='instructor_course_edit'),
    path('instructor/courses/<int:course_id>/delete/', views.instructor_course_delete, name='instructor_course_delete'),
    path('api/wishlist/toggle/', views.toggle_wishlist, name='toggle_wishlist'),
]
