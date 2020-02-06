from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import CreateAPIView
from .serializer import InvoiceFile_Serializer
from rest_framework.views import APIView
from rest_framework.response import Response

class InvoiceUpload(APIView):
    serializer_class = InvoiceFile_Serializer
    parser_classes = [ MultiPartParser,FormParser ]

    def post(self,request):
        try:
            serializer = InvoiceFile_Serializer(data=request.data)
            print(serializer.initial_data)

            if serializer.is_valid():
                print(serializer.data)
                return Response("Done")
            else:
                print(serializer.errors)
                return Response("Not Done")

        except Exception as e:
            return Response(str(e)) 

        
