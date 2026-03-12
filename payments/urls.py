from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<int:course_id>/', views.payment_checkout, name='payment_checkout'),
    path('initiate/<int:course_id>/', views.initiate_payment, name='initiate_payment'),
    path('history/', views.payment_history, name='payment_history'),
    path('success/<str:transaction_id>/', views.payment_success, name='payment_success'),
    path('failed/', views.payment_failed, name='payment_failed'),
]
