# Generated by Django 3.0.3 on 2020-02-06 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csv_app', '0004_auto_20200206_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='dueDate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoiceDate',
            field=models.DateField(),
        ),
    ]