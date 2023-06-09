from rest_framework import serializers
from API.models import Data

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = "__all__"
        read_only_fields = ('id', 'timestep','owner')