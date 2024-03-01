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
from django.contrib import messages


def aboutus(request):
    print('hey from about')
    context = {

    }
    return render(request, 'about_us.html', context)

def dummy(request):
    print('hey from dummy') 
    
    return render(request, 'dummy.html')

def security_warranty(request):
    return render(request, 'support_warranty.html')

def return_policy(request):
    return render(request, 'return_policy.html')

def faqs(request):
    return render(request, 'faqs.html')

def term_condition(request):
    return render(request, 'term_condition.html')

def social_responsibility(request):
    return render(request, 'social_responsiblity.html')

def bulk_order(request):
    return render(request, 'bulk_order.html')

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

def offers(request):
    return render(request, 'offers.html')

def checkout(request):
    return render(request, 'checkout.html')

def userFrofile(request):
    return render(request, 'user_profile.html')

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
        
        sort_by = self.request.GET.get('sort_by')

        if category:
            queryset = queryset.filter(category=category)
        if sub_category:
            queryset = queryset.filter(sub_category=sub_category)
        
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
            Q(category='SKIN') |
            Q(category='Candles')
        )
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        perfumes = queryset.filter(category='Fragrances')
        body_bath = queryset.filter(category='body_bath')
        skin = queryset.filter(category='SKIN')
        candles = queryset.filter(category='Candles')
        context = {
            'fragrances': perfumes,
            'body_bath': body_bath,
            'skin': skin,
            'candles' : candles
        }
        return render(request, 'index.html', context)
    
def product_detail(request, product_id, product_name):
    print('hey from product detail')
    # Retrieve the product from the database
    product = get_object_or_404(ProductItem, id=product_id)

    # Modify the product description to replace spaces with hyphens
    modified_name = slugify(product_name)

    related_products = ProductItem.objects.filter(sub_category=product.sub_category).exclude(id=product_id)[:5]

    # Pass the product and modified description to the template
    context = { 
        'product': product,
        'modified_description': modified_name,
        'related_products': related_products
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
        request.session.save()
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
    print("Cart Total:", total)
    
    request.session['cart_total'] = total
    print(cart)
    return render(request, 'cart.html', {'cart': cart, 'total': total})

def remove_from_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        if 'cart' in request.session:
            cart = request.session['cart']
            if item_id in cart:
                del cart[item_id]
                request.session.modified = True
                request.session.save()
                return redirect('view_cart')
    return JsonResponse({'success': False, 'error': 'Invalid request'})


def update_cart(request):
    print('he from cart update')
    print(request.method)
    
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        new_quantity = int(request.POST.get('quantity', 1))
        print(item_id)
        print(new_quantity)
        if 'cart' in request.session:
            cart = request.session['cart']
            if item_id in cart:
                # Get the item data
                item_data = cart[item_id]
                # Calculate the price of the item
                item_price = item_data['price']
                # Calculate the current total of the item
                current_total = item_data['quantity'] * item_price
                # Update the quantity of the item
                cart[item_id]['quantity'] = new_quantity
                # Calculate the new total of the item
                new_total = new_quantity * item_price
                # Update the cart total
                cart_total = sum(cart[item]['quantity'] * cart[item]['price'] for item in cart)
                print(cart_total)
                request.session['cart_total'] = cart_total
                # Save the changes to the session
                request.session.modified = True
                request.session.save()
                # Return the updated totals
                return redirect('view_cart')
    # If the request is not valid or if there's an error, stay on the cart page
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