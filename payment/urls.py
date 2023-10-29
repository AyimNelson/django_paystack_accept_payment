from django.urls import path, include

from .views import (
    ProductListView,
    ProductDetailView,
    SuccessPageView,
)


urlpatterns=[
    path('products/', ProductListView.as_view(), name='products'),
    path('product-detail/<uuid:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('success/', SuccessPageView.as_view(), name='success'),
]