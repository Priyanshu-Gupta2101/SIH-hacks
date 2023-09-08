from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Scholarship_DB(models.Model):
    id = models.AutoField(primary_key=True)
    scholarship_name = models.CharField(max_length=100, null=False)
    conditions = models.JSONField(default=dict)
    state_specific = models.BooleanField()
    state_name = models.CharField(max_length=50, null=True)
    date_added = models.DateTimeField(auto_now=True)
    
    def _str_(self):
        return self.scholarship_name

    
class student_details(models.Model):
    student_username = models.CharField(max_length=50, null= False ,primary_key=True)
    student_name = models.CharField(max_length=50, null= False)
    student_DOB = models.DateField()
    student_gender = models.CharField(max_length=20, null=True)
    student_father = models.CharField(max_length=30, null=False)
    student_mother = models.CharField(max_length=30, null=False)
    student_phoneno = models.IntegerField(max_length=10)
    student_email = models.EmailField()
    student_address = models.CharField(max_length=50)
    student_city = models.CharField(max_length=30)
    student_state =models.CharField(max_length=30)
    student_pincode = models.IntegerField(max_length=6)

