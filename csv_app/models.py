from django.db import models

# Create your models here.
class Invoice(models.Model):
    contactName = models.CharField(max_length=40)
    invoiceNumber=models.IntegerField()
    invoiceNumber = models.DateField()
    dueDate=models.DateField()
    price = models.DecimalField(decimal_places=2, max_digits=20)
    description=models.TextField()
    quantity=models.IntegerField()
    unitAmount=models.IntegerField()