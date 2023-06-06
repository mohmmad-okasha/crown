from rest_framework import serializers
from . import models

#####################################################################################

class settings_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Settings
        fields = '__all__'

#####################################################################################

class flights_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Flights
        fields = '__all__'

#####################################################################################

class flight_dates_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Flight_dates
        fields = '__all__'

#####################################################################################
class hotels_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hotels
        fields = '__all__'

#####################################################################################
class rooms_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rooms
        fields = '__all__'

#####################################################################################

class room_dates_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room_dates
        fields = '__all__'

#####################################################################################
class bookings_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bookings
        fields = '__all__'

#####################################################################################

class accounts_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Accounts
        fields = '__all__'

#####################################################################################

class dashboard_buttons_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dashboard_buttons
        fields = '__all__'

#####################################################################################

class roles_serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Roles
        exclude = ('id', 'user_name')  # Specify the fields to exclude


#####################################################################################
