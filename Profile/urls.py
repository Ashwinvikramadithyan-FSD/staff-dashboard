from django.urls import path
from .views import register, login, logout, staff

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('staff/', staff, name='staff'),
    # Removed delete_history_request and delete_request_product 
    # as they are no longer supported in views.py
]