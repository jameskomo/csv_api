from django.urls import path
from . import views
from .views import InvoiceUpload



urlpatterns = [
    path('upload_file/', InvoiceUpload.as_view())
        
]