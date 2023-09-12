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


class InstituteDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=20, blank=True, null=True)
    established_year = models.PositiveIntegerField()
    registration_number = models.CharField(max_length=20, unique=True)
    website = models.URLField(blank=True, null=True)

class ContactDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

class InstituteDoc(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='institution_logo/', blank=True, null=True)
    scholarships_offered = models.ManyToManyField(Scholarship, related_name='scholarship_institutions')
    accredited_by = models.ManyToManyField(AccreditationBody, related_name="authorized_institutions") 
    affiliation_document = models.FileField(upload_to='affiliation_document/')


class Institution(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institute_detail = models.ForeignKey(InstituteDetail, on_delete=models.CASCADE,blank=True, null=True)
    contact_detail = models.ForeignKey(ContactDetail, on_delete=models.CASCADE, blank=True, null=True)
    institution_doc = models.ForeignKey(InstituteDoc, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
    

class PersonalDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    enrollment_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()




class GuardianDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_phone = models.CharField(max_length=15, blank=True, null=True)
    guardian_email = models.EmailField(blank=True, null=True)
    guardian_gender = models.CharField(max_length=10, blank=True, null=True)

class FileDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/')
    signature = models.ImageField(upload_to='signature/')
    #aadhaar_no = models.CharField(max_length=12, unique=True)
    aadhaar = models.FileField(upload_to='aadhaar_card/')
    income_cert = models.FileField(upload_to='income_certificate/', blank=True, null=True)


class Student(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, null=True)
    personal_detail = models.ForeignKey(PersonalDetail, on_delete=models.CASCADE, blank=True, null=True)
    contact_detail = models.ForeignKey(ContactDetail, on_delete=models.CASCADE, blank=True, null=True)
    guardian_detail = models.ForeignKey(GuardianDetail, on_delete=models.CASCADE, blank=True, null=True)
    file_detail = models.ForeignKey(FileDetail, on_delete=models.CASCADE, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.username}'s Profile with {self.personal_detail.enrollment_number}"


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

    

