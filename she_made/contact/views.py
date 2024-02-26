from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import ContactForm, SubscribeForm
from django.contrib import messages
from django.shortcuts import render, redirect

class ContactView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        try:
            form_data = self.request.data 
            form = ContactForm(form_data)
            if form.is_valid():
                contact_instance = form.save()
                messages.success(request, "We will contact you ASAP.")

                return render(request, 'contact_us.html', {'messages': messages.get_messages(request)})
            else:
                messages.error(request, 'Please fill the correct details.')
                # Return a response indicating that the form is not valid
                return render(request, 'contact_us.html', {'messages': messages.get_messages(request)})
        except Exception as e:
            return Response({'error': f'Failed to send contact. Error: {str(e)}'})
        

class SubscribeView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        try:
            subscribe_email = self.request.data
            
            subscribe_form = SubscribeForm(subscribe_email)
            if subscribe_form.is_valid():
                subscribe_instance = subscribe_form.save()
                messages.success(request, 'Now, You are subscribed to us.')
                return render(request, 'base.html', {'messages': messages.get_messages(request)} )
            else:
                messages.error(request, 'Please fill the correct details.')
                return render(request, 'base.html', {'messages': messages.get_messages(request)} )

        except Exception as e:
            return Response({'error': f'Failed to subscribe. Error: {str(e)}'})
