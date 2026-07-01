from django.contrib import admin
from .models import Product, BorrowRequest  # Import your models explicitly

admin.site.register(Product)
admin.site.register(BorrowRequest)