from django.urls import path
from .views import register, login, logout, staff, delete_history_request, delete_request_product

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('staff/', staff, name='staff'),
    path('staff/delete-history/<int:id>/', delete_history_request, name='delete_history_request'),
    path('staff/delete-product/<int:id>/', delete_request_product, name='delete_request_product'),
]