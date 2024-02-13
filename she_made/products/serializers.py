from rest_framework import serializers
from .models import ProductItem, Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image_url']

class ProductItemSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)

    class Meta:
        model = ProductItem
        fields = '__all__'

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        product = ProductItem.objects.create(**validated_data)

        for image_data in images_data:
            image_url = image_data.get('image_url')
            if image_url:
                image_instance, _ = Image.objects.get_or_create(image_url=image_url)
                product.images.add(image_instance)

        return product
