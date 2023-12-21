from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard, name='dashboard'),

    path('settings/', views.settings, name='settings'),
    path('overview/', views.overview, name='overview'),

    path('ideas/', views.list_ideas, name='list_ideas'),
    path('ideas/create/', views.create_idea, name='create_idea'),
    path('ideas/<int:pk>/edit/', views.update_idea, name='update_idea'),
    path('ideas/<int:pk>/delete/', views.delete_idea, name='delete_idea'),

    path('posts/', views.list_posts, name='list_posts'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:pk>/edit/', views.update_post, name='update_post'),
    path('posts/<int:pk>/delete/', views.delete_post, name='delete_post'),

    path('topics/', views.list_topics, name='list_topics'),
    path('topics/create/', views.create_topic, name='create_topic'),
    path('topics/<int:pk>/edit/', views.update_topic, name='update_topic'),
    path('topics/<int:pk>/delete/', views.delete_topic, name='delete_topic'),

    path('reasons/', views.list_reasons, name='list_reasons'),
    path('reasons/create/', views.create_reason, name='create_reason'),
    path('reasons/<int:pk>/edit/', views.update_reason, name='update_reason'),
    path('reasons/<int:pk>/delete/', views.delete_reason, name='delete_reason'),


]
