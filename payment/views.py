import requests
import json
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from api.models import Cart, Enrollment
from .models import Payment

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initialize_payment(request):
    cart_items = request.data.get('cart_items', [])
    
    if not cart_items:
        return Response({'error': 'No cart items provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get cart items and calculate total
    cart_objects = Cart.objects.filter(id__in=cart_items, user=request.user)
    total_amount = sum(item.course.price for item in cart_objects)
    
    # Update cart items
    cart_json = {"ids": [],
                 "name": [],
                 "price": [],
                 }
    for cart_item in cart_objects:
        cart_json['ids'].append(cart_item.id)
        cart_json['name'].append(cart_item.course.title)
        cart_json['price'].append(float(cart_item.course.price))

    # Create payment record
    payment = Payment.objects.create(
        user=request.user,
        email=request.user.email,
        amount=total_amount,
        cart_items = cart_json
    )
    
    # Initialize Paystack payment
    paystack_data = {
        'email': payment.email,
        'amount': int(payment.amount * 100),  # Paystack expects amount in kobo
        'reference': payment.paystack_ref,
        'callback_url': f'{settings.FRONTEND_URL}/payment/callback'
    }
    
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(
            'https://api.paystack.co/transaction/initialize',
            data=json.dumps(paystack_data),
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            payment.message = data
            payment.save()
            
            return Response({
                'authorization_url': data['data']['authorization_url']
            })
        else:
            return Response({'error': 'Payment initialization failed', 'details':response.json()}, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_payment(request):
    reference = request.data.get('reference')
    
    if not reference:
        return Response({'error': 'Reference is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(
            f'https://api.paystack.co/transaction/verify/{reference}',
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            # print(data)
            payment = Payment.objects.get(paystack_ref=reference)
            payment.status = data['data']['status']
            payment.message = data
            payment.save()
            
            if data['data']['status'] == 'success':
                # Process enrollment for specific cart items
                cart_item_ids = payment.cart_items['ids']
                cart_item_price = payment.cart_items['price']

                cart_objects = Cart.objects.filter(id__in=cart_item_ids, user=request.user)
                
                for cart_item in cart_objects:
                    Enrollment.objects.get_or_create(
                        user=request.user,
                        course=cart_item.course,
                        defaults={'cart': cart_item}
                    )
                    cart_item.paid = True
                    cart_item.paid_at = data['data']['paid_at']
                    cart_item.payment_reference = reference
                    cart_item.course_price = cart_item_price[cart_item_ids.index(cart_item.id)]
                    

                    cart_item.save()
                
                payment.status = 'success'
                payment.save()
                
                return Response({'message': 'Payment verified successfully'})
            else:
                return Response({'error': 'Payment verification failed'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Payment verification failed'}, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)