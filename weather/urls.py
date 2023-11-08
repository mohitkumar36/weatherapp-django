from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('', views.index, name='index'),
    path('check/<str:id>', views.check, name = 'check'),
    path('<str:review>/', views.review, name='review'),
    path('send', views.send, name='send'),
    
    path('logout', views.logout, name='logout')
]
