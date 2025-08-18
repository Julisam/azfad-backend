from django.contrib import admin
from .models import Payment

# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'email', 'amount',
        'status', 'updated',
    ]
    list_filter = ['status', 'created', 'updated']
