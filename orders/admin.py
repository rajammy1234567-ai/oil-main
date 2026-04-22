from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'razorpay_order_id', 'razorpay_payment_id', 'amount', 'currency', 'status', 'delivery_date', 'created_at')
    list_filter = ('status', 'currency', 'created_at')
    search_fields = ('razorpay_order_id', 'razorpay_payment_id', 'receipt', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    list_editable = ('status', 'delivery_date')
