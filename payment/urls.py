from django.urls import path
from . import views

urlpatterns = [
    path('initialize/', views.initialize_payment, name='initialize_payment'),
    path('verify/', views.verify_payment, name='verify_payment'),
]