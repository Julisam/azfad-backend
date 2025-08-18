from django.db import models
import uuid
from api.models import CustomUser

# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    paystack_ref = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=100, default='initialized')
    message = models.JSONField(default=dict)

    cart_items = models.JSONField(default=dict)


    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Paymen: {self.email} {self.amount}'

    def get_amount(self):
        return self.amount
    
    def save(self, *args, **kwargs):
        while not self.paystack_ref:
            ref = str(uuid.uuid4())
            object_with_similar_ref = Payment.objects.filter(paystack_ref=ref)
            if not object_with_similar_ref:
                self.paystack_ref = ref

        super().save(*args, **kwargs)