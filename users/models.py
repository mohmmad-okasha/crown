from django.db import models
#from django.contrib.auth.models import User


class Test_model(models.Model):
    a = models.CharField(max_length=1)
    b = models.CharField(max_length=50)

class Users(models.Model):
    name = models.CharField(max_length=25)
    user_name = models.CharField(max_length=20)
    mobile = models.CharField(max_length=15,default="0")
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    img=models.ImageField(default='1.jpg',blank=True)

    def __str__(self):
        return self.user_name # change object name in admin table

    class Meta:
        ordering= ['id'] #to Sort the values

class Customers(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    id_type = models.CharField(max_length=50)
    id_number = models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    notes=models.CharField(max_length=100)
    img=models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.name # change object name in admin table

    class Meta:
        ordering= ['id'] #to Sort the values