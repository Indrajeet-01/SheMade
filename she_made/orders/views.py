from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import AddressForm, PaymentDetailsForm
from .models import Order, OrderItem, PaymentDetails, PhoneVerification
from products.models import ProductItem

from django.http import JsonResponse

class CheckoutView(View):
    def post(self, request):
        address_form = AddressForm(request.POST)
        payment_method = request.POST.get('payment_method')
        print(payment_method)

        if payment_method == 'cash_on_delivery':
            # If payment method is cash on delivery, skip payment form validation
            if address_form.is_valid():
                address_instance = address_form.save()
                cart = request.session.get('cart', {})
                total = request.session.get('cart_total', 0)

                order = Order(address=address_instance, order_total=total, payment_method=payment_method)
                order.save()

                # Save order items from session to the database
                for item_id, item_data in cart.items():
                    order_item = ProductItem.objects.get(id=item_id)
                    quantity = item_data['quantity']
                    OrderItem.objects.create(order=order, product_item=order_item, quantity=quantity, price=order_item.price)

                # Clear the cart session
                request.session['cart'] = {}

                messages.success(request, "Order placed successfully!")
                return JsonResponse({'status': 'success', 'message': 'Order placed successfully!'})
            else:
                # Return JSON response with validation errors for address
                return JsonResponse({'status': 'error', 'errors': {'address': address_form.errors}})

        else:
            # For other payment methods, proceed with both address and payment form validation
            payment_form = PaymentDetailsForm(request.POST)
            if address_form.is_valid() and payment_form.is_valid():
                address_instance = address_form.save()
                payment_instance = payment_form.save(commit=False)
                payment_instance.save()
                cart = request.session.get('cart', {})
                total = request.session.get('cart_total', 0)

                order = Order(address=address_instance, order_total=total, payment_method=payment_method)
                order.save()

                # Save order items from session to the database
                for item_id, item_data in cart.items():
                    order_item = ProductItem.objects.get(id=item_id)
                    quantity = item_data['quantity']
                    OrderItem.objects.create(order=order, product_item=order_item, quantity=quantity, price=order_item.price)

                # Clear the cart session
                request.session['cart'] = {}

                messages.success(request, "Order placed successfully!")
                return JsonResponse({'status': 'success', 'message': 'Order placed successfully!'})
            else:
                # Return JSON response with validation errors for both address and payment form
                return JsonResponse({'status': 'error', 'errors': {'address': address_form.errors, 'payment': payment_form.errors}})

def calculate_order_total(request):
    # Retrieve cart items from session
    cart = request.session.get('cart', {})
    
    # Calculate total order amount based on cart items
    total = 0
    for item_id, item_data in cart.items():
        quantity = item_data['quantity']
        # Fetch the order item from the database using item_id
        order_item = ProductItem.objects.get(id=item_id)
        # Access the product item associated with the order item
        
        # Calculate subtotal for each item (price * quantity)
        subtotal = order_item.price * quantity
        # Add subtotal to the total order amount
        total += subtotal
    
    # Add delivery charge or any other additional charges if applicable
    total += 60  # Assuming a flat delivery charge of ₹60
    
    return total
