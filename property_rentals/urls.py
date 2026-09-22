from django.urls import path
from . import views

app_name = 'property_rentals'

urlpatterns = [
    path('halls/', views.hallrent_page, name='hallrent'),
    path('api/halls/live-list/', views.client_live_halls_api, name='api_client_live_halls'),
    path('api/halls/submit-inquiry/', views.create_hall_inquiry_api, name='api_submit_hall_inquiry'),
    path('hall-details/', views.hall_details_page, name='hall_details'),
    path('hall-inquiry/', views.hall_inquiry_page, name='hall_inquiry'),
    path('houses/', views.houserent_page, name='houserent'),
    path('api/houses/live-list/', views.client_live_houses_api, name='api_client_live_houses'),
    path('api/houses/submit-inquiry/', views.create_house_inquiry_api, name='api_submit_house_inquiry'),
    path('house-details/', views.house_details_page, name='house_details'),
    path('offices/', views.officerent_page, name='officerent'),
    path('api/offices/live-list/', views.client_live_offices_api, name='api_client_live_offices'),
    path('api/offices/submit-inquiry/', views.create_office_inquiry_api, name='api_submit_office_inquiry'),
    path('office-details/', views.office_details_page, name='office_details'),
]
