from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import IntegrityError
from .models import Review
from courses.models import Course
from enrollments.models import Enrollment
from .forms import ReviewForm


@login_required
def add_review(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    if not enrollment:
        messages.error(request, 'You must enroll in this course to leave a review.')
        return redirect('course_detail', slug=course.slug)
    
    existing_review = Review.objects.filter(user=request.user, course=course).first()
    if existing_review:
        messages.info(request, 'You have already reviewed this course.')
        return redirect('course_detail', slug=course.slug)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.course = course
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('course_detail', slug=course.slug)
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/review_form.html', {
        'form': form,
        'course': course
    })


@login_required
def my_reviews(request):
    reviews = Review.objects.filter(user=request.user).select_related('course')
    return render(request, 'reviews/my_reviews.html', {'reviews': reviews})
