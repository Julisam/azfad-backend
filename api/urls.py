from django.urls import path
from .views import CourseListView
from .auth_views import register, login

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('auth/register/', register, name='register'),
    path('auth/login/', login, name='login'),
]