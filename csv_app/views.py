from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import CreateAPIView
from .serializer import InvoiceFile_Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import csv, io

# Calculate transactions from date
import datetime as dt
from datetime import datetime

# Date imports end
from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
import codecs
from .models import Invoice
from django.contrib import messages
import logging
from .forms import InvoiceForm
from django.db.models import Sum, F
# Truncates a date up to a significant component.-The month or year
from django.db.models.functions import TruncMonth, TruncYear, TruncDay


def uploadcsv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "base.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("csv_app:upload_csv"))
        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("csv_app:upload_csv"))

        file_data = csv_file.read().decode("utf-8")

        io_string = io.StringIO(file_data)

        # loop over the lines and save them in db. If error , store as string and then display
        i = 0
        for fields in csv.reader(io_string, skipinitialspace=True):
            # only allow after header
            if (i):
                if (len(fields) > 19):
                    data_dict = {}
                    data_dict["contactName"] = fields[0]
                    data_dict["invoiceNumber"] = fields[10]
                    data_dict["invoiceDate"] = datetime.strptime(fields[12], '%d/%m/%Y')
                    data_dict["dueDate"] = datetime.strptime(fields[13], '%d/%m/%Y')
                    #date dict just for demonstration
                    data_dict["description"] = fields[16]
                    data_dict["quantity"] = fields[17]
                    data_dict["unitAmount"] = fields[18]
                    try:
                        #add Invoice Directly to model
                        test = Invoice.objects.create(contactName=fields[0], invoiceNumber=fields[10],
                                                      invoiceDate=datetime.strptime(fields[12], '%d/%m/%Y'),
                                                      dueDate=datetime.strptime(fields[12], '%d/%m/%Y'),
                                                      description=fields[16], quantity=fields[17],
                                                      unitAmount=fields[18])
                    except Exception as e:
                        print(e)

            i = i + 1

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. " + repr(e))
        messages.error(request, "Unable to upload file. " + repr(e))

    #Calculating UI Amounts
    # Returning a summary of total amount incurred for each month
    monthly_totals_ui=Invoice.objects.annotate(month=TruncMonth('invoiceDate'), year=TruncYear("invoiceDate")).values('month', 'year').annotate(total=Sum(F('quantity')*F('unitAmount'))).values('month', 'year', 'total')
    # Data for a Bar Chart showing Top Five customers according Total amount due
    top_five_customers_ui=Invoice.objects.all().annotate(customer_total=Sum(F('quantity')*F('unitAmount'))).order_by('-customer_total').values_list('contactName', 'customer_total')[:5]
    
    # Data for A line graph showing all transactions that took place 30days from a given date (using today's date for demo)
    now = datetime.now()
    dt_t = now - dt.timedelta(30)#Delta imported above
    total_daily_transaction=Invoice.objects.filter(invoiceDate__gte=dt_t, invoiceDate__lte=now).annotate(day=TruncDay('invoiceDate')).values('day').annotate(total=Sum(F('quantity')*F('unitAmount'))).values('day','total')
    
    # print(total_daily_transaction)

    context={
        'monthly_totals_ui': monthly_totals_ui,
        'top_five_customers_ui': top_five_customers_ui,
        'total_daily_transaction': total_daily_transaction
    }
    print(context)

    return render(request, 'base.html', context)



class InvoiceUploadAPIView(CreateAPIView):
    serializer_class = InvoiceFile_Serializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        file_data = file.read().decode("utf-8")

        io_string = io.StringIO(file_data)

        # loop over the lines and save them in db. If error , store as string and then display
        i = 0
        for fields in csv.reader(io_string, skipinitialspace=True):
            # only allow after header
            if (i):
                if (len(fields) > 19):
                    data_dict = {}
                    data_dict["contactName"] = fields[0]
                    data_dict["invoiceNumber"] = fields[10]
                    data_dict["invoiceDate"] = datetime.strptime(fields[12], '%d/%m/%Y')
                    data_dict["dueDate"] = datetime.strptime(fields[13], '%d/%m/%Y')
                    # date dict just for demonstration
                    data_dict["description"] = fields[16]
                    data_dict["quantity"] = fields[17]
                    data_dict["unitAmount"] = fields[18]
                    try:
                        # add Invoice Directly to model
                        test = Invoice.objects.create(contactName=fields[0], invoiceNumber=fields[10],
                                                      invoiceDate=datetime.strptime(fields[12], '%d/%m/%Y'),
                                                      dueDate=datetime.strptime(fields[12], '%d/%m/%Y'),
                                                      description=fields[16], quantity=fields[17],
                                                      unitAmount=fields[18])
                        
                        
                    except Exception as e:
                        print(e)
            i = i + 1

        # just for demo
        invoices = Invoice.objects.all()
        
    
        # Calculating API Amounts

        # Returning a summary of total amount incurred for each month
        monthly_totals=Invoice.objects.annotate(month=TruncMonth('invoiceDate'), year=TruncYear("invoiceDate")).values('month', 'year').annotate(total=Sum(F('quantity')*F('unitAmount'))).values('month', 'year', 'total')
        
        # Returning the Top Five customers according Total amount (quantity * unitAmount) due for a given year
        top_five_customers=Invoice.objects.all().annotate(customer_total=Sum(F('quantity')*F('unitAmount'))).order_by('-customer_total').values_list('contactName', 'customer_total')[:5]
        
        # Returning the Top Five customers, according to Quantity bought.
        top_customers_quantity=Invoice.objects.all().order_by('-quantity').values_list('contactName', 'quantity')[:5]

        # Returning total invoice transaction per day for all transactions that took place 30days from a given date.
        now = datetime.now()
        dt_t = now - dt.timedelta(30)#Delta imported above
        total_daily_invoice=Invoice.objects.filter(invoiceDate__gte=dt_t, invoiceDate__lte=now).annotate(day=TruncDay('invoiceDate')).values('day').annotate(total=Sum(F('quantity')*F('unitAmount'))).values('day','total')
       
        context={
            'monthly_totals': monthly_totals,
            'top_five_customers': top_five_customers,
            'top_customers_quantity': top_customers_quantity,
            'total_daily_invoice': total_daily_invoice

        }
        print(context)

        return Response(status=status.HTTP_204_NO_CONTENT)
        return render(request, 'base.html', context)
