from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'role',
        'branch'
    )

    search_fields = (
        'first_name',
        'last_name',
        'email'
    )

    list_filter = (
        'role',
        'branch'
    )# Register your models here.
