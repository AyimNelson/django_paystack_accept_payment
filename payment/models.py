from django.db import models
from django.conf import settings
from authentication.models import User
from django.urls import reverse
import uuid
from datetime import datetime, timedelta
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    product_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=100, null=True, blank=False)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=100)
    description = models.TextField(max_length=500, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"pk": self.product_id})


class Payment(models.Model):
    payment_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_paid = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=100)
    reference = models.CharField(max_length=100, null=False)
        

    def __str__(self):
        return f"{self.user.username}'s {self.product.name} Payment"
    
    def get_absolute_url(self):
        return reverse("payment-detail", kwargs={"pk": self.payment_id})
    
    class Meta:
        ordering = ['-date_paid']