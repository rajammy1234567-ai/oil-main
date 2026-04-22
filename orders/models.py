from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


def default_delivery_date():
    # Default delivery date is 4 days from today
    return (timezone.now() + timedelta(days=4)).date()


class Order(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('processing', 'Processing'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out for delivery'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    razorpay_order_id = models.CharField(max_length=128, blank=True, null=True, db_index=True)
    razorpay_payment_id = models.CharField(max_length=128, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=256, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=8, default='INR')
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='created')
    # Estimated / planned delivery date (optional). Default is today + 4 days.
    delivery_date = models.DateField(null=True, blank=True, default=default_delivery_date)
    receipt = models.CharField(max_length=128, blank=True, null=True)
    items = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.pk} - {self.status} - {self.amount} {self.currency}"
