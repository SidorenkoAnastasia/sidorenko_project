from django.shortcuts import render, redirect, get_object_or_404
from .models import Race, RaceRegistration, CommentRace
from django.http import HttpResponse
from django import forms
from .forms import RaceForm
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from .models import Race, Comment
from .forms import CommentForm, CustomUserCreationForm, CustomAuthenticationForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import logging


class RaceForm(forms.ModelForm):
    # Форма для создания и редактирования гонки.
    class Meta:
        model = Race
        fields = ['name', 'date', 'path', 'organizer']

@login_required
def race_list(request):
    # Представление для отображения списка гонок.
    query = request.GET.get('q')
    # ^^^ Получает параметр поиска из URL-строки
    if query:
        # Фильтрует гонки на основе заданного запроса.
        races = Race.objects.filter(
            Q(name__icontains=query) |  
            Q(date__icontains=query) |  
            Q(path__icontains=query)  
        )
    else:
        races = Race.objects.all()
    #^^^  Отображает все гонки, если запрос не задан
    return render(request, 'races/race_list.html', {'races': races})
    # Отправляет данные в шаблон


@login_required
def create_race(request):
    # Если форма валидна, сохраняет гонку и перенаправляет на список гонок.
    if request.method == 'POST':
        form = RaceForm(request.POST)
        # Создает форму с данными из POST-запроса
        if form.is_valid():
            form.save()
            #^^^ Сохраняет новую гонку в базе данных
            return redirect('race_list') 
            # ^^^Перенаправляет на список гонок
    else:
        form = RaceForm()
        #^^^ Создает пустую форму для отображения
    return render(request, 'races/create_race.html', {'form': form})
    #^^^ Отправляет форму в шаблон

def register(request):
    # Регистрация нового пользователя.
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        # Создает форму с данными из POST-запроса
        if form.is_valid():
            user = form.save()
            #^^^ Сохраняет нового пользователя в базе данных
            login(request, user) 
            #^^^ Выполняет вход пользователя в систему
            return redirect('home') 
            #^^^ Перенаправляет на главную страницу
    else:
        form = CustomUserCreationForm()
        # Создает пустую форму для отображения
    return render(request, 'races/register.html', {'form': form})
    # Отправляет форму в шаблон

def user_login(request):
    # Для входа пользователя в систему.
    # Выполняет вход и перенаправляет на главную страницу.
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            #^^^ Проверяет учетные данные пользователя
            if user is not None:
                login(request, user)
                #^^^ Выполняет вход пользователя в систему
                return redirect('home') 
    else:
        form = CustomAuthenticationForm()
    return render(request, 'races/login.html', {'form': form})
    # Отправляет форму в шаблон

def home(request):
    races = Race.objects.all()
    # ^^^ Получаем список гонок
    comments = Comment.objects.all()  
    # ^^^ Получаем все комментарии
    login_form = CustomAuthenticationForm(request, data=request.POST) if request.method == 'POST' else CustomAuthenticationForm()
    comment_form = CommentForm(request.POST or None)

    if request.method == 'POST':
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('race_list')

        # Обработка отправки комментария
        if comment_form.is_valid() and request.user.is_authenticated:
            comment = comment_form.save(commit=False)
            comment.author = request.user  
            # ^^^ Присваиваем автору текущего пользователя
            comment.save()
            return redirect('home')  
            # ^^^ Перенаправляем на страницу с главной

    return render(request, 'races/home.html', {
        'races': races,
        'login_form': login_form,
        'comment_form': comment_form,
        'comments': comments,  
        # ^^^ Передаем список комментариев в шаблон
    })

def race_detail(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    registered_ids = race.raceregistration_set.values_list('user_id', flat=True)
    context = {
        'race': race,
        'registered_ids': registered_ids 
         # Список регистраций
    }
    return render(request, 'races/race_detail.html', context)

@login_required
def register_for_race(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    registration, created = RaceRegistration.objects.get_or_create(user=request.user, race=race)
    if created:
        return redirect('race_detail', race_id=race.id) 
         # Перенаправляем на страницу гонки после регистрации
    else:
        return render(request, 'races/race_detail.html', {'race': race, 'error': 'Вы уже зарегистрированы на эту гонку.'})


@login_required
def add_comment(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            CommentRace.objects.create(race=race, user=request.user, text=comment_text)
            return HttpResponseRedirect(request.path)  
            # Перенаправляет обратно на страницу гонки
    return render(request, 'races/race_detail.html', {'race': race})


def unregister_from_race(request, race_id):
    if request.method == 'POST' and request.user.is_authenticated:
        race = get_object_or_404(Race, id=race_id)
        
        try:
            registration = RaceRegistration.objects.get(user=request.user, race=race)
            registration.delete()  
            # Удаляем регистрацию
        except RaceRegistration.DoesNotExist:
            pass  
        # Если регистрация не найдена, ничего не делаем

        return redirect('race_detail', race_id=race.id)  
        # Возвращаемся на страницу гонки

@login_required
def delete_race(request, race_id):
    race = get_object_or_404(Race, id=race_id)

    # Проверяем, является ли текущий пользователь создателем гонки
    if request.user == race.creator:
        race.delete()
    
    return redirect('race_list')