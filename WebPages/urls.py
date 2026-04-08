from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('category/<int:cat_id>/', views.category_view, name='category'),
    path('events/', views.events_view, name='events'),
    path('venues/', views.venues_view, name='venues'),
    path('organizers/', views.organizers_view, name='organizers'),
    path('about/', views.about_view, name='about'),
    path('contacts/', views.contacts_view, name='contacts'),


]