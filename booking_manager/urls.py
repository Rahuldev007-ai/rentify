from django.urls import path
from . import views

app_name = 'booking_manager'

urlpatterns = [
    path('payment/', views.payment_page, name='payment'),
    path('api/process-payment/', views.process_payment_api, name='process_payment_api'),
    path('api/cancel/', views.cancel_booking_api, name='cancel_booking_api'),
    path('api/pay-extra-fee/', views.pay_extra_fee_api, name='pay_extra_fee_api'),
    path('api/submit-feedback/', views.submit_booking_feedback_api, name='submit_booking_feedback_api'),
    path('confirmation/', views.confirmation_page, name='confirmation'),
    path('my-bookings/', views.my_bookings_page, name='my_bookings'),
    path('my-hall-inquiries/', views.my_hall_inquiries_page, name='my_hall_inquiries'),
    path('my-house-inquiries/', views.my_house_inquiries_page, name='my_house_inquiries'),
    path('my-office-inquiries/', views.my_office_inquiries_page, name='my_office_inquiries'),
]

