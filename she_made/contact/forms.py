from django import forms
from .models import Contact, Subscribe

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone',  'email', 'message']


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ['email']