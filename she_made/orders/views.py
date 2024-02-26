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
                delivery_charge = request.POST.get('delivery_charge', 0)  # Assuming delivery charge is an integer
                discount_amount = request.POST.get('discount_amount', 0)  # Assuming discount amount is an integer
                
                order_total = request.POST.get('order_total')
                order = Order(address=address_instance, order_total=order_total, delivery_charge=delivery_charge, discount_amount=discount_amount, payment_method=payment_method)
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


