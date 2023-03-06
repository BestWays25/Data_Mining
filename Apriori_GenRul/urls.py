from django import urls
from django.urls import path
from .views import apriori_results, apriori_results_csv, home_apriori

urlpatterns = [
    path('', home_apriori, name='home_apriori'),
    path('apriori/', apriori_results, name='apriori_results'),
    path('apriori_csv/', apriori_results_csv, name='apriori_results_csv'),
]
