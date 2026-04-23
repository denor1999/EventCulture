from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponseNotFound, HttpResponseServerError
from .models import Event, Category, Tag

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

def server_error(request):
    return HttpResponseServerError("<h1>Ошибка 500</h1><p>Внутренняя ошибка сервера</p>")

def index(request):
    return render(request, 'index.html')

def category_view(request, cat_slug):    
    category = get_object_or_404(Category, slug=cat_slug)
    
    events = Event.published.filter(cat=category).order_by('-date')
    
    context = {
        'title': f'Категория: {category.name}',
        'events': events,
        'category': category,
        'events_count': events.count(),
    }
    return render(request, 'events.html', context)

def tag_view(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    events = Event.published.filter(tags=tag).order_by('-date')
    
    context = {
        'title': f'Тег: {tag.name}',
        'events': events,
        'tag': tag,
        'events_count': events.count(),
    }
    return render(request, 'events.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Успешный вход!')
        else:
            messages.error(request, 'Неверный логин или пароль!')
    
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно!')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    
    return redirect('home')

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы')
    return redirect('home')

def events_view(request):
    events = Event.published.all().order_by('-date')
    context = {
        'events': events,           
        'title': 'Мероприятия', 
        'events_count': events.count(), 
    }
    return render(request, 'events.html', context)

def event_detail(request, event_slug):
    event = get_object_or_404(Event, slug=event_slug)
    
    context = {
        'event': event,
        'title': event.title,
    }
    return render(request, 'webpages/event_deatail.html', context)

def venues_view(request):
    return render(request, 'venues.html')

def organizers_view(request):
    return render(request, 'organizers.html')

def about_view(request):
    return render(request, 'about.html')

def contacts_view(request):
    return render(request, 'contacts.html')