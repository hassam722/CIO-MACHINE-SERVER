from django.db import models
# Create your models here.

class user(models.Model):
    id = models.IntegerField(primary_key= True,auto_created =True)
    username = models.TextField(unique = True)
    nfcnum = models.BigIntegerField(null = True,unique = True)

class user_data(models.Model):
    date = models.DateField()
    checkintime = models.TimeField()
    checkouttime = models.TimeField(null = True)
    timediff = models.TimeField(null = True)
    userid = models.ForeignKey(user,on_delete = models.CASCADE)