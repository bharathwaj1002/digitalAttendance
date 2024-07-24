from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
# Register your models here.
admin.site.unregister(Group)

admin.site.register(Department)
admin.site.register(Class)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)