from rest_framework import serializers
from .models import WeatherSearch

class WeatherSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherSearch
        fields = '__all__'