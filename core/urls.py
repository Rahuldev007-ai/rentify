from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('home/', views.home_page, name='home_alias'),
    path('aboutus/', views.aboutus_page, name='aboutus'),
    path('gallery/', views.gallery_page, name='gallery'),
    path('feedback/', views.feedback_page, name='feedback'),
    path('api/search-suggestions/', views.search_suggestions_api, name='search_suggestions'),
]
