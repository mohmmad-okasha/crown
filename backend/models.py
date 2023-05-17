from django.db import models


#####################################################################################

class Bookings(models.Model):
    book_date = models.DateTimeField(max_length=50)
    guest_name = models.CharField(max_length=50)
    hotel = models.CharField(max_length=50)
    dates = models.CharField(max_length=100)
    room_id = models.CharField(max_length=50)
    room_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    guests=models.CharField(max_length=100,blank=True)
    notes=models.CharField(max_length=100,blank=True)
    user = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return self.id #to change object name in admin table

    class Meta:
        ordering= ['id'] #to Sort the values


#####################################################################################

class Rooms(models.Model):
    hotel = models.CharField(max_length=50)
    room_id = models.CharField(max_length=50)
    room_type = models.CharField(max_length=50)
    dates = models.CharField(max_length=1000)
    notes=models.CharField(max_length=100,blank=True)
    user = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return self.room_id #to change object name in admin table

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["hotel", "room_id"],
                name="unique_room_for_hotel",
            ),
        ]
        ordering= ['id'] #to Sort the values

#####################################################################################

class Room_dates(models.Model):
    room_id=models.IntegerField(max_length=100)
    date = models.DateField(max_length=50)


    def __str__(self):
        return self.room_id #to change object name in admin table

    class Meta:
        ordering= ['date'] #to Sort the values

#####################################################################################

class Flights(models.Model):
    code = models.CharField(max_length=50)
    airline = models.CharField(max_length=50)
    from_airport = models.CharField(max_length=50)
    to_airport = models.CharField(max_length=50)
    departure_date = models.DateTimeField(max_length=50)
    arrival_date=models.DateTimeField(max_length=50)
    seats=models.IntegerField(max_length=100)
    status=models.CharField(max_length=100)
    notes=models.CharField(max_length=100,blank=True)
    user = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return self.code #to change object name in admin table

    class Meta:
        ordering= ['id'] #to Sort the values

#####################################################################################

class Flight_dates(models.Model):
    flight_id=models.IntegerField(max_length=100)
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

class Settings(models.Model):
    dark_mode = models.BooleanField()
    lang = models.CharField(max_length=50)
    primary_color = models.CharField(max_length=50)
    back_color = models.CharField(max_length=50)

#####################################################################################
