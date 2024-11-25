from django.urls import path
from . import views
app_name = 'pdfdata'

urlpatterns = [
    path('', views.pdfdata, name= 'pdfdata'),
    path('download/', views.download_all_pdf, name='uploaddata'),
    
]
