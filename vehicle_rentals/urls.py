from django.urls import path
from . import views

app_name = 'vehicle_rentals'

urlpatterns = [
    path('cars/', views.carrent_page, name='carrent'),
    path('car-details/', views.car_details_page, name='car_details'),
    path('bikes/', views.bikerent_page, name='bikerent'),
    path('bike-details/', views.bike_details_page, name='bike_details'),
    path('jawa/', views.jawa_page, name='jawa'),
    path('manage-categories/', views.manage_categories_page, name='manage_categories'),
    path('api/delete-category/', views.delete_category_api, name='api_delete_category'),
]
