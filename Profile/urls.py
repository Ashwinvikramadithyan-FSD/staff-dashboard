from django.urls import path
from .views import register, login, logout, staff, delete_profile, update, delete_history_request
from .views import register, login, logout, staff, delete_profile, update, delete_history_request, delete_request_product

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('staff/', staff, name='staff'),
    path('delete/<int:id>/', delete_profile, name='delete_profile'),
    path('update/<int:id>/', update, name='update_profile'),
    path('delete-history/<int:id>/', delete_history_request, name='delete_history_request'),
    path('delete-request-product/<int:id>/', delete_request_product, name='delete_request_product'),
]
