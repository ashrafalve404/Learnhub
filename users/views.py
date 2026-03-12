from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserCreationForm, ProfileUpdateForm
from .models import User


def home(request):
    from courses.models import Course, Category
    featured_courses = Course.objects.filter(is_published=True, is_approved=True)
    categories = Category.objects.all()[:8]
    return render(request, 'home.html', {
        'featured_courses': featured_courses,
        'categories': categories,
    })


def about(request):
    return render(request, 'pages/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        messages.success(request, f'Thank you, {name}! We have received your message and will get back to you soon.')
        return redirect('contact')
    
    return render(request, 'pages/contact.html')


def teaching_guidelines(request):
    return render(request, 'pages/teaching_guidelines.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def dashboard(request):
    if request.user.is_instructor or request.user.is_platform_admin:
        return redirect('instructor_dashboard')
    return redirect('student_dashboard')


@login_required
def student_dashboard(request):
    if not request.user.is_student and not request.user.is_instructor:
        return redirect('home')
    from enrollments.models import Enrollment, LessonProgress
    from payments.models import Payment
    from lessons.models import Lesson, Module
    
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    purchases = Payment.objects.filter(user=request.user, status='completed')
    
    enrollment_data = []
    for enrollment in enrollments:
        last_progress = LessonProgress.objects.filter(enrollment=enrollment).order_by('-completed_at').first()
        if last_progress:
            first_lesson = last_progress.lesson
        else:
            first_module = enrollment.course.modules.first()
            first_lesson = first_module.lessons.first() if first_module else None
        
        enrollment_data.append({
            'enrollment': enrollment,
            'first_lesson': first_lesson
        })
    
    return render(request, 'users/student_dashboard.html', {
        'enrollment_data': enrollment_data,
        'purchases': purchases,
    })


@login_required
def instructor_dashboard(request):
    if not request.user.is_instructor and not request.user.is_platform_admin:
        return redirect('home')
    from courses.models import Course
    from enrollments.models import Enrollment
    courses = Course.objects.filter(instructor=request.user)
    total_students = Enrollment.objects.filter(course__instructor=request.user).count()
    total_revenue = sum(course.get_total_revenue() for course in courses)
    return render(request, 'users/instructor_dashboard.html', {
        'courses': courses,
        'total_students': total_students,
        'total_revenue': total_revenue,
    })


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})
