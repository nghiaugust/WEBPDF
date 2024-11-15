from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import LoginUser

router = DefaultRouter()
router.register('users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginUser.as_view(), name='login'),
]