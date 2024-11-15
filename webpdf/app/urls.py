from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'home'

router = DefaultRouter()
router.register('dulieu',views.DuLieuViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
