from django.db import models



#####################################################################################

class Bookings(models.Model):
    book_date = models.DateTimeField(max_length=50)
    persons_number = models.IntegerField()
    persons_names = models.CharField(max_length=200)
    kids_number = models.IntegerField(default=0)
    kids_names = models.CharField(max_length=200,blank=True)
    kids_ages = models.CharField(max_length=200,blank=True)
    hotel = models.CharField(max_length=50)
    dates = models.CharField(max_length=100)
    out_date = models.CharField(max_length=100,blank=True)
    room_id = models.CharField(max_length=50)
    room_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    notes=models.CharField(max_length=100,blank=True)
    user = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return self.id #to change object name in admin table

    class Meta:
        ordering= ['id'] #to Sort the values

#####################################################################################

class Hotels(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)  
    city = models.CharField(max_length=50)
    area = models.CharField(max_length=50,blank=True)
    rate = models.CharField(max_length=50)
    allotment = models.IntegerField()
    notes=models.CharField(max_length=100,blank=True)
    user = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return self.name #to change object name in admin table

    class Meta:
        ordering= ['id'] #to Sort the values

#####################################################################################

class Rooms(models.Model):
    id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(Hotels, on_delete=models.CASCADE)
    room_id = models.CharField(max_length=50)  
    room_categ = models.CharField(max_length=50,blank=True)#ROOM CATEGORY
    room_type = models.CharField(max_length=50)
    meals = models.CharField(max_length=50,blank=True)
    persons = models.IntegerField()#persons number
    range = models.CharField(max_length=1000)
    notes=models.CharField(max_length=100,blank=True)
    user = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return self.room_id #to change object name in admin table

    class Meta:
        ordering= ['id'] #to Sort the values
#####################################################################################

class Room_dates(models.Model):
    room_id = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    date = models.CharField(max_length=50)

    class Meta:
        ordering = ['date']

#####################################################################################

class Flights(models.Model):
    code = models.CharField(max_length=50)
    airline = models.CharField(max_length=50)
    from_airport = models.CharField(max_length=50)
    to_airport = models.CharField(max_length=50)
    departure_date = models.DateTimeField(max_length=50)
    arrival_date=models.DateTimeField(max_length=50)
    seats=models.IntegerField()
    status=models.CharField(max_length=100)
    notes=models.CharField(max_length=100,blank=True)
    user = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return self.code #to change object name in admin table

    class Meta:
        ordering= ['id'] #to Sort the values

#####################################################################################

class Airlines(models.Model):
    name = models.CharField(max_length=50,unique=True)
    def __str__(self):
        return self.name #to change object name in admin table

    class Meta:
        ordering= ['id'] #to Sort the values

#####################################################################################
STATUS_ENABLED = (
    (0, "Disabled"),
    (1, "Enabled")
)

class Airports(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering= ['id']

#####################################################################################

class Flight_dates(models.Model):
    flight_id=models.IntegerField()
    departure_date = models.DateTimeField(max_length=50)
    arrival_date=models.DateTimeField(max_length=50)


    def __str__(self):
        return self.flight_id #to change object name in admin table

    class Meta:
        ordering= ['flight_id'] #to Sort the values

#####################################################################################

class Accounts(models.Model):
    parent = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    debit = models.FloatField(max_length=10,null=True)
    credit = models.FloatField(max_length=10,null=True)
    user = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.name #to change object name in admin table

    class Meta:
        ordering= ['id'] #to Sort the values

#####################################################################################

class Dashboard_buttons(models.Model):
    title = models.CharField(max_length=50)
    url = models.CharField(max_length=50)
    icon = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.title #to change object name in admin table

    class Meta:
        ordering= ['id'] #to Sort the values

#####################################################################################
from django.contrib.auth.models import User

class Roles(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    users = models.IntegerField(default=0)
    bookings = models.IntegerField(default=0)
    hotels = models.IntegerField(default=0)
    available_hotel = models.IntegerField(default=0)
    hotels_report = models.IntegerField(default=0)
    backups = models.IntegerField(default=0)
    logs = models.IntegerField(default=0)
    flights = models.IntegerField(default=0)

#####################################################################################

class Settings(models.Model):
    dark_mode = models.BooleanField()
    lang = models.CharField(max_length=50)
    primary_color = models.CharField(max_length=50)
    back_color = models.CharField(max_length=50)

#####################################################################################
class SecondDBManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('second_db')
    
class Logs(models.Model):
    log = models.CharField(max_length=500)
    user_name = models.CharField(max_length=50)
    time = models.DateTimeField(max_length=50)

#####################################################################################

from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


#####################################################################################
