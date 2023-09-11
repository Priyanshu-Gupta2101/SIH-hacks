from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(PersonalDetail)
admin.site.register(ContactDetail)
admin.site.register(GuardianDetail)
admin.site.register(Student)