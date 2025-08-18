import requests
import json
paystack_data = {"email": "julius4sam@gmail.com", 
        "amount": 21000000, 
        "reference": "payment_5_5", 
        "callback_url": "http://localhost:3000/payment/callback"
        }

headers = {
        'Authorization': f'Bearer sk_test_790bac2feccde283b3b96a27dfaa64cb58e43c3d',
        'Content-Type': 'application/json'
    }



res = requests.post(
            'https://api.paystack.co/transaction/initialize',
            data=json.dumps(paystack_data),
            headers=headers
        )
print(res)
print(res.json())



# sample response
# {'status': True, 
#  'message': 'Authorization URL created', 
#  'data': {
#      'authorization_url': 'https://checkout.paystack.com/25gb8dwf0syg0ct', 
#      'access_code': '25gb8dwf0syg0ct', 
#      'reference': 'df5f33d8-bac2-4a86-9dd2-cb9daa247083'}
# }

# "http://localhost:3000/payment/callback/
# 8c76983d-a7d9-4be9-8ec2-e7ea837bfc5f?
# trxref=8c76983d-a7d9-4be9-8ec2-e7ea837bfc5f
# &reference=8c76983d-a7d9-4be9-8ec2-e7ea837bfc5f"


