from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import ContactForm

class ContactView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        try:
            form_data = self.request.data 
            form = ContactForm(form_data)
            if form.is_valid():
                contact_instance = form.save()

                return Response({'success': 'Contact send successfully'})
            else:
                # Return a response indicating that the form is not valid
                return Response({'error': 'Form validation failed'})
        except Exception as e:
            return Response({'error': f'Failed to send contact. Error: {str(e)}'})