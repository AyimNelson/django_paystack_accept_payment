from django.contrib import admin

# Register your models here.
from .models import Product, Payment

admin.site.register(Product)
admin.site.register(Payment)