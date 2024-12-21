from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        first_name = extra_fields.pop('first_name', 'Admin')
        last_name = extra_fields.pop('last_name', 'User')
        return self.create_user(
            email=email, 
            first_name=extra_fields.get('first_name', 'Admin'), 
            last_name=extra_fields.get('last_name', 'User'), 
            password=password, 
            **extra_fields
        )

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('principal', 'Principal'),
        ('hod', 'HOD'),
        ('staff', 'Staff'),
    )
    
    username = None  # Remove username field
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Ensure these are required

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Department(models.Model):

    departmentList = (
    ('SNH','Science and Humanities'),
    ('IT','Information Technology'),
    ('CSE','Computer Science and Engineering'),
    ('CSBS','Computer Science and Business Systems'),
    ('ECE','Electronics and communication Engineering'),
    ('AIML','Artificial Intelligence and Machine Learning')
    )

    department_name = models.CharField(max_length=4,choices=departmentList,blank=False,null=False)
    
    def __str__(self):
        return self.department_name
    
class Class(models.Model):
    semesterList=(
        ('I','1st Semester'),
        ('II','2nd Semester'),
        ('III','3rd Semester'),
        ('IV','4th Semester'),
        ('V','5th Semester'),
        ('VI','6th Semester'),
        ('VII','7th Semester'),
        ('VIII','8th Semester')
    )
    
    yearList=(
        ('I Year','1st Year'),
        ('II Year','2nd Year'),
        ('III Year','3rd Year'),
        ('IV Year','4th Year'),
    )
    
    sectionList=(
        ('A','A Section'),
        ('B','B Section'),
        ('C','C Section'),
    )
    
    
    department = models.ForeignKey(Department,blank=False,null=False,on_delete=models.CASCADE)
    year = models.CharField(max_length=8,choices=yearList)
    semester = models.CharField(max_length=4,choices=semesterList)
    section = models.CharField(max_length=1,choices=sectionList)
    
    def __str__(self):
        return f"{self.department} - {self.year} - {self.semester} Semester - {self.section} Section"
    
    
    
    
    
    
class Student(models.Model):
    modeList=(
        ('Hosteller','Hosteller'),
        ('Dayscholar','Dayscholar')
    )
    
    register_number = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=50)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    mode = models.CharField(choices=modeList,max_length=10)
    
    def __str__(self):
        return f"{self.register_number} - {self.name}"
    
    
    
class Staff(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Attendance(models.Model):
    
    date = models.DateField()
    department = models.CharField(max_length=4)
    semester = models.CharField(max_length=4)
    section = models.CharField(max_length=1)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.department} - {self.semester} - {self.section} ({self.date})"
    
class AttendanceReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    Class = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    mode = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    reason = models.TextField(blank=True, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.Class}"
    