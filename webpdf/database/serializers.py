from rest_framework import serializers
from .models import VanBan
from .models import Data

class VanBanSerializer(serializers.ModelSerializer):
    class Meta:
        model = VanBan
        fields = '__all__' 

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = '__all__'  # Bao gồm tất cả các trường của model