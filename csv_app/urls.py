from django.urls import path
from . import views
from .views import InvoiceUpload, uploadcsv



urlpatterns = [
    path('upload_file/', InvoiceUpload.as_view()),
    path('', views.uploadcsv, name='csv-home')
        
]