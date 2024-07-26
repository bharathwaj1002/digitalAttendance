from datetime import timedelta
import json
from pyexpat.errors import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .import EmailBackend
from .models import *
from django.views.decorators.csrf import csrf_exempt
from .forms import DateSelectionForm
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, user_passes_test

def staff_required(view_func):
    decorated_view_func = user_passes_test(
        lambda user: user.is_authenticated and user.is_staff,
        login_url='/login/'
    )(view_func)
    return decorated_view_func

def login(request):
    return render(request,'login.html')

def doLogin(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Invalid Credentials, Verify your credentials')
            return redirect('login')
            
    else:
        return render(request,'login.html')

@csrf_exempt
def get_students(request):
    if request.method == 'POST':
        department_name = request.POST.get('department')
        semester = request.POST.get('semester')
        section = request.POST.get('section')

        try:
            # Retrieve the department instance based on the department name
            department = Department.objects.get(department_name=department_name)

            # Filter students based on class attributes
            students = Student.objects.filter(Class__department=department, Class__semester=semester, Class__section=section)
            
            # Prepare the data for response
            student_data = []
            for student in students:
                data = {
                    "id": student.register_number,
                    "name": student.name
                }
                student_data.append(data)

            return JsonResponse(student_data, safe=False)
        
        except Department.DoesNotExist:
            return JsonResponse({"error": "Department not found"}, status=400)
        
        except Exception as e:
            return JsonResponse({"error": "An error occurred: " + str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
def index(request):
    if request.user.is_staff:
        return redirect('hod_index')
    else:
        staff = get_object_or_404(Staff,email=request.user.email)
        
        students = Student.objects.filter(
            Class__department=staff.Class.department,
            Class__semester=staff.Class.semester,
            Class__section=staff.Class.section
        )
        
        students_count=students.count()
        present_count=0
        absent_count=0
        hosteller_absent_count=0
        dayscholar_absent_count=0
        
        od_ex_count=0
        hosteller_od_ex = 0
        dayscholar_od_ex = 0
        
        od_in_count=0
        hosteller_od_in = 0
        dayscholar_od_in = 0
        
        hosteller_od = 0
        dayscholar_od = 0
        
        total_present_count=0
        is_attendance_taken_today='No'
        current_date = timezone.now()

        if Attendance.objects.filter(date=current_date):
            is_attendance_taken_today = 'Yes'
            
            report = AttendanceReport.objects.filter(
                Class__department=staff.Class.department,
                Class__semester=staff.Class.semester,
                Class__section=staff.Class.section,
                date=timezone.now()
            )
            
            present_count = report.filter(status="Present").count()
            
            absent_count = report.filter(status="Absent").count()
            hosteller_absent_count = report.filter(status="Absent",mode="Hosteller").count()
            dayscholar_absent_count = report.filter(status="Absent",mode="Dayscholar").count()
            
            od_in_count = report.filter(status="On Duty Internal").count()
            hosteller_od_in = report.filter(status="On Duty Internal",mode="Hosteller").count()
            dayscholar_od_in = report.filter(status="On Duty Internal",mode="Dayscholar").count()
            
            od_ex_count = report.filter(status="On Duty External").count()
            hosteller_od_ex = report.filter(status="On Duty External",mode="Hosteller").count()
            dayscholar_od_ex = report.filter(status="On Duty External",mode="Dayscholar").count()
            
            hosteller_od = hosteller_od_in+hosteller_od_ex
            dayscholar_od = dayscholar_od_in+dayscholar_od_ex
            
            total_present_count = present_count+od_in_count+od_ex_count
            
        consecutive_absent_students_data =[]
        consecutive_absent_students=[]
        
        students = Student.objects.filter(
            Class__department=staff.Class.department,
            Class__semester=staff.Class.semester,
            Class__section=staff.Class.section
        )
        
        # Fetch attendance reports for the last three days including today
        for student in students:
            # Get the last three attendance records for the student
            last_three_attendances = AttendanceReport.objects.filter(
                student=student,
                Class__department=staff.Class.department,
                Class__semester=staff.Class.semester,
                Class__section=staff.Class.section
            ).order_by('-date')[:3]

            # Check if all three records have status 'Absent'
            if last_three_attendances.count() == 3 and all(att.status == 'Absent' for att in last_three_attendances):
                
                consecutive_absent_students_data.append(student)

        for student in consecutive_absent_students_data:
            data = {
                'id':student.register_number,
                'name':student.name,
            }
            consecutive_absent_students.append(data)
            
        
        context = {
                'count':students_count,
                'present':present_count,
                'absent':absent_count,
                'hosteller_absent_count':hosteller_absent_count,
                'dayscholar_absent_count':dayscholar_absent_count,
                'OD_IN':od_in_count,
                'OD_EX':od_ex_count,
                'hosteller_od':hosteller_od,
                'dayscholar_od':dayscholar_od,
                'total_present':total_present_count,
                'is_attendance_taken_today':is_attendance_taken_today,
                'consecutive_absent_students':consecutive_absent_students
            }

        return render(request,'index.html',context)

@staff_required
def hod_index(request):
    staff = get_object_or_404(Staff,email=request.user.email)
    attendances = []
    classes = []
    students = Student.objects.filter(
        Class__department=staff.department
    )
    
    students_count=students.count()
    present_count=0
    
    absent_count=0
    hosteller_absent_count=0
    dayscholar_absent_count=0
    
    od_ex_count=0
    hosteller_od_ex = 0
    dayscholar_od_ex = 0
    
    od_in_count=0
    hosteller_od_in = 0
    dayscholar_od_in = 0
    
    total_od_count=0
    hosteller_od = 0
    dayscholar_od = 0
    
    total_present_count=0
    is_attendance_taken_today='No'
    current_date = timezone.now()
    classes_query_set = Class.objects.filter(department=staff.department)
    for item in classes_query_set:
        data = {
                'semester':item.semester,
                'section':item.section,
                'status':"Yet to note"
            }
        classes.append(data)

    if Attendance.objects.filter(date=current_date):
        is_attendance_taken_today = 'Yes'
        
        attendances = Attendance.objects.filter(department=staff.department)
        attendances_query_set = Attendance.objects.filter(department=staff.department,date=timezone.now())
        
        for item in attendances_query_set:
            for classItem in classes:
                if item.semester == classItem['semester']:
                    classItem['status'] = 'Noted'
        
        report = AttendanceReport.objects.filter(
            Class__department=staff.department,
            date=timezone.now()
        )
        
        present_count = report.filter(status="Present").count()
        
        absent_count = report.filter(status="Absent").count()
        hosteller_absent_count = report.filter(status="Absent",mode="Hosteller").count()
        dayscholar_absent_count = report.filter(status="Absent",mode="Dayscholar").count()
        
        od_in_count = report.filter(status="On Duty Internal").count()
        hosteller_od_in = report.filter(status="On Duty Internal",mode="Hosteller").count()
        dayscholar_od_in = report.filter(status="On Duty Internal",mode="Dayscholar").count()
        
        od_ex_count = report.filter(status="On Duty External").count()
        hosteller_od_ex = report.filter(status="On Duty External",mode="Hosteller").count()
        dayscholar_od_ex = report.filter(status="On Duty External",mode="Dayscholar").count()
        
        hosteller_od = hosteller_od_in+hosteller_od_ex
        dayscholar_od = dayscholar_od_in+dayscholar_od_ex
        
        total_present_count = present_count+od_in_count+od_ex_count
        total_od_count = od_in_count+od_ex_count
        
    consecutive_absent_students_data =[]
    consecutive_absent_students=[]
    
    students = Student.objects.filter(
        Class__department=staff.department
    )
    
    # Fetch attendance reports for the last three days including today
    for student in students:
        # Get the last three attendance records for the student
        last_three_attendances = AttendanceReport.objects.filter(
            student=student,
            Class__department=staff.department,
        ).order_by('-date')[:3]

        # Check if all three records have status 'Absent'
        if last_three_attendances.count() == 3 and all(att.status == 'Absent' for att in last_three_attendances):
            
            consecutive_absent_students_data.append(student)

    for student in consecutive_absent_students_data:
        data = {
            'id':student.register_number,
            'name':student.name,
        }
        consecutive_absent_students.append(data)
        
    
    context = {
            'count':students_count,
            'present':present_count,
            'absent':absent_count,
            'hosteller_absent_count':hosteller_absent_count,
            'dayscholar_absent_count':dayscholar_absent_count,
            'OD_IN':od_in_count,
            'OD_EX':od_ex_count,
            'hosteller_od':hosteller_od,
            'dayscholar_od':dayscholar_od,
            'total_present':total_present_count,
            'total_od_count':total_od_count,
            'is_attendance_taken_today':is_attendance_taken_today,
            'consecutive_absent_students': consecutive_absent_students,
            'attendances': attendances,
            'classes': classes
        }
    
    return render(request,'hod_index.html',context)


def students_info(request):
    staff = get_object_or_404(Staff, email=request.user.email)
    students_data = []
    students = Student.objects.filter(
        Class__department=staff.Class.department,
        Class__semester=staff.Class.semester,
        Class__section=staff.Class.section
    )
    students_data.append(students)
    
    if Attendance(date=timezone.now(), department=staff.Class.department, semester=staff.Class.semester, section=staff.Class.section):
        date = timezone.now()
        students = AttendanceReport.objects.filter(Class__department=staff.Class.department,Class__semester=staff.Class.semester,Class__section=staff.Class.section,date=date)
        for student in students:
            students_data.append(student)

    context = {
        'students': students_data
    }

    return render(request, 'student_info.html', context)


def staff_take_attendance(request):
    staff = Staff.objects.filter(email=request.user.email)
    is_attendance_taken_today='No'
    current_date = timezone.now()
    if Attendance.objects.filter(date=current_date):
        is_attendance_taken_today = 'Yes'
    else:
        is_attendance_taken_today = 'No'
    
    context = {
        'staffs':staff,
        'is_attendance_taken_today':is_attendance_taken_today
    }

    return render(request, 'staff_take_attendance.html', context)


    
@csrf_exempt
def save_attendance(request):
    if request.method == 'POST':
        try:
            student_data = request.POST.get('register_numbers')
            date = request.POST.get('date')
            department = request.POST.get('department')
            semester = request.POST.get('semester')
            section = request.POST.get('section')

            # Parse the JSON data
            students = json.loads(student_data)

            # Create an attendance record (adjust based on your model)
            attendance = Attendance(date=date, department=department, semester=semester, section=section)
            attendance.save()

            # Save each student's attendance record
            for student_dict in students:
                student = get_object_or_404(Student, register_number=student_dict.get('id'))
                attendance_report = AttendanceReport(student=student, Class=attendance, status=student_dict.get('status'),date=date,mode=student.mode)
                attendance_report.save()

            return HttpResponse('OK')

        except Exception as e:

            return JsonResponse({'status': 'Error', 'message': str(e)}, status=500, safe=False)

    return JsonResponse({'status': 'Error', 'message': 'Invalid request method'}, status=400, safe=False)

@csrf_exempt
def get_attendance(request):
    staff = get_object_or_404(Staff,email=request.user.email)
    attendances = Attendance.objects.filter(department=staff.Class.department,semester=staff.Class.semester,section=staff.Class.section)
    attendance_data = []
    for attendance in attendances:
        data = {
            "id": attendance.date,
            "date":attendance.date
        }
        attendance_data.append(data)
    
    return JsonResponse(attendance_data, safe=False)

@csrf_exempt
def hod_get_attendance(request):
    staff = get_object_or_404(Staff,email=request.user.email)
    attendances = Attendance.objects.filter(department=staff.department,semester=request.POST['semester'],section=request.POST['section'])
    attendance_data = []
    for attendance in attendances:
        data = {
            "id": attendance.date,
            "date":attendance.date
        }
        attendance_data.append(data)
    
    return JsonResponse(attendance_data, safe=False)

@csrf_exempt
def get_attendance_report(request):
    staff = get_object_or_404(Staff,email=request.user.email)
    date = request.POST.get('attendance_date_id')
    attendance_reports = AttendanceReport.objects.filter(Class__department=staff.Class.department,Class__semester=staff.Class.semester,Class__section=staff.Class.section,date=date)
    attendance_report_data = []
    for attendance_report in attendance_reports:
        data = {
            "id": attendance_report.student.register_number,
            "name": attendance_report.student.name,
            "date": date,
            "status":attendance_report.status
        }
        attendance_report_data.append(data)
    
    return JsonResponse(attendance_report_data, safe=False)

@csrf_exempt
def hod_get_attendance_report(request):
    staff = get_object_or_404(Staff,email=request.user.email)
    date = request.POST.get('attendance_date_id')
    attendance_reports = AttendanceReport.objects.filter(Class__department=staff.department,Class__semester=request.POST['semester'],Class__section=request.POST['section'],date=date)
    attendance_report_data = []
    for attendance_report in attendance_reports:
        data = {
            "id": attendance_report.student.register_number,
            "name": attendance_report.student.name,
            "date": date,
            "semester": attendance_report.student.Class.semester,
            "section": attendance_report.student.Class.section,
            "status":attendance_report.status
        }
        attendance_report_data.append(data)
    
    return JsonResponse(attendance_report_data, safe=False)
    

def staff_view_attendance(request):
    staff = get_object_or_404(Staff, email=request.user.email)
    department = staff.Class.department
    semester = staff.Class.semester
    section = staff.Class.section
    context = {
        'department': department,
        'semester': semester,
        'section': section,
        'page_title': 'Update Attendance'
    }

    return render(request, 'staff_view_attendance.html', context)

def hod_view_attendance(request):
    staff = get_object_or_404(Staff, email=request.user.email)
    department = staff.department
    context = {
        'department': department,
    }

    return render(request, 'hod_view_attendance.html', context)


def get_consecutive_absent_students(request):
    staff = get_object_or_404(Staff, email=request.user.email)
    
    consecutive_absent_students_data =[]
    consecutive_absent_students=[]
    
    students = Student.objects.filter(
        Class__department=staff.Class.department,
        Class__semester=staff.Class.semester,
        Class__section=staff.Class.section
    )
    
    # Fetch attendance reports for the last three days including today
    for student in students:
        # Get the last three attendance records for the student
        last_three_attendances = AttendanceReport.objects.filter(
            student=student,
            Class__department=staff.Class.department,
            Class__semester=staff.Class.semester,
            Class__section=staff.Class.section
        ).order_by('-date')[:3]

        # Check if all three records have status 'Absent'
        if last_three_attendances.count() == 3 and all(att.status == 'Absent' for att in last_three_attendances):
            
            consecutive_absent_students_data.append(student)

    for student in consecutive_absent_students_data:
        data = {
            'id':student.register_number,
            'name':student.name,
        }
        consecutive_absent_students.append(data)
        
    return JsonResponse(consecutive_absent_students,safe=False)

def logout(request):
    auth.logout(request)
    return redirect('login')