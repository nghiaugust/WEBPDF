from django.urls import path
from .views import UploadPDFView, ConvertPDFView, GetConvertedPDFView

urlpatterns = [
    #path('upload/', UploadPDFView.as_view(), name='upload_pdf'),
    path('convert/<int:pk>/', ConvertPDFView.as_view(), name='convert_pdf'),
    #path('get/<int:pk>/', GetConvertedPDFView.as_view(), name='get_converted_pdf'),
]