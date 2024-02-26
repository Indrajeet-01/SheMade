from django.urls import path
from .views import CheckoutView

urlpatterns = [

    path('checkout-order/', CheckoutView.as_view(), name='checkout_order'),

    
]