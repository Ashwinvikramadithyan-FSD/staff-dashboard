from django.db import models
from assettracker.models import Asset


class Profile(models.Model):
    ROLE_CHOICES = [
        ('staff', 'Staff'),
        ('hr', 'HR'),
    ]
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='staff')
    branch = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class BorrowRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    product = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='borrow_requests')
    requested_by = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    take_time = models.DateTimeField()
    bring_time = models.DateTimeField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.product.name}"