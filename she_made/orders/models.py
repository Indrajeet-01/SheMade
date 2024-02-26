from django.core.exceptions import ValidationError
from django.db import models
from twilio.rest import Client
from products.models import ProductItem
import random
import string

class Address(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    street = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.street}, {self.district}, {self.state}"
    

class PhoneVerification(models.Model):
    order = models.OneToOneField('Order', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    verification_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Phone Verification for Order #{self.order.id}"

class PaymentDetails(models.Model):
    
    card_number = models.CharField(max_length=16, null=True, blank=True)
    expiry_month = models.IntegerField(null=True, blank=True)
    expiry_year = models.IntegerField(null=True, blank=True)
    cvc = models.CharField(max_length=4, null=True, blank=True)
    card_holder_name = models.CharField(max_length=255, null=True, blank=True)
    upi_id = models.CharField(max_length=255, null=True, blank=True)
    is_verified = models.BooleanField(default=False, editable=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    

    def __str__(self):
        if self.card_number:
            return f"Card Payment - {self.card_number}"
        elif self.upi_id:
            return f"UPI Payment - {self.upi_id}"
        elif self.transaction_id:
            return f"Cash on Delivery - {self.transaction_id}"
        else:
            return "Payment Details"

class Order(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=[('card', 'Card'), ('upi', 'UPI'), ('cash_on_delivery', 'Cash on Delivery')])
    payment_details = models.OneToOneField(PaymentDetails, on_delete=models.CASCADE, null=True, blank=True)
    order_items = models.ManyToManyField(ProductItem, through='OrderItem', related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    def generate_verification_code(self):
        """Generate a random verification code."""
        return ''.join(random.choices(string.digits, k=6))  # Generates a 6-digit random string

    def save(self, *args, **kwargs):
        if self.payment_method == 'cash_on_delivery':
            # Create phone verification instance for cash on delivery orders
            # phone_verification = PhoneVerification(order=self, phone_number=self.address.phone)
            # phone_verification.verification_code = self.generate_verification_code()  # Generate verification code
            # phone_verification.save()

            # # Send verification code via Twilio SMS
            #             # Send verification code via Twilio SMS
            # account_sid = 'your_account_sid'
            # auth_token = 'your_auth_token'
            # client = Client(account_sid, auth_token)

            # message = client.messages.create(
            #     body=f"Your verification code for Order #{self.id} is: {phone_verification.verification_code}",
            #     from_='your_twilio_phone_number',
            #     to=self.address.phone
            # )
            # Your Twilio SMS code here...

            # Set payment_details to None since it's not required for cash on delivery
            self.payment_details = None
        else:
            PhoneVerification.objects.filter(order=self).delete()
            # For other payment methods, create or update payment_details
            if not self.payment_details:
                self.payment_details = PaymentDetails.objects.create()
            self.payment_details.card_number = None
            self.payment_details.expiry_month = None
            self.payment_details.expiry_year = None
            self.payment_details.cvc = None
            self.payment_details.card_holder_name = None
            self.payment_details.upi_id = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrderItem #{self.id} for Order #{self.order.id}"



