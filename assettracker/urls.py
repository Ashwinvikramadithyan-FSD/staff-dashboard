from django.urls import path
from . import views

urlpatterns = [

    # Authentication
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboards
    path('hr-dashboard/', views.hr_dashboard, name='hr_dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),

    # Employee
    path('employees/', views.employee_profile, name='employee_profile'),
    path('employee/update/<int:id>/', views.update_employee, name='update_employee'),
    path('employee/delete/<int:id>/', views.delete_employee, name='delete_employee'),

    # Asset Pages
    path('assets/', views.assets_page, name='assets_page'),
    path('asset/add/', views.add_asset, name='add_asset'),

    # Asset CRUD
    path('asset/<int:asset_id>/', views.asset_detail, name='asset_detail'),
    path('asset/<int:asset_id>/edit/', views.asset_edit, name='asset_edit'),
    path('asset/<int:asset_id>/delete/', views.asset_delete, name='asset_delete'),
    path('asset/<int:asset_id>/toggle/', views.toggle_stock, name='toggle_stock'),

    # Existing Update/Delete Pages (keep these for now)
    path('asset/update/<int:id>/', views.update_asset, name='update_asset'),
    path('asset/delete/<int:id>/', views.delete_asset, name='delete_asset'),

    # Asset Requests
    path('request-asset/', views.request_asset, name='request_asset'),
    path('approve/<int:id>/', views.approve_request, name='approve_request'),
    path('reject/<int:id>/', views.reject_request, name='reject_request'),

    # Other Pages
    path('requests/', views.submitted_requests, name='submitted_requests'),
    path('history/', views.history_page, name='history_page'),
    path('inventory/', views.inventory_page, name='inventory_page'),
]