from django.db import models

# Create your models here.
class Invoice(models.Model):
    contactName = models.CharField(max_length=40)
    invoiceNumber=models.IntegerField()
    invoiceDate = models.DateField()
    dueDate=models.DateField()
    description=models.TextField()
    quantity=models.IntegerField()
    unitAmount=models.IntegerField()

    def __str__(self):
        return self.contactName

class InvoiceFile(models.Model):
    file = models.FileField(upload_to='invoice/')
    