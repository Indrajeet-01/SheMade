from django.urls import path
from .views import ProductItemListCreateView, ProductItemDetailView

urlpatterns = [
    path('products/', ProductItemListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductItemDetailView.as_view(), name='product-detail'),
]