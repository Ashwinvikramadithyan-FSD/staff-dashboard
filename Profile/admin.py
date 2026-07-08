from django.contrib import admin
from .models import Profile, BorrowRequest

admin.site.register(Profile)
admin.site.register(BorrowRequest)