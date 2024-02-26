from django.urls import path
from .views import ContactView

urlpatterns = [
    path('create-contact/', ContactView.as_view(), name='create_contact'),
    # Add other URLs as needed
]