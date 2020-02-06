from rest_framework import serializers
from .models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ('contactName', 'invoiceNumber', 'invoiceDate', 'dueDate', 'description', 'quantity', 'unitAmount')
