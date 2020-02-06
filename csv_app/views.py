from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import CreateAPIView
from .serializer import InvoiceFile_Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
import csv, io
from django.shortcuts import render, HttpResponseRedirect, reverse
import codecs
from .models import Invoice
from django.contrib import messages
import logging
from .forms import InvoiceForm

def uploadcsv(request):
	data = {}
	if "GET" == request.method:
		return render(request, "base.html", data)
	# if not GET, then proceed
	try:
		csv_file = request.FILES["csv_file"]
		if not csv_file.name.endswith('.csv'):
			messages.error(request,'File is not CSV type')
			return HttpResponseRedirect(reverse("csv_app:upload_csv"))
		#if file is too large, return
		if csv_file.multiple_chunks():
			messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
			return HttpResponseRedirect(reverse("csv_app:upload_csv"))

		file_data = csv_file.read().decode("utf-8")  		

		lines = file_data.split("\n")
		#loop over the lines and save them in db. If error , store as string and then display
		for line in lines:
			fields = line.split(",")
			data_dict = {}
			data_dict["contactName"] = fields[0]
			data_dict["invoiceNumber"] = fields[10]
			data_dict["invoiceDate"] = fields[12]
			data_dict["dueDate"] = fields[13]
			data_dict["description"] = fields[16]
			data_dict["quantity"] = fields[17]
			data_dict["unitAmount"] = fields[18]
   
   
   
			try:
				form = InvoiceForm(data_dict)
				if form.is_valid():
					form.save()
				else:
					logging.getLogger("error_logger").error(form.errors.as_json())                                                
			except Exception as e:
				logging.getLogger("error_logger").error(form.errors.as_json())                    
				pass

	except Exception as e:
		logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
		messages.error(request,"Unable to upload file. "+repr(e))

	return HttpResponseRedirect(reverse("csv-home"))

class InvoiceUpload(APIView):
    serializer_class = InvoiceFile_Serializer
    parser_classes = [ MultiPartParser,FormParser ]

    def post(self,request):
        try:
            serializer = InvoiceFile_Serializer(data=request.data)
            print(serializer.initial_data)

            if serializer.is_valid():
                if serializer.is_valid():
                    data = self.request.data.get('datafile')
                    reader = csv.DictReader(data, delimiter='\t')
                    for row in reader:
                        print (row['customer'])
            else:
                print(serializer.errors)
                return Response("Not Done")

        except Exception as e:
            return Response(str(e)) 

