from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('inscription/', views.register, name='register'),
    path('messages/', views.conversation_list, name='conversation_list'),
    path('messages/nouveau/', views.new_conversation, name='new_conversation'),
    path('messages/<int:pk>/', views.conversation_detail, name='conversation_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
