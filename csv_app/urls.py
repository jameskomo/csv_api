from django.urls import path
from . import views
from .views import InvoiceUploadAPIView, uploadcsv



urlpatterns = [
    path('upload_file/', InvoiceUploadAPIView.as_view()),
    path('', views.uploadcsv, name='csv-home')
        
]