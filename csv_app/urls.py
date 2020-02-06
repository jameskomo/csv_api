from django.urls import path
from . import views
from .views import FileUploadView



urlpatterns = [
    path('', views.home, name='csv-home'),
    path('api/invoice/', views.InvoiceList.as_view()),
    # Upload CSV
    path('upload/<filename>/', FileUploadView.as_view())
        
]