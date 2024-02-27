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
    generic_name = models.CharField(max_length=255, blank=True)
    quality_assurance = models.CharField(max_length=255, blank=True)
    eco_friendly = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=255, blank=True)
    country_of_origin = models.CharField(max_length=255, blank=True)
    handcrafted_by = models.CharField(max_length=255, blank=True)
    packed_by = models.CharField(max_length=255, blank=True)
    marketed_by = models.CharField(max_length=255, blank=True)
    product_type = models.CharField(max_length=255, blank=True)
    weight = models.CharField(max_length=255, blank=True)
    expiry = models.CharField(max_length=255, blank=True)
    
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

    
    benefits = models.TextField(blank=True, null=True)
    def set_benefits(self, benefits):
        self.benefits = '#'.join(benefits)
    def get_benefits(self):
        return self.benefits.split('#') if self.benefits else []
    
    key_ingredients = models.TextField(blank=True, null=True)
    def set_key_ingredients(self, key_ingredients):
        self.key_ingredients = '#'.join(key_ingredients)
    def get_key_ingredients(self):
        return self.key_ingredients.split('#') if self.key_ingredients else []
    
    directions = models.TextField(blank=True, null=True)
    def set_directions(self, directions):
        self.directions = '#'.join(directions)
    def get_directions(self):
        return self.directions.split('#') if self.directions else []
    
    key_notes = models.TextField(blank=True, null=True)
    def set_key_notes(self, key_notes):
        self.key_notes = '#'.join(key_notes)
    def get_key_note(self):
        return self.key_notes.split('#') if self.key_notes else []
    
    safety_warnings = models.TextField(blank=True, null=True)
    def set_safety_warnings(self, safety_warnings):
        self.safety_warnings = '#'.join(safety_warnings)
    def get_safety_warnings(self):
        return self.safety_warnings.split('#') if self.safety_warnings else []
    
    cautions = models.TextField(blank=True, null=True)
    def set_cautions(self, cautions):
        self.cautions = '#'.join(cautions)
    def get_cautions(self):
        return self.cautions.split('#') if self.cautions else []
    
    faqs = models.TextField(blank=True, null=True)
    def set_faqs(self, faqs):
        self.faqs = '#'.join(faqs)
    def get_faqs(self):
        return self.faqs.split('#') if self.faqs else []


    def __str__(self):
        return self.name
    

class Image(models.Model):
    image_url = models.URLField()

    def __str__(self):
        return self.image_url
