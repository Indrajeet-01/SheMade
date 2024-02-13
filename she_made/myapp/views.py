from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import permissions
from rest_framework import generics
from django.db.models import Q
from django.utils.text import slugify
from products.models import ProductItem
from products.serializers import ProductItemSerializer
from django.views import View
from django.http import JsonResponse
from .filters import ProductItemFilter
import decimal
from django.views.generic.list import ListView
from products.serializers import ProductItemSerializer
from rest_framework.pagination import PageNumberPagination
from django.views.generic import TemplateView


def about_us(request):
    return render(request, 'about_us.html')

def blogs(request):
    return render(request, 'blogs.html')

def contact(request):
    return render(request, 'contact_us.html')


class ShopView(ListView):
    model = ProductItem
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 12

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        category = request.GET.get('filter.p.category')
        sub_category = request.GET.get('filter.p.sub_category')
        min_price = request.GET.get('filter.p.min_price')
        max_price = request.GET.get('filter.p.max_price')

        if category:
            queryset = queryset.filter(category=category)
        if sub_category:
            queryset = queryset.filter(sub_category=sub_category)
        if min_price:
            min_price = decimal.Decimal(min_price)
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            max_price = decimal.Decimal(max_price)
            queryset = queryset.filter(price__lte=max_price)

        return render(request, self.template_name, {'products': queryset})


class ProductListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = ProductItemSerializer

    def get_queryset(self):
        queryset = ProductItem.objects.filter(
            Q(category='Fragrances') |
            Q(category='body_bath') |
            Q(category='SKIN')
        )
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        perfumes = queryset.filter(category='Fragrances')
        body_bath = queryset.filter(category='body_bath')
        skin = queryset.filter(category='SKIN')
        context = {
            'fragrances': perfumes,
            'body_bath': body_bath,
            'skin': skin
        }
        return render(request, 'index.html', context)
    
def product_detail(request, product_id, product_description):
    # Retrieve the product from the database
    product = get_object_or_404(ProductItem, id=product_id)

    # Modify the product description to replace spaces with hyphens
    modified_description = slugify(product_description)

    # Pass the product and modified description to the template
    context = {
        'product': product,
        'modified_description': modified_description
    }

    # Render the template with the product details
    return render(request, 'product_detail.html', context)

def subcategory_products(request, sub_category):
    # Filter products based on the selected sub-category
    products = ProductItem.objects.filter(sub_category=sub_category)

    # Pass the filtered products and sub-category to the template
    context = {
        'products': products,
        'sub_category': sub_category,
    }

    return render(request, 'product_subcat.html', context)



def search_view(request):
    queryset = ProductItem.objects.all()
    query = request.GET.get('key')
    if query:
        queryset = ProductItemFilter(request.GET, queryset=queryset).qs
    return render(request, 'search.html', {'products': queryset})

def search_results_view(request):
    query = request.GET.get('key')
    queryset = ProductItem.objects.filter(name__icontains=query)
    return render(request, 'search_result.html', {'products': queryset, 'query': query})


class SearchProduct(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProductItemSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = ProductItem.objects.all()

        # Get query parameters from the request
        category = self.request.query_params.get('category')
        sub_category = self.request.query_params.get('sub_category')
        content = self.request.query_params.get('content')
        product_name = self.request.query_params.get('name')

        # Apply filters based on query parameters
        if category:
            queryset = queryset.filter(category=category)
        if sub_category:
            queryset = queryset.filter(sub_category=sub_category)
        if content:
            queryset = queryset.filter(content__icontains=content)
        if product_name:
            queryset = queryset.filter(name__icontains=product_name)

        queryset = queryset.order_by('id')

        return queryset


def add_to_cart(request, item_id):
    # Ensure the 'cart' key is initialized in the session
    if 'cart' not in request.session:
        request.session['cart'] = {}
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        item = get_object_or_404(ProductItem, pk=item_id)  # Get the item
        cart = request.session['cart']
        
        # Retrieve the related images queryset or objects
        images = item.images.all()

        # Check if there are any images related to the item
        if images.exists():
            # Access the first image URL
            first_image_url = images.first().image_url
        else:
            # Handle the case where there are no images related to the item
            # You can set a default image URL or handle it based on your requirements
            first_image_url = "default_image_url.jpg"  # Replace with your default image URL

        if item_id in cart:
            cart[item_id]['quantity'] += quantity
        else:
            cart[item_id] = {
                'image': first_image_url,
                'name': item.name,
                'quantity': quantity,
                'price': float(item.price)
            }
        request.session.modified = True
        return redirect('view_cart')
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

def view_cart(request):
    cart = request.session.get('cart', {})
    # Convert the Decimal to float when calculating the total
    for item_data in cart.values():
        item_data['total'] = float(item_data['quantity']) * float(item_data['price'])
    total = sum(item_data['total'] for item_data in cart.values())
    request.session['cart_total'] = total
    return render(request, 'cart.html', {'cart': cart, 'total': total})

def remove_from_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        if 'cart' in request.session:
            cart = request.session['cart']
            if item_id in cart:
                del cart[item_id]
                request.session.modified = True
                return redirect('view_cart')
    return JsonResponse({'success': False, 'error': 'Invalid request'})