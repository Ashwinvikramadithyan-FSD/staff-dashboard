from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):

    phone_number = models.CharField( max_length=15, blank=True, null=True )

    dob = models.DateField( blank=True,null=True )

    role = models.CharField(
        max_length=10,
        choices=[
            ('HR','HR'),
            ('STAFF','STAFF')
        ],
        default='STAFF'
    )

    branch = models.CharField( max_length=100,blank=True, null=True )

    groups = models.ManyToManyField(
        Group,
        related_name='assettracker_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='assettracker_user_permissions_set',
        blank=True,
    )

class Asset(models.Model):
    name = models.CharField(max_length=255)

    description = models.TextField( blank=True,  null=True )

    image = models.ImageField( upload_to="assets/",blank=True, null=True )

    is_in_stock = models.BooleanField( default=True  )

    def __str__(self):
        return self.name
    
class Employee(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField()

    phone = models.CharField(max_length=10)

    branch = models.CharField(max_length=100)

    role = models.CharField(max_length=20)

    created_at = models.DateTimeField(auto_now_add=True)

class AssetRequest(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    employee_name = models.CharField(
        max_length=150
    )

    product = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name='asset_requests'
    )

    take_time = models.DateTimeField()

    return_time = models.DateTimeField()

    submitted_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING",
    )

    rejection_reason = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.employee_name} - {self.product.name}"
    
class InventoryItem(models.Model):

    name = models.CharField(
        max_length=100
    )

    image = models.ImageField(
        upload_to='inventory/'
    )

    quantity = models.IntegerField()

    status = models.CharField(
        max_length=20,
        choices=[
            ('IN_STOCK','In Stock'),
            ('OUT_OF_STOCK','Out Of Stock')
        ]
    )

    assigned_to = models.CharField(
        max_length=100,
        blank=True
    )