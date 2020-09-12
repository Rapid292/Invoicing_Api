from rest_framework import serializers
from .models import Invoice, InvoiceItem, Payment

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'invoice_no', 'user', 'created_at', 'updated_at', 'tax_total', 'sub_total', 'total', 'pending_amount', 'payment_status', 'due_date']
        depth = 1

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['item', 'quantity', 'invoice']
        depth = 2

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['invoice', 'payment', 'created_at']
        # depth = 1