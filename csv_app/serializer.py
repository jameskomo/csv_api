from rest_framework import serializers
from .models import Invoice, InvoiceFile

class InvoiceFile_Serializer(serializers.ModelSerializer):
    file = serializers.FileField()
    class Meta:
        model = InvoiceFile
        fields = ('file',)


    
