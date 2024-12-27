from django.shortcuts import render, redirect, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from datetime import datetime
from .models import *
from .forms import *


def index(request):
    courses = Course.objects.all()
    lessons = Lessons.objects.all()

    context = {
        'courses': courses,
        'lessons': lessons,
        'current_year': datetime.now().year
    }

    return render(request, 'index.html', context)


def courses(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = Lessons.objects.filter(course_id=course_id)

    context = {
        'courses': [course],
        'lessons': lessons,
        'current_year': datetime.now().year
    }

    return render(request, 'index.html', context)


def lessons(request, lesson_id):
    lesson = get_object_or_404(Lessons, id=lesson_id)

    context = {
        'lesson': lesson,
        'current_year': datetime.now().year
    }

    return render(request, 'detail.html', context)


def addCourse(request: WSGIRequest):
    if request.method == 'POST':
        form = CourseForms(data=request.POST, files=request.FILES)
        if form.is_valid():
            if Course.objects.filter(name=form.cleaned_data['name']).exists():
                messages.success(request, "Ma'lumot saqlanmadi. Bunday kurs allaqachon mavjud!")
            else:
                Course.objects.create(**form.cleaned_data)
                messages.success(request, "Ma'lumot muvaffaqiyatli saqlandi!")
            return redirect('addCourse')

    context = {
        'forms': CourseForms()
    }
    return render(request, 'addCourse.html', context)


def addLesson(request: WSGIRequest):
    if request.method == 'POST':
        form = LessonForms(data=request.POST, files=request.FILES)
        if form.is_valid():
            if Lessons.objects.filter(name=form.cleaned_data['name'], course=form.cleaned_data['course']).exists():
                messages.success(request, "Ma'lumot saqlanmadi.Bunday vazifa allaqachon mavjud!")
            else:
                Lessons.objects.create(**form.cleaned_data)
                messages.success(request, "Ma'lumotlar muvaffaqiyatli saqlandi!")
            return redirect('addLesson')

    context = {
        'forms': LessonForms(),

    }
    return render(request, 'addLesson.html', context)

def updateCourse(request: WSGIRequest, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == 'POST':
        form = CourseForms(data=request.POST, files=request.FILES)

        if form.is_valid():
            if Course.objects.filter(name=form.cleaned_data.get('name')).exists():
                messages.error(request, "Ma'lumot o'zgartirilmadi. Bunday ma'lumot allaqachon qo'shilgan!")
                return redirect('home')

            course.name = form.cleaned_data.get('name')
            course.save()

            messages.success(request, "Ma'lumot muvaffaqiyatli o'zgartirildi.")
            return redirect('home')

    forms = CourseForms(initial={
        'name': course.name
    })

    context = {
        'forms': forms,
        'current_year': datetime.now().year
    }

    return render(request, 'addLesson.html', context)


def deleteCourse(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course.delete()
    messages.success(request, "Ma'lumot muvaffaqiyatli o'chirildi.")
    return redirect('home')


def updateLesson(request: WSGIRequest, lesson_id):
    lesson = get_object_or_404(Lessons, pk=lesson_id)

    if request.method == 'POST':
        form = LessonForms(data=request.POST, files=request.FILES)
        if form.is_valid():
            if Lessons.objects.filter(name=form.cleaned_data.get('name')).exists():
                messages.error(request, "Ma'lumot o'zgartirilmadi. Bunday ma'lumot allaqachon qo'shilgan!")
                return redirect('lessons_detail', lesson_id=lesson_id)

            lesson.name = form.cleaned_data.get('name')
            lesson.homework = form.cleaned_data.get('homework')
            lesson.deadline = form.cleaned_data.get('deadline') if form.cleaned_data.get(
                'deadline') else lesson.deadline
            lesson.course = form.cleaned_data.get('course')
            lesson.save()

            messages.success(request, "Ma'lumot muvaffaqiyatli o'zgartirildi.")
            return redirect('lessons_detail', lesson_id=lesson_id)

    forms = LessonForms(initial={
        'name': lesson.name,
        'homework': lesson.homework,
        'deadline': lesson.deadline,
        'course': lesson.course
    })

    context = {
        'forms': forms,
        'current_year': datetime.now().year
    }

    return render(request, 'addLesson.html', context)


def deleteLesson(request, lesson_id):
    lesson = get_object_or_404(Lessons, pk=lesson_id)
    lesson.delete()
    messages.success(request, "Ma'lumot muvaffaqiyatli o'chirildi.")
    return redirect('home')


def register(request: WSGIRequest):
    if request.method == 'POST':
        form = Register(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            confirm_password = form.cleaned_data.get('confirm_password')
            if password == confirm_password:

                if User.objects.filter(username=username).exists():
                    messages.error(request,
                                   "Foydalanuvchi nomi  ro'yxatdan mavjud. Iltimos boshqa qiymat kiriting!")
                else:
                    User.objects.create_user(username, email, password)

                    messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz 😁😁😁 ")
                    return redirect('login')

            else:
                messages.error(request,
                               "Parollar bir-biriga mos kelmayapti. Iltimos, qayta urinib koring!")

    context = {
        'forms': Register(),
        'current_year': datetime.now().year
    }

    return render(request, 'auth/sign-up.html', context)


def loginPage(request: WSGIRequest):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Tizimga muvaffaqiyatli kirdingiz 😊😊😊 ")
                return redirect('home')
            else:
                messages.error(request,
                               "Kiritilgan foydalanuvchi nomi yoki parol noto‘g‘ri. Iltimos, qayta tekshirib ko‘ring.")

    context = {
        'forms': LoginForm(),
        'current_year': datetime.now().year
    }

    return render(request, 'auth/login.html', context)


def logoutPage(request: WSGIRequest):
    logout(request)
    messages.success(request, "Tizimdan muvaffaqiyatli chiqdingiz!")
    return redirect('home')
