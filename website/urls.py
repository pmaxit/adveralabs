"""Website URL Configuration"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('calculate-roi/', views.calculate_roi, name='calculate_roi'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:post_id>/', views.blog_post, name='blog_post'),
    path('careers/', views.careers, name='careers'),
    path('contact/', views.contact, name='contact'),
    path('documentation/', views.documentation, name='documentation'),
    path('api/', views.api_docs, name='api_docs'),
    path('support/', views.support, name='support'),
    path('privacy/', views.privacy, name='privacy'),
]

