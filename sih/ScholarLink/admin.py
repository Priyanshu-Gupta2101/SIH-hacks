from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(PersonalDetail)
admin.site.register(ContactDetail)
admin.site.register(GuardianDetail)
admin.site.register(FileDetail)
admin.site.register(Student)
admin.site.register(Institution)
admin.site.register(InstituteDetail)
admin.site.register(InstituteDoc)
admin.site.register(AccreditationBody)
admin.site.register(Scholarship)