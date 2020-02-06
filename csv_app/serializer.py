from rest_framework import serializers
from .models import Invoice, InvoiceFile

class InvoiceFile_Serializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceFile
        fields = ('invoice_csv',)

            