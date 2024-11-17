from django.urls import path

from django.contrib import admin
from django.urls import path, include

from app import views

urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('user_registration', views.user_registration, name='user_registration'),
    path('login', views.user_login, name='login'),
    path('posts/', views.post_list, name='post-list'),
    path('create_post/', views.create_post, name='create-post'),
    path('analyze_post/', views.analyze_post, name='analyze-post'),
    path('title_generator', views.title_generator, name='title_generator'),
    path('posts/<int:post_id>/edit', views.edit_post, name='edit_post'),
    
    path('match/', views.partnership_match, name='partnership_match'),
    path('match/status/<int:pk>/', views.partnership_status, name='partnership_status'),
    path('resources/upload/', views.resource_upload, name='resource_upload'),
    path('resources/', views.resource_list, name='resource_list'),
    path('resources/<str:category>/', views.resource_by_category, name='resource_by_category'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/upcoming/', views.upcoming_events, name='upcoming_events'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('analytics/', views.predictive_analytics, name='predictive_analytics'),
]