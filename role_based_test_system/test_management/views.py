from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Test, Student, School, Marks
from django.contrib.auth.models import User
from django.http import JsonResponse


# -------------------------------
# General Views
# -------------------------------
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def edit_marks(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    students = Student.objects.filter(test=test)
    
    if request.method == 'POST':
        for student in students:
            mark_key = f"mark_{student.id}"
            if mark_key in request.POST:
                student.marks = request.POST[mark_key]
                student.save()
        return redirect('collector_dashboard')
    
    return render(request, 'edit_marks.html', {'test': test, 'students': students})
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


from django.shortcuts import redirect

@login_required
def dashboard(request):
    role = request.user.userprofile.role
    if role == 'collector':
        return redirect('collector_dashboard')
    elif role == 'school':
        return redirect('school_dashboard')
    elif role == 'other':
        return redirect('other_dashboard')
    return redirect('login')



# -------------------------------
# Collector Views
# -------------------------------
@login_required
def collector_dashboard(request):
    if request.user.userprofile.role != 'collector':
        return redirect('dashboard')
    tests = Test.objects.all()
    return render(request, 'collector_dashboard.html', {'tests': tests})


@login_required
def add_test(request):
    if request.user.userprofile.role != 'collector':
        return redirect('dashboard')
    if request.method == 'POST':
        Test.objects.create(
            name=request.POST['name'],
            subject=request.POST['subject'],
            date=request.POST['date'],
            question_file=request.FILES['question_file'],
            answer_file=request.FILES['answer_file'],
            created_by=request.user,
            active=True
        )
        return redirect('collector_dashboard')
    return render(request, 'add_test.html')


@login_required
def toggle_test_status(request, test_id):
    if request.user.userprofile.role != 'collector':
        return redirect('dashboard')
    test = get_object_or_404(Test, id=test_id)
    test.active = not test.active
    test.save()
    return redirect('collector_dashboard')


@login_required
def student_ranking(request):
    if request.user.userprofile.role != 'collector':
        return redirect('dashboard')
    rankings = Marks.objects.select_related('student', 'student__school').order_by('-marks')
    return render(request, 'ranking.html', {'rankings': rankings})


@login_required
def student_report(request):
    if request.user.userprofile.role != 'collector':
        return redirect('dashboard')
    total_students = Student.objects.count()
    return render(request, 'report.html', {'total_students': total_students})


# -------------------------------
# School Views
# -------------------------------
@login_required
def test_list(request):
    if request.user.userprofile.role != 'school':
        return redirect('dashboard')
    
    active_tests = Test.objects.filter(active=True)
    
    return render(request, 'test_list.html', {'tests': active_tests})
@login_required
def school_dashboard(request):
    if request.user.userprofile.role != 'school':
        return redirect('dashboard')
    students = Student.objects.filter(school__created_by=request.user)
    return render(request, 'school_dashboard.html', {'students': students})


from django.shortcuts import get_object_or_404

@login_required
def add_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        roll_number = request.POST.get('roll_number')
        if name and roll_number:
            Student.objects.create(name=name, roll_number=roll_number)
            return redirect('add_student')
    
    students = Student.objects.all()
    return render(request, 'add_student.html', {'students': students})
    if request.user.userprofile.role != 'school':
        return redirect('dashboard')
    
    try:
        school = School.objects.get(created_by=request.user)
    except School.DoesNotExist:
        return render(request, 'error.html', {'message': 'No school associated with this account. Please contact admin.'})
    
    if request.method == 'POST':
        Student.objects.create(
            name=request.POST['name'],
            roll_number=request.POST['roll_number'],
            school=school
        )
        return redirect('school_dashboard')
    
    return render(request, 'add_student.html')


@login_required
def edit_student(request, student_id):
    if request.user.userprofile.role != 'school':
        return redirect('dashboard')
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        student.name = request.POST['name']
        student.roll_number = request.POST['roll_number']
        student.save()
        return redirect('school_dashboard')
    return render(request, 'edit_student.html', {'student': student})


@login_required
def delete_student(request, student_id):
    if request.user.userprofile.role != 'school':
        return redirect('dashboard')
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('school_dashboard')


from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Test, Marks
@login_required
def add_marks(request):
    students = Student.objects.all()
    tests = Test.objects.all()
    marks = Marks.objects.all()
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        test_id = request.POST.get('test_id')
        marks_value = request.POST.get('marks')
        
        student = get_object_or_404(Student, id=student_id)
        test = get_object_or_404(Test, id=test_id)
        
        # Create or Update Mark Entry
        mark_entry, created = Marks.objects.update_or_create(
            student=student,
            test=test,
            defaults={'marks': marks_value}
        )
        return redirect('add_marks')
    
    return render(request, 'add_marks.html', {
        'students': students,
        'tests': tests,
        'marks': marks
    })
@login_required
def edit_student_mark(request, mark_id):
    mark = get_object_or_404(Marks, id=mark_id)
    
    if request.method == 'POST':
        new_marks = request.POST.get('marks')
        mark.marks = new_marks
        mark.save()
        return redirect('add_marks')
    
    return render(request, 'edit_student_mark.html', {'mark': mark})


def delete_student_mark(request, mark_id):
    mark = get_object_or_404(Marks, id=mark_id)
    mark.delete()
    return redirect('add_marks')

@login_required
def student_list(request):
    if request.user.userprofile.role != 'school':
        return redirect('dashboard')
    students = Student.objects.filter(school__created_by=request.user).prefetch_related('marks_set')
    return render(request, 'student_list.html', {'students': students})


# -------------------------------
# Other Role Views
# -------------------------------
@login_required
def other_dashboard(request):
    return render(request, 'other_dashboard.html')


@login_required
def top_students(request):
    if request.user.userprofile.role != 'other':
        return redirect('dashboard')
    top_students = Marks.objects.select_related('student').order_by('-marks')[:3]
    return render(request, 'top_students.html', {'top_students': top_students})
