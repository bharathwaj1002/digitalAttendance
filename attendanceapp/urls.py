from django.urls import path
from .import views

urlpatterns=[
    path('',views.index,name='index'),
    path('hod_index',views.hod_index,name='hod_index'),
    path('principal_index',views.principal_index,name='principal_index'),
    
    
    path('login',views.login,name='login'),
    path('doLogin',views.doLogin,name='doLogin'),
    
    
    path('staff_take_attendance',views.staff_take_attendance,name='staff_take_attendance'),
    path('staff_update_attendance',views.staff_update_attendance,name='staff_update_attendance'),
    
    
    path('staff_view_attendance',views.staff_view_attendance,name='staff_view_attendance'),
    path('hod_view_attendance',views.hod_view_attendance,name='hod_view_attendance'),
    path('principal_view_attendance',views.principal_view_attendance,name='principal_view_attendance'),
    
    
    path('get_attendance_report',views.get_attendance_report,name='get_attendance_report'),
    path('hod_get_attendance_report',views.hod_get_attendance_report,name='hod_get_attendance_report'),
    path('principal_get_attendance_report',views.principal_get_attendance_report,name='principal_get_attendance_report'),
    
    
    path('get_students',views.get_students,name='get_students'),
    
    
    path('students_info',views.students_info,name='students_info'),
    path('hod_students_info',views.hod_students_info,name='hod_students_info'),
    path('principal_students_info',views.principal_students_info,name='principal_students_info'),
    
    path('present_student_info',views.present_students_info,name='present_student_info'),
    path('hod_present_student_info',views.hod_present_students_info,name='hod_present_student_info'),
    path('principal_present_student_info',views.principal_present_students_info,name='hod_present_student_info'),
    
    path('absent_student_info',views.absent_students_info,name='absent_student_info'),
    path('hod_absent_student_info',views.hod_absent_students_info,name='hod_present_student_info'),
    path('principal_absent_student_info',views.principal_absent_students_info,name='hod_present_student_info'),
    
    path('hod_od_student_info',views.hod_od_students_info,name='hod_od_student_info'),
    path('principal_od_student_info',views.principal_od_students_info,name='od_student_info'),
    
    
    path('get_consecutive_absent_students',views.get_consecutive_absent_students,name='get_consecutive_absent_students'),
    
    
    path('get_attendance',views.get_attendance,name='get_attendance'),
    path('hod_get_attendance',views.hod_get_attendance,name='hod_get_attendance'),
    path('principal_get_attendance',views.principal_get_attendance,name='principal_get_attendance'),
    
    
    path('save_attendance',views.save_attendance,name='save_attendance'),
    
    
    path('logout',views.logout,name='logout'),
    
]