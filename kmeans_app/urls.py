from django.urls import path
from . import views

urlpatterns = [
    path('kmeans-clustring/', views.home, name='home'),
    path('results/', views.kmeans_view, name='results-kmeans'),
    path('kmeans/', views.kmeans_blog, name='kmeans-blog'),
]
