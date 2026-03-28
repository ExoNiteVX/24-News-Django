from django.urls import path

from .views import index, about, contact, technology, business, register, login, events, forums, members, single, science, groups, politics, blog

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('technology/', technology, name='technology'),
    path('business/', business, name='business'),
    path('events/', events, name='events'),
    path('forums/', forums, name='forums'),
    path('members/', members, name='members'),
    path('single/', single, name='single'),
    path('science/', science, name='science'),
    path('groups/', groups, name='groups'),
    path('politics/', politics, name='politics'),
    path('blog/',blog, name='blog'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
]