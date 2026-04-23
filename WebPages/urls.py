from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('category/<slug:cat_slug>/', views.category_view, name='category'),
    path('events/', views.events_view, name='events'),
    path('event/<slug:event_slug>/', views.event_detail, name='event_detail'),
    path('tag/<slug:tag_slug>/', views.tag_view, name='tag'),
    path('venues/', views.venues_view, name='venues'),
    path('organizers/', views.organizers_view, name='organizers'),
    path('about/', views.about_view, name='about'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('Error404/', views.page_not_found),
    path('Error500/', views.server_error),

]

handler404 = views.page_not_found
handler500 = views.server_error