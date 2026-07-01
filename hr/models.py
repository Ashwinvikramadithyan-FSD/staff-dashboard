from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    made_in = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="products/")
    def __str__(self):
        return self.name

class BorrowRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    requested_by = models.ForeignKey(
        'Profile.Profile',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='hr_borrow_requests'
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    take_time = models.DateTimeField()
    bring_time = models.DateTimeField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.product.name}"