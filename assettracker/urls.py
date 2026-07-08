from django.urls import path
from . import views

urlpatterns = [
    path('', views.hr_dashboard, name='hr_dashboard'),

    path('employees/<int:id>/update/', views.update_employee, name='update_employee'),
    path('employees/<int:id>/delete/', views.delete_employee, name='delete_employee'),

    path('assets/add/', views.add_asset, name='add_asset'),
    path('assets/<int:asset_id>/', views.asset_detail, name='asset_detail'),
    path('assets/<int:asset_id>/edit/', views.asset_edit, name='asset_edit'),
    path('assets/<int:asset_id>/delete/', views.asset_delete, name='asset_delete'),
    path('assets/<int:asset_id>/toggle-stock/', views.toggle_stock, name='toggle_stock'),

    path('requests/<int:id>/approve/', views.approve_request, name='approve_request'),
    path('requests/<int:id>/reject/', views.reject_request, name='reject_request'),
    path('requests/<int:id>/delete/', views.delete_borrow_request, name='delete_borrow_request'),

    path('asset-requests/', views.asset_request_history, name='asset_request_history'),
    path('asset-requests/new/', views.submit_asset_request, name='submit_asset_request'),
    path('asset-requests/<int:id>/approve/', views.approve_asset_request, name='approve_asset_request'),
    path('asset-requests/<int:id>/reject/', views.reject_asset_request, name='reject_asset_request'),
    path('asset-requests/<int:id>/delete/', views.delete_asset_request, name='delete_asset_request'),
]