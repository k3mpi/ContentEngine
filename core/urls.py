from django.conf.urls.static import static
from django.urls import path

from ContentEngine import settings
from . import views

urlpatterns = [

    path('', views.dashboard, name='dashboard'),

    path('settings/', views.settings, name='settings'),
    path('overview/', views.overview, name='overview'),

    path('ideas/', views.list_ideas, name='list_ideas'),
    path('ideas/create/', views.create_idea, name='create_idea'),
    path('ideas/<int:pk>/edit/', views.update_idea, name='update_idea'),
    path('ideas/<int:pk>/delete/', views.delete_idea, name='delete_idea'),

    path('ideas/get_ideas/', views.get_ideas, name='get_ideas'),


    path('posts/', views.list_posts, name='list_posts'),
    path('posts/<int:post_id>/', views.view_post, name='view_post'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<int:pk>/edit/', views.update_post, name='update_post'),
    path('posts/<int:pk>/delete/', views.delete_post, name='delete_post'),

    path('posts/publish/', views.list_publish_posts, name='list_publish_posts'),
    path('posts/publications/<int:post_id>/', views.view_post_publications, name='view_post_publications'),
    path('posts/publish/youtube/<int:post_id>/', views.publish_youtube_post, name='publish_youtube_post'),
    path('posts/publish/pinterest/<int:post_id>/', views.publish_pinterest_post, name='publish_pinterest_post'),
    path('posts/publish/facebook/<int:post_id>/', views.publish_facebook_post, name='publish_facebook_post'),
    path('posts/publish/instagram/<int:post_id>/', views.publish_instagram_post, name='publish_instagram_post'),

    path('posts/<int:pk>/create_audio/', views.create_audio, name='create_audio'),
    path('posts/<int:pk>/create_article/', views.create_article, name='create_article'),
    path('posts/<int:pk>/create_seo/', views.create_seo, name='create_seo'),
    path('posts/<int:pk>/create_ig_post/', views.create_ig_post, name='create_ig_post'),
    path('posts/<int:pk>/create_ig_video/', views.create_ig_video, name='create_ig_video'),
    path('posts/<int:pk>/create_long_video/', views.create_long_video, name='create_long_video'),



    path('slides/', views.list_slides, name='list_slides'),


    path('topics/', views.list_topics, name='list_topics'),
    path('topics/create/', views.create_topic, name='create_topic'),
    path('topics/<int:pk>/edit/', views.update_topic, name='update_topic'),
    path('topics/<int:pk>/delete/', views.delete_topic, name='delete_topic'),

    path('reasons/', views.list_reasons, name='list_reasons'),
    path('reasons/create/', views.create_reason, name='create_reason'),
    path('reasons/<int:pk>/edit/', views.update_reason, name='update_reason'),
    path('reasons/<int:pk>/delete/', views.delete_reason, name='delete_reason'),

    path('projects/', views.list_projects, name='list_projects'),
    path('projects/<int:project_id>/', views.view_project, name='view_project'),
    path('project/create/', views.create_project, name='create_project'),
    path('project/<int:pk>/edit/', views.update_project, name='update_project'),
    path('project/<int:pk>/delete/', views.delete_project, name='delete_project'),

    path('accounts/', views.list_accounts, name='list_accounts'),

    path('accounts/instagram/create/', views.create_instagram_account, name='create_instagram_account'),
    path('accounts/instagram/<int:pk>/edit/', views.update_instagram_account, name='update_instagram_account'),
    path('accounts/instagram/<int:pk>/delete/', views.delete_instagram_account, name='delete_instagram_account'),


    path('accounts/facebook/create/', views.create_facebook_account, name='create_facebook_account'),
    path('accounts/facebook/<int:pk>/edit/', views.update_facebook_account, name='update_facebook_account'),
    path('accounts/facebook/<int:pk>/delete/', views.delete_facebook_account, name='delete_facebook_account'),

    path('accounts/pinterest/create/', views.create_pinterest_account, name='create_pinterest_account'),
    path('accounts/pinterest/<int:pk>/edit/', views.update_pinterest_account, name='update_pinterest_account'),
    path('accounts/pinterest/<int:pk>/delete/', views.delete_pinterest_account, name='delete_pinterest_account'),


    path('accounts/youtube/create/', views.create_youtube_account, name='create_youtube_account'),
    path('accounts/youtube/<int:pk>/edit/', views.update_youtube_account, name='update_youtube_account'),
    path('accounts/youtube/<int:pk>/delete/', views.delete_youtube_account, name='delete_youtube_account'),




    path('links/', views.list_links, name='list_links'),
    path('links/create/', views.create_link, name='create_link'),
    path('links/<int:pk>/edit/', views.update_link, name='update_link'),
    path('links/<int:pk>/delete/', views.delete_link, name='delete_link'),

]
