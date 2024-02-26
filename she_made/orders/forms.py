from django import forms
from .models import Address, PaymentDetails

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'phone', 'email', 'state', 'district', 'pincode', 'street']

class PaymentDetailsForm(forms.ModelForm):
    class Meta:
        model = PaymentDetails
        fields = ['card_number', 'expiry_month', 'expiry_year', 'cvc', 'card_holder_name', 'upi_id']
