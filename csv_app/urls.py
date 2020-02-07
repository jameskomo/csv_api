from django.urls import path
from . import views
from .views import InvoiceUploadAPIView, uploadcsv



urlpatterns = [
    path('upload_file/', InvoiceUploadAPIView.as_view(), name="api-upload"),
    path('', views.uploadcsv, name='csv-home')
        
]