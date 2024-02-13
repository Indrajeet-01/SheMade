from django.contrib import admin
from .models import ProductItem, Image

@admin.register(ProductItem)
class ProductItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'display_image_urls')
    list_filter = ('category', 'sub_category')
    search_fields = ('name', 'description', 'category', 'sub_category')

    # Custom method to display related image URLs
    def display_image_urls(self, obj):
        return ', '.join([image.image_url for image in obj.images.all()])

    display_image_urls.short_description = 'Image URLs'

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_url',)

# No need for ImageInline class anymore

