from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass


from django.db import models


class AccreditationBody(models.Model):
    name = models.CharField(max_length=100, unique=True)
    abbreviation = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    headquarters_location = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # Other accreditation body-related fields
    # ...

    def __str__(self):
        return self.name


class Scholarship(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    eligibility_criteria = models.TextField()
    award_amount = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    contact_email = models.EmailField()

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    established_year = models.PositiveIntegerField()
    registration_number = models.CharField(max_length=20, unique=True)
    logo = models.ImageField(upload_to='institution_logos/', blank=True, null=True)

    scholarships_offered = models.ManyToManyField(Scholarship, related_name='scholarship_institutions')
    accreditations_offered = models.ManyToManyField(AccreditationBody, related_name="authorized_institutions") 

    affiliation_documents = models.FileField(upload_to='affiliation_documents/')


    def __str__(self):
        return self.name
    

class Student(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    enrollment_number = models.CharField(max_length=20, unique=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_phone = models.CharField(max_length=15, blank=True, null=True)

    academic_records = models.FileField(upload_to='academic_records/')


    def __str__(self):
        return self.full_name


'''
class VerificationStatus(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.full_name}'s Verification Status"


class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])

    def __str__(self):
        return f"{self.student.full_name}'s {self.scholarship.name} Application"
'''

    

