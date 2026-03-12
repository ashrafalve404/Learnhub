from django.urls import path
from . import views

urlpatterns = [
    path('my-certificates/', views.my_certificates, name='my_certificates'),
    path('<str:certificate_id>/', views.certificate_detail, name='certificate_detail'),
]
