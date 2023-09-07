from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass


class Institution(models.Model):
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=20, unique=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    affiliation_documents = models.FileField(upload_to='affiliation_documents/')
    # Other institution-related fields

    def __str__(self):
        return self.name
    

class Student(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    enrollment_number = models.CharField(max_length=20, unique=True)
    academic_records = models.FileField(upload_to='academic_records/')
    # Other student-related fields

    def __str__(self):
        return self.full_name


class VerificationStatus(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    # Other fields to track verification status

    def __str__(self):
        return f"{self.student.full_name}'s Verification Status"


class Scholarship(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    eligibility_criteria = models.TextField()
    # Other scholarship-related fields

    def __str__(self):
        return self.name
    

class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])
    # Other application-related fields

    def __str__(self):
        return f"{self.student.full_name}'s {self.scholarship.name} Application"




