from rest_framework import serializers
from .models import Invoice, InvoiceItem, Payment


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['id', 'item', 'quantity', 'invoice']
        # depth = 1

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'invoice', 'payment', 'created_at']
        # depth = 1

class InvoiceSerializer(serializers.ModelSerializer):
    invoiceitems = InvoiceItemSerializer(many=True)
    payments = PaymentSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['id', 'invoice_no', 'user', 'created_at', 'updated_at', 'tax_total', 'sub_total', 'total', 'pending_amount', 'payment_status', 'due_date', 'invoiceitems', 'payments']
        # depth = 1