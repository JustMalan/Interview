from django.contrib import admin
from .models import Camp, ParentRegistration, Student, CampRegistration

admin.site.register(Camp)
admin.site.register(ParentRegistration)
admin.site.register(Student)
admin.site.register(CampRegistration)
