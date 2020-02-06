from .models import Invoice
from django.forms import ModelForm


class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ['contactName', 'invoiceNumber', 'invoiceDate', 'dueDate', 'description', 'quantity', 'unitAmount' ]