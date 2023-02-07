from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.decorators import api_view

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


from .serializers import AddressSerializer, OrderSerializer

from .models import Order, OrderItem, Address, Payment
from product.models import Product, ProductStock

import stripe, requests, random, string

stripe.api_key = settings.STRIPE_KEY

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))

def yoco_payment(token, amount):
    response = requests.post(
        'https://online.yoco.com/v1/charges/',
        headers={
            'X-Auth-Secret-Key': 'sk_test_960bfde0VBrLlpK098e4ffeb53e1',
        },
        json={
            'token': token,
            'currency': 'ZAR',
            'amountInCents': amount,
        },
    )
    
    res_status = response.status_code
    if (res_status == 201):
        return {'res': response.json(), 'status': res_status}
    elif res_status == 400:
        return {'res': response.json(), 'status': res_status}
    elif (res_status == 500):
        return {'res': response.json(), 'status': res_status}

def confirmation_email(ref_code, name, email):
    full_msg = f'Hi {name},\n\n Thank you for your order to check your order status and tracking details follow go to https://footprintz.netlify.app/orders/{ref_code} \n\n Thanks.' 
    send_mail("Footprints Order Confirmation", full_msg, settings.EMAIL_HOST_USER, [email], fail_silently=False)


    

class OrderView(APIView):
    serializer_class = OrderSerializer

    def get(self, request):
        print(request.query_params)
        #params = (request.data['params'])
        try: 
            order = Order.objects.get(ref_code=request.query_params.get('order_ref'))
            #print(product.tags.similar_objects())
            

            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        orders = Order.objects.get(order_ref=params['order_ref'])

        serializer = OrderSerializer(orders)

        return Response(serializer.data) 

    def post(self, request):
        # print(request.user)
        print(request.data)
        params = (request.data['params'])

        shipping = params['delivery_address']
        email = shipping['email']
        name = shipping['name']
        s_address = shipping['address']
        postal = shipping['postal']
        city = shipping['city']
        country = shipping['country']
        sameAs = shipping['sameAs']
        guest = True
        charge_id = params['charge_id']
        payment_choice = params['payment_choice']
        total = 0
        
        ship_address = Address.objects.create(email=email, guest=True,
                                         name=name,
                                         address=s_address,
                                         postal=postal,
                                         city=city,
                                         country=country,
                                         default=True,
                                         address_type="S")

        ship_address.save()

        if (sameAs is True):
            order = Order.objects.create(ref_code=create_ref_code(),
                                             shipping_address=ship_address,
                                             billing_address=ship_address,
                                             sameAsShipping=True,
                                             )
        else:
            _billing_a = params['billing_address']
            billing_a = Address.objects.create(guest=True,
                                         name=_billing_a['name'],
                                         address=_billing_a['address'],
                                         postal=_billing_a['postal'],
                                         city=_billing_a['city'],
                                         country=_billing_a['country'],
                                         default=True,
                                         address_type="B")
            billing_a.save()
            order = Order.objects.create(ref_code=create_ref_code(),
                                             shipping_address=ship_address,
                                             billing_address=billing_a,
                                             sameAsShipping=False)


        for item in params['order_items']:
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
        


        #handle payments
        res = yoco_payment(params['charge_id'], int(total *100))
        
        res_status = res['status']
        pay_res = res['res']

        print(order.ref_code)

        if res_status == 201:
                
            payment = Payment.objects.create(charge_id=pay_res['id'], amount=(pay_res['amountInCents']/100), payment_method=1)
            if(len(User.objects.filter(id = request.user.id)) != 0 ):
                payment.save(user=request.user)      
            else:
                payment.save()
            
            order.save()
            confirmation_email(order.ref_code, name, email)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        elif res_status == 400:
            try:
                billing_a.delete()
            except UnboundLocalError:
                pass
            ship_address.delete()
            order.delete()
            return Response(status=status.HTTP_400_BAD_REQUEST, data=pay_res)
            

        elif (res_status == 500):
            # for item in order.orderitem_set.all():
            #     item.delete()
            try:
                billing_a.delete()
            except UnboundLocalError:
                pass
            ship_address.delete()
            order.delete()
            print("payment failded")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=pay_res)


        #extra_msg = ''

        # customer_data = stripe.Customer.list(email=email).data

        # if len(customer_data) == 0:
        #     #creating customer
        #     customer = stripe.Customer.create(email=email, payment_method=payment_method_id)
        # else:
        #     customer = customer_data[0]
        #     extra_msg = "Customer already existed."

        # order_amount = total

        # stripe.PaymentIntent.create(
        #     customer=customer,
        #     payment_method=payment_method_id,
        #     currency='zar',
        #     amount=int(order_amount*100),
        #     confirm=True
        # )

        # payment = Payment.objects.create(stripe_charge_id=payment_method_id,
        #                                   amount=order_amount)
        
        # if(len(User.objects.filter(id = request.user.id)) != 0 ):
        #     payment.save(user=request.user)
        # else:
        #     payment.save()


        # serializer = OrderSerializer(order)
    
        # return Response(serializer.data)

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