from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import uuid
from .models import Payment
from enrollments.models import Enrollment


@login_required
def payment_checkout(request, course_id):
    from courses.models import Course
    course = get_object_or_404(Course, id=course_id, is_published=True)
    
    if course.price == 0:
        return redirect('enroll_in_course', course_id=course_id)
    
    existing_enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    if existing_enrollment:
        messages.info(request, 'You are already enrolled in this course.')
        return redirect('course_detail', slug=course.slug)
    
    amount = course.discount_price if course.discount_price else course.price
    
    return render(request, 'payments/checkout.html', {
        'course': course,
        'amount': amount,
    })


@login_required
def initiate_payment(request, course_id):
    from courses.models import Course
    course = get_object_or_404(Course, id=course_id, is_published=True)
    
    if course.price == 0:
        return redirect('enroll_in_course', course_id=course_id)
    
    existing_enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    if existing_enrollment:
        messages.info(request, 'You are already enrolled in this course.')
        return redirect('course_detail', slug=course.slug)
    
    amount = course.discount_price if course.discount_price else course.price
    
    transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
    
    payment = Payment.objects.create(
        user=request.user,
        course=course,
        amount=amount,
        transaction_id=transaction_id,
        status='completed'
    )
    
    Enrollment.objects.create(
        user=request.user,
        course=course,
        payment=payment
    )
    
    messages.success(request, f'Successfully enrolled in {course.title}!')
    
    if course.modules.exists() and course.modules.first().lessons.exists():
        first_lesson = course.modules.first().lessons.first()
        return redirect('lesson_player', course_slug=course.slug, lesson_id=first_lesson.id)
    
    return redirect('course_detail', slug=course.slug)


@login_required
def payment_history(request):
    payments = Payment.objects.filter(user=request.user).select_related('course')
    return render(request, 'payments/payment_history.html', {'payments': payments})


@login_required
def payment_success(request, transaction_id):
    payment = get_object_or_404(Payment, transaction_id=transaction_id, user=request.user)
    payment.status = 'completed'
    payment.save()
    
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=payment.course,
        defaults={'payment': payment}
    )
    
    messages.success(request, 'Payment successful! You are now enrolled in the course.')
    return redirect('course_detail', slug=payment.course.slug)


@login_required
def payment_failed(request):
    messages.error(request, 'Payment failed. Please try again.')
    return redirect('course_list')
