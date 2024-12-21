

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.shortcuts import redirect
from django.urls import path
from unfold.admin import ModelAdmin
from .models import User, Department, Class, Student, Staff, Attendance, AttendanceReport
from django.contrib.auth.models import Group
from django.contrib import messages
from django.views.generic import TemplateView
from unfold.views import UnfoldModelAdminViewMixin



admin.site.unregister(Group)
@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Customize list display
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

    # Fieldsets for the detail view
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name')}),
        ('Personal Info', {'fields': ('role',)}),
    )

    # Fieldsets for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'role'),
        }),
    )

    # Search functionality
    search_fields = ('email',)
    ordering = ('email',)

    # Make 'role' a required field
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['role'].required = True
        return form


@admin.register(Department)
class DepartmentAdmin(ModelAdmin):
    list_display = ('department_name',)
    search_fields = ('department_name',)


@admin.register(Class)
class ClassAdmin(ModelAdmin):
    list_display = ('department', 'year', 'semester', 'section')
    list_filter = ('department', 'year', 'semester', 'section')
    search_fields = ('department__department_name',)



@admin.register(Student)
class StudentAdmin(ModelAdmin):
    list_display = ('register_number', 'name', 'Class', 'mode')
    list_filter = ('Class', 'mode')
    search_fields = ('register_number', 'name')


@admin.register(Staff)
class StaffAdmin(ModelAdmin):
    list_display = ('user', 'department', 'Class')
    list_filter = ('department', 'Class')
    search_fields = ('user__first_name', 'user__last_name', 'department__department_name')


@admin.register(Attendance)
class AttendanceAdmin(ModelAdmin):
    list_display = ('date', 'department', 'semester', 'section', 'created_at', 'updated_at')
    list_filter = ('department', 'semester', 'section', 'date')
    search_fields = ('department', 'semester', 'section')


@admin.register(AttendanceReport)
class AttendanceReportAdmin(ModelAdmin):
    list_display = ('student', 'Class', 'mode', 'status', 'date', 'created_at', 'updated_at')
    list_filter = ('Class', 'mode', 'status', 'date')
    search_fields = ('student__name', 'Class__department')
