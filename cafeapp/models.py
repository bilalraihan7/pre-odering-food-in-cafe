from django.db import models
from django.urls import path


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    image=models.ImageField(upload_to='drimg/',default='nothing')
    address=models.CharField(max_length=100,default='nothing')
    phone=models.IntegerField(default='1')
    def __str__(self):
        return self.name




class Driver(models.Model):
    name = models.CharField(max_length=100)
    email=models.CharField(max_length=50,default='nothing')
    license = models.ImageField(upload_to='license/',default='nothing')
    password =models.CharField(max_length=18,default='nothing')
    image=models.ImageField(upload_to='drimg/',default='nothing')
    address=models.CharField(max_length=100,default='nothing')
    phone=models.IntegerField(default='1')
    status=models.CharField(max_length=20,default='Not Verified')
    is_verified = models.BooleanField('Is Verified', default=False)
    def __str__(self):
        return self.name



class vehicle(models.Model):
    userid=models.ForeignKey(Driver,on_delete=models.CASCADE)
    vehicle_name = models.CharField(max_length=100)
    vehicle_reg = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=500)
    vehicle_image = models.ImageField(upload_to="vehicles/", blank=True)
    rate=models.IntegerField(null=True)
    status=models.CharField(max_length=20,default="not booked")
    
    
    def __str__(self):
        return self.vehicle_name

class booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    vehicle=models.ForeignKey(vehicle, on_delete=models.CASCADE,null=True,blank=True)
    time=models.TimeField(auto_now=True)
    date=models.DateField(auto_now=True)
    pickup_location = models.CharField(max_length=100)
    dropoff_location = models.CharField(max_length=100)
    distance=models.IntegerField(blank=True,null=True)

class Payment(models.Model):
    bookid=models.ForeignKey(booking,on_delete=models.CASCADE)
    cname=models.CharField(max_length=25)
    amount=models.IntegerField()
    cardno=models.IntegerField()
    cvv=models.IntegerField()