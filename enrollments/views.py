from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .models import Enrollment


@login_required
def enroll_in_course(request, course_id):
    from courses.models import Course
    course = get_object_or_404(Course, id=course_id, is_published=True)
    
    if course.price == 0:
        try:
            enrollment = Enrollment.objects.create(user=request.user, course=course)
            messages.success(request, f'Successfully enrolled in {course.title}!')
            
            first_module = course.modules.first()
            if first_module and first_module.lessons.exists():
                first_lesson = first_module.lessons.first()
                return redirect('lesson_player', course_slug=course.slug, lesson_id=first_lesson.id)
            return redirect('course_detail', slug=course.slug)
        except IntegrityError:
            messages.info(request, 'You are already enrolled in this course.')
            return redirect('course_detail', slug=course.slug)
    
    return redirect('initiate_payment', course_id=course.id)


@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course', 'course__instructor')
    
    enrollment_data = []
    for enrollment in enrollments:
        first_module = enrollment.course.modules.first()
        first_lesson = first_module.lessons.first() if first_module else None
        enrollment_data.append({
            'enrollment': enrollment,
            'first_lesson': first_lesson
        })
    
    return render(request, 'enrollments/my_courses.html', {'enrollment_data': enrollment_data})
