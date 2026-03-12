from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Module, Lesson
from courses.models import Course
from .forms import ModuleForm, LessonForm


@login_required
def lesson_player(request, course_slug, lesson_id):
    course = get_object_or_404(Course, slug=course_slug)
    
    from enrollments.models import Enrollment
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)
    
    if not lesson.is_preview and not enrollment:
        messages.error(request, 'You must enroll in this course to view this lesson.')
        return redirect('course_detail', slug=course_slug)
    
    modules = Module.objects.filter(course=course).prefetch_related('lessons')
    
    all_lessons = []
    for module in modules:
        for l in module.lessons.all():
            all_lessons.append(l)
    
    current_index = all_lessons.index(lesson)
    prev_lesson = all_lessons[current_index - 1] if current_index > 0 else None
    next_lesson = all_lessons[current_index + 1] if current_index < len(all_lessons) - 1 else None
    
    completed_lessons = []
    if enrollment:
        from enrollments.models import LessonProgress
        completed_lessons = LessonProgress.objects.filter(
            enrollment=enrollment
        ).values_list('lesson_id', flat=True)
    
    return render(request, 'lessons/lesson_player.html', {
        'course': course,
        'lesson': lesson,
        'modules': modules,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'completed_lessons': completed_lessons,
        'enrollment': enrollment,
    })


@login_required
def mark_lesson_complete(request, lesson_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.module.course
    
    from enrollments.models import Enrollment, LessonProgress
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    
    if not enrollment:
        return JsonResponse({'error': 'Not enrolled'}, status=403)
    
    progress, created = LessonProgress.objects.get_or_create(
        enrollment=enrollment,
        lesson=lesson
    )
    
    total_lessons = Lesson.objects.filter(module__course=course).count()
    completed_count = LessonProgress.objects.filter(enrollment=enrollment).count()
    progress_percentage = (completed_count / total_lessons * 100) if total_lessons > 0 else 0
    
    enrollment.progress_percentage = progress_percentage
    enrollment.save()
    
    if progress_percentage >= 100:
        enrollment.completed = True
        enrollment.save()
    
    return JsonResponse({
        'success': True,
        'progress_percentage': progress_percentage,
        'completed': enrollment.completed
    })


@login_required
def instructor_module_create(request, course_id):
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    
    if request.method == 'POST':
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            messages.success(request, 'Module created successfully!')
            return redirect('instructor_course_edit', course_id)
    else:
        form = ModuleForm()
    
    return render(request, 'lessons/module_form.html', {
        'form': form,
        'course': course,
        'module': None
    })


@login_required
def instructor_module_edit(request, module_id):
    module = get_object_or_404(Module, id=module_id, course__instructor=request.user)
    
    if request.method == 'POST':
        form = ModuleForm(request.POST, instance=module)
        if form.is_valid():
            form.save()
            messages.success(request, 'Module updated successfully!')
            return redirect('instructor_course_edit', module.course.id)
    else:
        form = ModuleForm(instance=module)
    
    return render(request, 'lessons/module_form.html', {
        'form': form,
        'course': module.course,
        'module': module
    })


@login_required
def instructor_lesson_create(request, module_id):
    module = get_object_or_404(Module, id=module_id, course__instructor=request.user)
    
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()
            messages.success(request, 'Lesson created successfully!')
            return redirect('instructor_course_edit', module.course.id)
    else:
        form = LessonForm()
    
    return render(request, 'lessons/lesson_form.html', {
        'form': form,
        'module': module,
        'lesson': None
    })


@login_required
def instructor_lesson_edit(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course__instructor=request.user)
    
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lesson updated successfully!')
            return redirect('instructor_course_edit', lesson.module.course.id)
    else:
        form = LessonForm(instance=lesson)
    
    return render(request, 'lessons/lesson_form.html', {
        'form': form,
        'module': lesson.module,
        'lesson': lesson
    })


@login_required
def instructor_lesson_delete(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course__instructor=request.user)
    course_id = lesson.module.course.id
    lesson.delete()
    messages.success(request, 'Lesson deleted successfully!')
    return redirect('instructor_course_edit', course_id)
