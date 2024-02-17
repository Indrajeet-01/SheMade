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
from fuzzywuzzy import fuzz 
from django.db.models import F
from rest_framework.pagination import PageNumberPagination
from django.views.generic import TemplateView


def aboutus(request):
    print('hey from about')
    context = {

    }
    return render(request, 'about_us.html', context)


def contact(request): 
    print('hey from contact')
    return render(request, 'contact_us.html')

def blogs(request):
    print("hey from blogs")
    return render(request, 'blogs.html')

def cart(request):
    print('hey from cart')
    return render(request, 'cart.html')

def wishlist(request):
    return render(request, 'wishlist.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def checkout(request):
    return render(request, 'checkout.html')

class ShopView(ListView):
    print('hey from shop')
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
        sort_by = self.request.GET.get('sort_by')

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
        if sort_by == 'low_to_high':
            queryset = queryset.order_by('price')
        elif sort_by == 'high_to_low':
            queryset = queryset.order_by(F('price').desc())

        return render(request, self.template_name, {'products': queryset})


# product handling
class ProductListView(generics.ListAPIView):
    print('hey from home')
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
    print('hey from product detail')
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


# search handling
def search_view(request):
    print('hey from search')
    # Get the search query from the request GET parameters
    query = request.GET.get('key')

    # Perform the search query on the ProductItem model
    if query:
        # Split the search query into separate words
        query_parts = query.split()

        # Initialize a queryset to store the search results
        products = ProductItem.objects.all()

        # Initialize an empty set to store the matching products
        matching_products = set()

        # Filter products based on each word in the query
        for part in query_parts:
            # Filter based on exact match first
            exact_matches = products.filter(
                Q(name__icontains=part) |
                Q(category__icontains=part) |
                Q(sub_category__icontains=part)
            )

            # If no exact match found, search for approximate matches using fuzzy matching
            if not exact_matches.exists():
                # Perform fuzzy matching against product name, category, and subcategory
                for product in products:
                    if (fuzz.partial_ratio(part, product.name) > 65 or
                        fuzz.partial_ratio(part, product.category) > 65 or
                        fuzz.partial_ratio(part, product.sub_category) > 65):
                        matching_products.add(product)

        # Combine exact and approximate matches
        matching_products |= set(exact_matches)

        # Convert the set to a queryset and remove duplicates
        products = ProductItem.objects.filter(pk__in=[product.pk for product in matching_products])

        # Render the search template with the search results
        return render(request, 'search.html', {'products': products, 'query': query})
    else:
        # If no query provided, render the search template without results
        return render(request, 'search.html')


# cart handling
def add_to_cart(request, item_id):
    if 'cart' not in request.session:
        request.session['cart'] = {}

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        item = get_object_or_404(ProductItem, pk=item_id)
        cart = request.session['cart']
        images = item.images.all()
        
        # Access the first image URL if available, otherwise provide a default image URL
        first_image_url = images.first().image_url
        print(first_image_url)

        if item_id in cart:
            cart[item_id]['quantity'] += quantity
        else:
            cart[item_id] = {
                'image': first_image_url,
                'name': item.name,
                'quantity': quantity,
                'price': float(item.price)  # Convert Decimal to float for arithmetic
            }
        request.session.modified = True
        print('item is added')
        return redirect('view_cart')

    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

def view_cart(request):
    print('hey from cart ')
    cart = request.session.get('cart', {})
    
    # Convert the Decimal to float when calculating the total
    for item_data in cart.values():
        item_data['total'] = float(item_data['quantity']) * float(item_data['price'])
    
    # Calculate the total with two decimal places
    total = sum(item_data['total'] for item_data in cart.values())
    total = "{:.2f}".format(total)  # Format the total with two decimal places
    
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

def add_to_wishlist(request, item_id):
    if 'wishlist' not in request.session:
        request.session['wishlist'] = {}

    if request.method == 'POST':
        item = get_object_or_404(ProductItem, pk=item_id)
        wishlist = request.session['wishlist']
        images = item.images.all()

        # Access the first image URL if available, otherwise provide a default image URL
        first_image_url = images.first().image_url if images.exists() else 'default_image_url.jpg'
        

        if item_id in wishlist:
            # If the item is already in the wishlist, you may want to handle this differently, such as updating the quantity
            pass
        else:
            
            wishlist[item_id] = {
                'product_id': item_id,
                'image': first_image_url,
                'name': item.name,
                'description': item.description,  # Ensure description is set here
                'price': float(item.price),
                # Add more details as needed
            }
        
        request.session.modified = True
        return redirect('view_wishlist')

    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

def view_wishlist(request):
    wishlist = request.session.get('wishlist', {})
    
    return render(request, 'wishlist.html', {'wishlist': wishlist})

def remove_from_wishlist(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        wishlist = request.session.get('wishlist', {})
        if item_id in wishlist:
            del wishlist[item_id]
            request.session['wishlist'] = wishlist
            return redirect('view_wishlist')
    return JsonResponse({'success': False, 'error': 'Invalid request'})