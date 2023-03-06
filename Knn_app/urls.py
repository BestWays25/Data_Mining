from django.urls import path
from . import views
# app_name = 'Knn_app'
urlpatterns = [
    path('knn/', views.knn_blog, name='knn_blog'),
    path('knn-algo/', views.index, name='knn-algo'),
    path('results/', views.results, name='results'),
]
