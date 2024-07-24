from django.db import models

    
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
    
    
    department = models.ForeignKey(Department,blank=False,null=False,on_delete=models.DO_NOTHING)
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
    
    register_number = models.CharField(max_length=12)
    name = models.CharField(max_length=50)
    Class = models.ForeignKey(Class, on_delete=models.DO_NOTHING)
    mode = models.CharField(choices=modeList,max_length=10)
    
    def __str__(self):
        return f"{self.register_number} - {self.name}"
    
    
    
class Staff(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    Class = models.ForeignKey(Class, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.name}"


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
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    Class = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    mode = models.CharField(max_length=10)
    status = models.CharField(max_length=10)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.Class}"
    