from django.shortcuts import render, HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import  Invoice
from .serializer import InvoiceSerializer
from rest_framework import status
from rest_framework.parsers import FileUploadParser

# Create your views here.
def home(request): 
    return render(request, 'base.html')


class InvoiceList(APIView):
    def get(self, request, format=None):
        all_invoices = Invoice.objects.all()
        serializers = InvoiceSerializer(all_invoices, many=True)
        return Response(serializers.data)

        # Uploading CSV
    def post(self, request, format=None):
        serializers = InvoiceSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class FileUploadView(APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        # ...
        # do some stuff with uploaded file
        # ...
        return Response(status=204)


