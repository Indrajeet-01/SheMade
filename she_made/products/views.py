from rest_framework import permissions
from rest_framework import generics
from .models import ProductItem, Image
from .serializers import ProductItemSerializer

class ProductItemListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny, )
    queryset = ProductItem.objects.all()
    serializer_class = ProductItemSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        images_data = self.request.data.get('images', [])
        
        for image_data in images_data:
            image_url = image_data.get('image_url')
            if image_url:
                image_instance, created = Image.objects.get_or_create(image_url=image_url)
                instance.images.add(image_instance)

class ProductItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.AllowAny, )
    queryset = ProductItem.objects.all()
    serializer_class = ProductItemSerializer


