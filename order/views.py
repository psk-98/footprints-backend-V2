import random, string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view

from django.contrib.auth.models import User

from .serializers import AddressSerializer, OrderSerializer

from .models import Order, OrderItem, Address, Payment
from product.models import Product, ProductStock

from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_KEY

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

class OrderView(APIView):
    serializer_class = OrderSerializer

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data) 

    def post(self, request):
        print(request.user)
        shipping = request.data['customer_address']
        email = shipping['email']
        name = shipping['name']
        s_address = shipping['address']
        postal = shipping['postal']
        city = shipping['city']
        country = shipping['country']
        guest = False
        payment_method_id = request.data['payment_method_id']
        total = 0
        #guest checkout or not
        if(len(User.objects.filter(id = request.user.id)) != 0 ):
            user = request.user
            print("user")
            if (Address.objects.get(user=user)):
                address = Address.objects.get(user=user)
            else:
                address = Address.objects.create(user=user)
        else:
            guest = True
            address = Address.objects.create(email=email, guest=guest,
                                            name=name,
                                            address=s_address,
                                            postal=postal,
                                            city=city,
                                            country=country,
                                            default=True,
                                            address_type="S")
        
        address.save()


        
            #address.save()
            #print(address)
            #queryset = []
        order = Order.objects.create(ref_code=create_ref_code(),
                                        shipping_address=address,
                                        guest=guest)
        for item in request.data['order_items']:
            print(item["quantity"])
            quantity = item["quantity"]
            size = item["size"]
            product = item["id"]
            product = Product.objects.get(id=product)

            if(ProductStock.objects.get(product=product, size=size)):
                
                stock = ProductStock.objects.get(product=product, size=size)
                stock.amount_in_stock -= quantity
                stock.save()
                orderItem = OrderItem.objects.create(item=product, order=order,
                                                    quantity=quantity, size=size)
                orderItem.save()
                total += orderItem.get_final_price()
        order.save()

        extra_msg = ''

        customer_data = stripe.Customer.list(email=email).data

        if len(customer_data) == 0:
            #creating customer
            customer = stripe.Customer.create(email=email, payment_method=payment_method_id)
        else:
            customer = customer_data[0]
            extra_msg = "Customer already existed."

        order_amount = total

        stripe.PaymentIntent.create(
            customer=customer,
            payment_method=payment_method_id,
            currency='zar',
            amount=int(order_amount*100),
            confirm=True
        )

        payment = Payment.objects.create(stripe_charge_id=payment_method_id,
                                          amount=order_amount)
        
        if(len(User.objects.filter(id = request.user.id)) != 0 ):
            payment.save(user=request.user)
        else:
            payment.save()


        serializer = OrderSerializer(order)
    
        return Response(serializer.data)

class AddressView(generics.CreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

@api_view(['POST'])
def test_payment(request):
    
    test_payment_intent = stripe.PaymentIntent.create(
    amount=1000, currency='pln', 
    payment_method_types=['card'],
    receipt_email='test@example.com')
    return Response(status=status.HTTP_200_OK, data=test_payment_intent)

@api_view(['POST'])
def save_stripe_info(request):
    data = request.data
    email = data['email']
    payment_method_id = data['payment_method_id']
    extra_msg = ''

    #check if customer email exists
    customer_data = stripe.Customer.list(email=email).data

    if len(customer_data) == 0:
        #creating customer
        customer = stripe.Customer.create(email=email, payment_method=payment_method_id)
    else:
        customer = customer_data[0]
        extra_msg = "Customer already existed."

    stripe.PaymentIntent.create(
        customer=customer,
        payment_method=payment_method_id,
        currency='zar',
        amount=999,
        confirm=True
    )

    return Response(status=status.HTTP_200_OK, 
            data={'message': 'Success', 'data': {
            'customer_id': customer.id, 'extra_msg': extra_msg}
        })