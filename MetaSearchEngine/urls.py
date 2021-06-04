from django.urls import path
from MetaSearchEngine import views

app_name='MetaSearchEngine'

urlpatterns = [
    path('search/', views.results_list, name='search'),
    path('', views.home, name='home'),

]