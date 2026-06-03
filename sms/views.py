from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile, Staff, Student

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        
        if user is not None:
            login(request, user)
            user_uuid = user.userprofile.user_uuid
            role = user.userprofile.role
            
            if role == 'admin':
                return redirect('admin_dashboard', user_uuid=user_uuid)
            elif role == 'staff':
                return redirect('staff_dashboard', user_uuid=user_uuid)
            elif role == 'student':
                return redirect('student_dashboard', user_uuid=user_uuid)
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'sms/login.html')

def admin_dashboard(request, user_uuid):
    if not request.user.is_authenticated or str(request.user.userprofile.user_uuid) != str(user_uuid) or request.user.userprofile.role != 'admin':
        return redirect('login_view')
        
    teachers = Staff.objects.all()
    context = {
        'teachers': teachers,
        'user_uuid': user_uuid
    }
    return render(request, 'sms/admin_dashboard.html', context)

def create_user_action(request, user_uuid):
    if not request.user.is_authenticated or str(request.user.userprofile.user_uuid) != str(user_uuid) or request.user.userprofile.role != 'admin':
        return redirect('login_view')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role')

        new_user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        UserProfile.objects.create(user=new_user, role=role)

        if role == 'staff':
            section = request.POST.get('section')
            Staff.objects.create(user=new_user, section=section)
            messages.success(request, f"Staff account successfully created for {username}!")
            
        elif role == 'student':
            parent_name = request.POST.get('parent_name')
            section = request.POST.get('section')
            teacher_id = request.POST.get('class_teacher')
            
            teacher_instance = Staff.objects.get(id=teacher_id) if teacher_id else None
            Student.objects.create(user=new_user, parent_name=parent_name, section=section, class_teacher=teacher_instance)
            messages.success(request, f"Student account successfully created for {username}!")

        return redirect('admin_dashboard', user_uuid=user_uuid)

def staff_dashboard(request, user_uuid):
    if not request.user.is_authenticated or str(request.user.userprofile.user_uuid) != str(user_uuid) or request.user.userprofile.role != 'staff':
        return redirect('login_view')
        
    staff_member = request.user.staff
    allocated_students = staff_member.my_students.all()
    
    context = {
        'section': staff_member.section,
        'students': allocated_students,
        'total_students': allocated_students.count(),
        'user_uuid': user_uuid
    }
    return render(request, 'sms/staff_dashboard.html', context)


def student_dashboard(request, user_uuid):
    if not request.user.is_authenticated or str(request.user.userprofile.user_uuid) != str(user_uuid) or request.user.userprofile.role != 'student':
        return redirect('login_view')
        
    student_details = request.user.student
    return render(request, 'sms/student_dashboard.html', {'student': student_details, 'user_uuid': user_uuid})

def user_logout(request):
    logout(request)
    return redirect('login_view')

