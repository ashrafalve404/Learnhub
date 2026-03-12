from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Course, Category, Wishlist
from .forms import CourseForm, CourseSearchForm


def course_list(request):
    courses = Course.objects.filter(is_published=True, is_approved=True).select_related('instructor', 'category')
    categories = Category.objects.all()
    
    form = CourseSearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        level = form.cleaned_data.get('level')
        
        if query:
            courses = courses.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query)
            )
        if category:
            courses = courses.filter(category=category)
        if level:
            courses = courses.filter(level=level)
    
    paginator = Paginator(courses, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'courses/course_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'form': form,
    })


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    from lessons.models import Module
    modules = Module.objects.filter(course=course).prefetch_related('lessons')
    from reviews.models import Review
    reviews = Review.objects.filter(course=course).select_related('user')[:10]
    
    related_courses = Course.objects.filter(
        category=course.category
    ).exclude(id=course.id).filter(is_published=True)[:4]
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'modules': modules,
        'reviews': reviews,
        'related_courses': related_courses,
    })


def category_courses(request, slug):
    category = get_object_or_404(Category, slug=slug)
    courses = Course.objects.filter(
        category=category,
        is_published=True,
        is_approved=True
    ).select_related('instructor')
    
    paginator = Paginator(courses, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'courses/category_courses.html', {
        'category': category,
        'page_obj': page_obj,
    })


@login_required
def instructor_course_list(request):
    if not request.user.is_instructor and not request.user.is_platform_admin:
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('home')
    
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'courses/instructor_course_list.html', {'courses': courses})


@login_required
def instructor_course_create(request):
    if not request.user.is_instructor and not request.user.is_platform_admin:
        messages.error(request, 'You are not authorized to create courses.')
        return redirect('home')
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('instructor_course_edit', course.id)
    else:
        form = CourseForm()
    return render(request, 'courses/instructor_course_form.html', {'form': form, 'course': None})


@login_required
def instructor_course_edit(request, course_id):
    if not request.user.is_instructor and not request.user.is_platform_admin:
        messages.error(request, 'You are not authorized to edit courses.')
        return redirect('home')
    
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('instructor_course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/instructor_course_form.html', {'form': form, 'course': course})


@login_required
def instructor_course_delete(request, course_id):
    if not request.user.is_instructor and not request.user.is_platform_admin:
        messages.error(request, 'You are not authorized to delete courses.')
        return redirect('home')
    
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    course.delete()
    messages.success(request, 'Course deleted successfully!')
    return redirect('instructor_course_list')


@login_required
def toggle_wishlist(request):
    from django.http import JsonResponse
    from django.views.decorators.csrf import csrf_exempt
    from django.views.decorators.http import require_POST
    import json
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            course_id = data.get('course_id')
            course = get_object_or_404(Course, id=course_id)
            
            wishlist_item, created = Wishlist.objects.get_or_create(
                user=request.user,
                course=course
            )
            
            if not created:
                wishlist_item.delete()
                return JsonResponse({'added': False, 'message': 'Removed from wishlist'})
            
            return JsonResponse({'added': True, 'message': 'Added to wishlist'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
