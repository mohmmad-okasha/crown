# get data from model ---> json

from rest_framework import serializers
from .models import Users
from .models import Customers
from .models import Test_model

# class users_ser(serializers.ModelSerializer):
#     class Meta:
#         model = Users
#         fields = '__all__'

class flights_serializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = '__all__'


# class test_ser(serializers.ModelSerializer):
#     class Meta:
#         model = Test_model
#         fields = '__all__'

