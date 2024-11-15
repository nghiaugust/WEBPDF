from django.urls import path
from . import views
app_name = 'add_data'
urlpatterns = [
    path('', views.add_data, name='add_data'),
    path('get_data/',views.get_data, name ='get_data'),
]   