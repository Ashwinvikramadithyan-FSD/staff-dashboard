from django.urls import path
from . import views

urlpatterns = [
    path('', views.hr_dashboard, name='hr_dashboard'),
    path('delete-product/<int:id>/', views.delete_product, name='delete_product'),
    path('delete-request/<int:id>/', views.delete_borrow_request, name='delete_borrow_request'),
    path('update-status/<int:id>/', views.update_status, name='update_status'),
    path('status/', views.hr_status, name='hr_status'),
]