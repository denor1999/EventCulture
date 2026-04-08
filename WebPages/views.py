from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

EVENTS = [
    {
        'id': 1,
        'title': 'Симфонический оркестр: Шедевры классики',
        'venue': 'Казанская филармония',
        'date': '2024-12-15',
        'image_url': 'https://images.unsplash.com/photo-1506157786151-b8491531f063',
        'price' : 1500,
    },
    
    {
        'id': 2,
        'title': 'Ромео и Джульетта',
        'venue': 'Драматический театр',
        'date': '2024-12-20',
        'image_url': 'https://images.unsplash.com/photo-1588200980342-23b585c03e26',
        'price' : 2000,
    },
]

def index(request):
    context = {
        'events': EVENTS,
        'title': 'Главная страница',
        'cat_selected' : 0,
    }
    return render(request, 'index.html', context)

def category_view(request, cat_id):
    context = {
        'events': EVENTS,
        'title': f'Категория {cat_id}',
        'cat_selected': cat_id,
    }
    return render(request, 'index.html', context)

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
    return render(request, 'events.html')

def venues_view(request):
    return render(request, 'venues.html')

def organizers_view(request):
    return render(request, 'organizers.html')

def about_view(request):
    return render(request, 'about.html')

def contacts_view(request):
    return render(request, 'contacts.html')