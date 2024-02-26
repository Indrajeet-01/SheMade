from django.urls import path
from .views import ContactView, SubscribeView

urlpatterns = [
    path('create-contact/', ContactView.as_view(), name='create_contact'),
    path('subscribe-us', SubscribeView.as_view(), name="subscribe_us" )
    # Add other URLs as needed
]