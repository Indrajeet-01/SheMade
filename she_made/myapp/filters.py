# filters.py

import django_filters
from products.models import ProductItem

class ProductItemFilter(django_filters.FilterSet):
    name_contains = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    category = django_filters.ChoiceFilter(field_name='category', choices=ProductItem.CATEGORY_CHOICES)
    sub_category = django_filters.ChoiceFilter(field_name='sub_category', choices=ProductItem.SUB_CATEGORY_CHOICES)
    content_contains = django_filters.CharFilter(field_name='content', lookup_expr='icontains')

    class Meta:
        model = ProductItem
        fields = ['name_contains', 'category', 'sub_category', 'content_contains']