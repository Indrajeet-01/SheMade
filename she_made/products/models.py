from django.db import models  

class ProductItem(models.Model):
    CATEGORY_CHOICES = [
        ('fragrances', 'Fragrances'),
        ('body_bath', 'Body Bath'),
        ('skin', 'Skin'),
    ]
    
    SUB_CATEGORY_CHOICES = [
        ('fragrances', [
            ('dhuni', 'Dhuni'),
            ('perfumes', 'Perfumes'),
            ('attars', 'Attars'),
        ]),
        ('body_bath', [
            ('soaps', 'Soaps'),
            ('shower_gel', 'Shower Gel'),
            ('facewash', 'Face Wash'),
            ('shampoo', 'Shampoo'),
            ('conditioner', 'Conditioner'),
        ]),
        ('skin', [
            ('facetoner', 'Face Toner'),
            ('aleo_gel', 'Aleo Gel'),
            ('lip_care', 'Lip Care'),
            ('scrubs', 'Scrubs'),
        ]),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    sub_category = models.CharField(max_length=20, choices=SUB_CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    content = models.CharField(max_length=255,blank=True)
    stock = models.IntegerField( blank=True)
    life = models.CharField(max_length=255, blank=True)
    
    ingredients = models.TextField(blank=True, null=True)
    direction_to_use = models.TextField(blank=True, null=True)
    images = models.ManyToManyField('Image', related_name='product_items', blank=True)

    def __str__(self):
        return self.name
    
class Image(models.Model):
    image_url = models.URLField()

    def __str__(self):
        return self.image_url
