from django.urls import path
from . import views
app_name = 'pdfdata'

urlpatterns = [
    path('', views.pdfdata, name= 'pdfdata'),
    path('upload/', views.download_pdf, name='uploaddata'),
]
