from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImageViewSet 
from . import views

router = DefaultRouter()
router.register(r'images', ImageViewSet)

app_name = 'get_image'
urlpatterns = [
    path('', include(router.urls)),
    path('get_image/',views.get_image, name ='get_image'),
]