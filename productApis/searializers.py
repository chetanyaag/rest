from rest_framework import serializers
from .models import *

class ProductDataSearializer(serializers.ModelSerializer):

    class Meta:
        model = ProductData
        fields = '__all__'
