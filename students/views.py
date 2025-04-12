import datetime
from django.shortcuts import render, get_object_or_404
from .models import PrimaryStudent, SchoolSetting, SecondaryStudent, SeniorSecondaryStudent,Teacher
from django.db.models import Q
from .utils import generate_teacher_card_pdf  # Import the function that generates the teacher card
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

#card generating
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import inch
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
import qrcode
import os
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from students.models import PrimaryStudent, SecondaryStudent, SeniorSecondaryStudent

#the form part for the studens 
from django.shortcuts import render, redirect
from .models import PrimaryStudent, SecondaryStudent, SeniorSecondaryStudent,Subject
from .forms import PrimaryStudentForm, SecondaryStudentForm, SeniorSecondaryStudentForm





@login_required
def home(request):
    setting, created = SchoolSetting.objects.get_or_create(id=1)  # Ensure a single setting exists
    
    # Get student counts
    primary_count = PrimaryStudent.objects.count()
    secondary_count = SecondaryStudent.objects.count()
    senior_secondary_count = SeniorSecondaryStudent.objects.count()
    total_students = primary_count + secondary_count + senior_secondary_count  # Overall total
    
      # Re-registered counts
    re_registered_secondary = SecondaryStudent.objects.filter(re_registered=True).count()
    re_registered_senior = SeniorSecondaryStudent.objects.filter(re_registered=True).count()

    # New admissions count
    new_secondary = secondary_count - re_registered_secondary
    new_senior = senior_secondary_count - re_registered_senior
#is for the new addes student
    current_year = datetime.date.today().year
    newly_added_primary_count = PrimaryStudent.objects.filter(admission_number__startswith=str(current_year)).count()


    # Comparison
    secondary_vs_senior_diff = secondary_count - senior_secondary_count

    
    return render(request, 'students/home.html', {
        'primary_count': primary_count,
        'secondary_count': secondary_count,
        'senior_secondary_count': senior_secondary_count,
        'total_students': total_students,
        'max_students': setting.max_students,
        "re_registered_secondary": re_registered_secondary,
        "re_registered_senior": re_registered_senior,
        "new_secondary": new_secondary,
        "new_senior": new_senior,
        "secondary_vs_senior_difference": secondary_vs_senior_diff,
        "newly_added_primary_count": newly_added_primary_count, 
    })
    

from django.shortcuts import render
from .models import SchoolSetting, PrimaryStudent, SecondaryStudent, SeniorSecondaryStudent

def primary_students(request):
    students = PrimaryStudent.objects.all()
    setting, created = SchoolSetting.objects.get_or_create(id=1)  # Ensure a single setting exists
    total_students = students.count()
    
    return render(request, 'students/primary_students.html', {
        'students': students,
        'total_students': total_students,
        'max_students': setting.max_students
    })

def secondary_students(request):
    students = SecondaryStudent.objects.all()
    setting, created = SchoolSetting.objects.get_or_create(id=1)  # Ensure a single setting exists
    total_students = students.count()
    
    return render(request, 'students/secondary_students.html', {
        'students': students,
        'total_students': total_students,
        'max_students': setting.max_students
    })

def senior_secondary_students(request):
    students = SeniorSecondaryStudent.objects.all()
    setting, created = SchoolSetting.objects.get_or_create(id=1)  # Ensure a single setting exists
    total_students = students.count()
    
    return render(request, 'students/senior_secondary_students.html', {
        'students': students,
        'total_students': total_students,
        'max_students': setting.max_students
    })

#adding the subject list for the views
def subjects(request):
    subjects = Subject.objects.all()
    return render(request, 'students/subject_list.html', {'subjects': subjects})
#teachers card
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Teacher

# View to display all teachers
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'students/teacher_list.html', {'teachers': teachers})

# View to display a single teacher's details
def teacher_detail(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    return render(request, 'students/teacher_detail.html', {'teacher': teacher})

# View to generate a teacher card as PDF
def generate_teacher_card_view(request, teacher_id):
    return generate_teacher_card_pdf(request, teacher_id)


#this is the query search for the student 
def primary_students(request):
    setting, created = SchoolSetting.objects.get_or_create(id=1)    
    query = request.GET.get('q', '')  # Get the search query from the request
    if query:
        students = PrimaryStudent.objects.filter(
            first_name__icontains=query
        ) | PrimaryStudent.objects.filter(
            last_name__icontains=query
        ) | PrimaryStudent.objects.filter(
            grades__name__icontains=query  # Fix: Using ForeignKey lookup correctly
        )
    else:
        students = PrimaryStudent.objects.all()
    student_count = students.count()  # Count the number of students
    classes = CLASS.objects.all()
    return render(request, 'students/primary_students.html', 
    {'students': students, 
    'student_count': student_count,
    'max_students': setting.max_students,
    'classes':classes})



def secondary_students(request):
    setting, created = SchoolSetting.objects.get_or_create(id=1) 
    query = request.GET.get('q', '')  # Get the search query from the request
    if query:
        students = SecondaryStudent.objects.filter(
            first_name__icontains=query
        ) | SecondaryStudent.objects.filter(
            last_name__icontains=query
        ) | SecondaryStudent.objects.filter(
            grades__name__icontains=query  # Fix: Using ForeignKey lookup correctly
        )
    else:
        students = SecondaryStudent.objects.all()
    student_count = students.count()# Count the number of students
    classes = CLASS.objects.all()
    return render(request, 'students/secondary_students.html',
    {'students': students,
     'student_count': student_count,
     'max_students': setting.max_students,
     'classes':classes})





def senior_secondary_students(request):
    setting, created = SchoolSetting.objects.get_or_create(id=1)
    query = request.GET.get('q', '')  # Get the search query from the request
    if query:
        students = SeniorSecondaryStudent.objects.filter(
            first_name__icontains=query
        ) | SeniorSecondaryStudent.objects.filter(
            last_name__icontains=query
        ) | SeniorSecondaryStudent.objects.filter(
            grades__name__icontains=query  # Fix: Using ForeignKey lookup correctly
        )
    else:
        students = SeniorSecondaryStudent.objects.all()
    student_count = students.count()
    classes = CLASS.objects.all()# Count the number of students
    return render(request, 'students/senior_secondary_students.html',
    {'students': students,
    'student_count': student_count,
    "max_students":setting.max_students,
    'classes':classes})


def subjects(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    if query:
        subjects = Subject.objects.filter(
            Q(name__icontains=query) 
          
        )
    else:
        subjects = Subject.objects.all()
    subject_count = subjects.count()  # Count the number of students
    return render(request, 'students/subject_list.html', {'subjects': subjects, 'subject_count': subject_count})




#teachers query
def teacher_list(request):
    query = request.GET.get('q', '')  # Get the search query parameter
    if query:
        # Search across first name, last name, contact, and subjects
        teachers = Teacher.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(contact__icontains=query) |
            Q(subjects__name__icontains=query)  # For related subjects
        ).distinct()  # Remove duplicates due to subjects relationship
    else:
        teachers = Teacher.objects.all()
    teachers_count = teachers.count()
    classes = CLASS.objects.all()
    return render(request, 'students/teacher_list.html',
                  {'teachers': teachers, 
                   'query': query,
                   'teachers_count':teachers_count,
                   'classes':classes})







#the section is to geneerate the student cards and teachers cards
def generate_student_card(request, level, student_id):
    try:
        # Fetch the student based on the level
        if level == 'primary':
            student = PrimaryStudent.objects.get(pk=student_id)
        elif level == 'secondary':
            student = SecondaryStudent.objects.get(pk=student_id)
        elif level == 'senior_secondary':
            student = SeniorSecondaryStudent.objects.get(pk=student_id)
        else:
            return HttpResponse("Invalid level", status=400)
    except (PrimaryStudent.DoesNotExist, SecondaryStudent.DoesNotExist, SeniorSecondaryStudent.DoesNotExist):
        return HttpResponse("Student not found", status=404)

    # Define card size (3.375 x 2.125 inches, standard ID card size)
    card_width, card_height = 3.375 * inch, 2.125 * inch

    # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.first_name}_{student.last_name}_Student_Card.pdf"'

    # Create a canvas with card dimensions
    p = canvas.Canvas(response, pagesize=(card_width, card_height))

    # White background
    p.setFillColor(colors.white)
    p.rect(0, 0, card_width, card_height, stroke=0, fill=1)  # Fill the card with white

    # Add a dark blue bottom line
    p.setFillColor(colors.darkblue)
    p.rect(0, 0, card_width, 10, stroke=0, fill=1)  # 10 points high dark blue line at the bottom

    # Add the school logo
    school_logo_path = os.path.join(settings.STATIC_ROOT, '1.png')
    if os.path.exists(school_logo_path):
        logo = ImageReader(school_logo_path)
        
        p.drawImage(logo, 10, card_height - 60, width=40, height=40)  # Position and size for the logo

    # Title: "Student Card"
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(colors.black)
    p.drawString(70, card_height - 40, "Jubilee International ")

    # Label: "Student ID"
    p.setFont("Helvetica-Bold", 9)
    p.setFillColor(colors.darkblue)
    p.drawString(10, card_height - 80, "Student ID:")

    # Student details
    p.setFont("Helvetica", 9)
    p.setFillColor(colors.black)
    p.drawString(10, card_height - 95, f"Admission No: {student.admission_number}")
    p.drawString(10, card_height - 110, f"Name: {student.first_name} {student.last_name}")
    p.drawString(10, card_height - 125, f"Grade: {student.grades}")

    p.drawString(10, card_height - 140, f"Contact: {student.parent_contact}")
    p.drawString(10, card_height - 155, f"Parent Contact: {student.parent_contact}")

    # Add the student's photo
    if student.image and student.image.name:
        photo_path = os.path.join(settings.MEDIA_ROOT, student.image.name)
        if os.path.exists(photo_path):
            photo = ImageReader(photo_path)
            p.drawImage(photo, card_width - 70, card_height - 100, width=50, height=50)  # Position and size for the photo
    else:
        p.setFont("Helvetica", 8)
        p.setFillColor(colors.red)
        p.drawString(card_width - 70, card_height - 90, "No Photo")

    # Generate QR code with student info
    qr_data = f"Name: {student.first_name} {student.last_name}\n" \
              f"Admission No: {student.admission_number}\n" \
              f"Grade: {student.grades}\n" \
             f"Level: {level.capitalize()}"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=4, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Save QR code to a temporary path
    qr_temp_path = os.path.join(settings.MEDIA_ROOT, "temp_qr.png")
    qr_img.save(qr_temp_path)

    # Add QR code to the card
    if os.path.exists(qr_temp_path):
        qr_code_img = ImageReader(qr_temp_path)
        p.drawImage(qr_code_img, card_width - 70, 10, width=40, height=40)  # Position and size for the QR code

    # Clean up temporary QR code file
    if os.path.exists(qr_temp_path):
        os.remove(qr_temp_path)

    # Finalize PDF
    p.showPage()
    p.save()

    return response





#this is the edit and delete forms for the students
from django.shortcuts import render, redirect, get_object_or_404
from .models import PrimaryStudent, SecondaryStudent, SeniorSecondaryStudent
from .forms import PrimaryStudentForm, SecondaryStudentForm, SeniorSecondaryStudentForm

# Edit Primary Student
def edit_primary_student(request, pk):
    student = get_object_or_404(PrimaryStudent, pk=pk)
    if request.method == "POST":
        form = PrimaryStudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('primary_students')
    else:
        form = PrimaryStudentForm(instance=student)
        
    classes = CLASS.objects.all()     
    return render(request, 'students/edit_primary.html', {'form': form, 'title': 'Edit Primary Student','classes':classes})

# Edit Secondary Student
def edit_secondary_student(request, pk):
    student = get_object_or_404(SecondaryStudent, pk=pk)
    if request.method == "POST":
        form = SecondaryStudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('secondary_students')
    else:
        form = SecondaryStudentForm(instance=student)
        
    classes = CLASS.objects.all()
    return render(request, 'students/edit_secondary.html', {'form': form, 'title': 'Edit Secondary Student','classes':classes})

# Edit Senior Secondary Student
def edit_senior_student(request, pk):
    student = get_object_or_404(SeniorSecondaryStudent, pk=pk)
    if request.method == "POST":
        form = SeniorSecondaryStudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('senior_secondary_students')
    else:
        form = SeniorSecondaryStudentForm(instance=student)
        
    classes = CLASS.objects.all()
    return render(request, 'students/edit_senior.html', {'form': form, 'title': 'Edit Senior Student','classes':classes})
# edith subject


def edit_subject(request, pk):
    subjects = get_object_or_404(Subject, pk = pk)
    if request.method == "POST":
         form = SubjectForm(request.POST, request.FILES, instance=subjects)
         if form.is_valid():
             form.save()
             return redirect('subject_list')
    else:
        form = SubjectForm(instance=subjects)
    
    return render(request, 'students/edit_subject.html',{'form': form, 'title': 'edit subject'})


# Delete Primary Student
def delete_primary_student(request, pk):
    student = get_object_or_404(PrimaryStudent, pk=pk)
    if request.method == "POST":
        student.delete()
        return redirect('primary_students')
    return render(request, 'students/confirm_delete.html', {'student': student})

# Delete Secondary Student
def delete_secondary_student(request, pk):
    student = get_object_or_404(SecondaryStudent, pk=pk)
    if request.method == "POST":
        student.delete()
        return redirect('secondary_students')
    return render(request, 'students/delete_secondary.html', {'student': student})

# Delete Senior Secondary Student
def delete_senior_student(request, pk):
    student = get_object_or_404(SeniorSecondaryStudent, pk=pk)
    if request.method == "POST":
        student.delete()
        return redirect('senior_secondary_students')
    classes = CLASS.objects.all()
    return render(request, 'students/delete_senior.html', {'student': student,'classes':classes})




def delete_subject(request, pk):
    subjects = get_object_or_404(Subject, pk=pk)
    if request.method == "POST":
        subjects.delete()
        return redirect('subject_list')
    return render(request, 'students/delete_subject.html',{'subjects':subjects})

#is other part is creating teachers
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from .models import Teacher
from .forms import TeacherForm,SubjectForm


#adding subject vews
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject_list')  # Redirect to the subject list view
    else:
        form = SubjectForm()
    
    return render(request, 'students/add_subject.html', {'form': form})
                
            
        



# Create a new teacher
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher created successfully!")
            return redirect('teacher_list')  # Redirect to teacher list or another page
    else:
        
        form = TeacherForm()
  
    return render(request, 'students/add_teachers.html', {'form': form,})

# Edit an existing teacher
from django.shortcuts import render, get_object_or_404, redirect
from .models import Teacher
from .forms import TeacherForm

def edit_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    if request.method == "POST":
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')  # Redirect to teacher list
    else:
        form = TeacherForm(instance=teacher)

    return render(request, 'students/edit_teacher.html', {'form': form, 'teacher': teacher, 'title': 'Edit Teacher'})

# Delete a teacher
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, "Teacher deleted successfully!")
        return redirect('teacher_list')  # Redirect to teacher list or another page
    return render(request, 'students/delete_teacher.html', {'teacher': teacher})











#cuatom user login 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
@csrf_protect
def login_view(request):
    """Login for admin users (student_admin or teacher_admin)."""
    if request.method == 'POST':
        username = request.POST.get('username')  # ✅ Use .get() to avoid KeyError
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)  # 🔹 Authenticate user

        if user is not None:
            auth_login(request, user)  # ✅ Use Django's built-in login function

            # Redirect based on role
            if user.role == 'student_admin':
                return redirect('home')
            elif user.role == 'superadmin':
                return redirect('update_registration_limit')# Redirect to Student Admin Dashboard
            else:
                return render(request, 'students/login.html', {'error': 'Unauthorized access!'})
        else:
            return render(request, 'students/login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'students/login.html')

# Logout View
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
  
        logout(request)
        return redirect('/')  # Redirect after logout



#a vies to add limit to the student registration 
from django.shortcuts import render, redirect
from .models import SchoolSetting
from django.contrib import messages


# this is to display the total student and student limit
#djeson files for the dashboard
from django.http import JsonResponse
from .models import PrimaryStudent, SecondaryStudent, SeniorSecondaryStudent

def student_data(request):
    # Total counts
    primary_count = PrimaryStudent.objects.count()
    secondary_count = SecondaryStudent.objects.count()
    senior_count = SeniorSecondaryStudent.objects.count()

    # Re-registered counts
    re_registered_secondary = SecondaryStudent.objects.filter(re_registered=True).count()
    re_registered_senior = SeniorSecondaryStudent.objects.filter(re_registered=True).count()

    # New admissions count
    new_secondary = secondary_count - re_registered_secondary
    new_senior = senior_count - re_registered_senior
#is for the new addes student
    current_year = datetime.date.today().year
    newly_added_primary_count = PrimaryStudent.objects.filter(admission_number__startswith=str(current_year)).count()


    # Comparison
    secondary_vs_senior_diff = secondary_count - senior_count

    data = {
        "primary_count": primary_count,
        "secondary_count": secondary_count,
        "senior_count": senior_count,
        "re_registered_secondary": re_registered_secondary,
        "re_registered_senior": re_registered_senior,
        "new_secondary": new_secondary,
        "new_senior": new_senior,
        "secondary_vs_senior_difference": secondary_vs_senior_diff,
        "newly_added_primary_count": newly_added_primary_count, 
        "max_students": 5000,  # Adjust if necessary
    }
    return JsonResponse(data)

#this is fo student updatel limit
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SchoolSetting
from .forms import SchoolSettingForm


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SchoolSetting

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SchoolSetting, PrimaryStudent, SecondaryStudent, SeniorSecondaryStudent

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SchoolSetting, PrimaryStudent, SecondaryStudent, SeniorSecondaryStudent

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SchoolSetting, PrimaryStudent, SecondaryStudent, SeniorSecondaryStudent
@login_required
def update_registration_limit(request):
    # Ensure a single SchoolSetting object exists
    setting, created = SchoolSetting.objects.get_or_create(id=1)

    if request.method == 'POST':
        max_students = request.POST.get('max_students')

        # Validate input (check if it's not None and is a digit)
        if max_students and max_students.isdigit() and int(max_students) > 0:
            setting.max_students = int(max_students)
            setting.save()
            messages.success(request, "Registration limit updated successfully!")
            return redirect('update_registration_limit')  # Redirect to avoid form resubmission
        else:
            messages.error(request, "Please enter a valid positive number for the limit.")

    # Get current student counts
    primary_count = PrimaryStudent.objects.count()
    secondary_count = SecondaryStudent.objects.count()
    senior_secondary_count = SeniorSecondaryStudent.objects.count()
    total_students = primary_count + secondary_count + senior_secondary_count

    return render(request, 'students/update_student_registrations.html', {
        'setting': setting,
        'primary_count': primary_count,
        'secondary_count': secondary_count,
        'senior_secondary_count': senior_secondary_count,
        'total_students': total_students
    })




from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import PrimaryStudentForm, SecondaryStudentForm, SeniorSecondaryStudentForm

def add_primary_student(request):
    form = PrimaryStudentForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Primary Student added successfully!")
                return redirect('add_primary_student')
            except Exception as e:
                messages.error(request, str(e))
               
    classes = CLASS.objects.all()
    return render(request, "students/add_primary.html", {"form": form, "title": "Add Primary Student",'classes':classes})

def add_secondary_student(request):
    form = SecondaryStudentForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Secondary Student added successfully!")
                return redirect('add_secondary_student')
            except Exception as e:
                messages.error(request, str(e))
    classes = CLASS.objects.all()
    return render(request, "students/add_secondary.html", {"form": form, "title": "Add Secondary Student",'classes':classes})

def add_senior_student(request):
    form = SeniorSecondaryStudentForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Senior Secondary Student added successfully!")
                return redirect()
            except Exception as e:
                messages.error(request, str(e))
    classes = CLASS.objects.all()
    return render(request, "students/add_senior.html", {"form": form, "title": "Add Senior Secondary Student",'classes':classes})




#THS IS THE GRADE LIST 

from django.shortcuts import render, redirect
from .models import CLASS
from .forms import GradeForm

def add_class(request):
    grades = CLASS.objects.all()
    form = GradeForm()

    if request.method == "POST":
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_list')  # Redirect after saving to avoid re-posting

    return render(request, 'students/add_class.html', {'form': form, 'grades': grades})


def class_list(request):
    classes = CLASS.objects.all()
    return render(request, 'students/class_list.html',{'classes':classes})

from django.shortcuts import render, get_object_or_404, redirect
from .models import CLASS

def delete_class(request, pk):
    class_instance = get_object_or_404(CLASS, pk=pk)
    
    if request.method == "POST":
        class_instance.delete()
        return redirect('class_list')

    return render(request, 'students/delete_class.html', {'class_instance': class_instance})



def edit_class(request, pk):
    classes = get_object_or_404(CLASS, pk = pk)
    if request.method == "POST":
         form = GradeForm(request.POST, request.FILES, instance=classes)
         if form.is_valid():
             form.save()
             return redirect('class_list')
    else:
        form = GradeForm(instance=classes)
    return render(request, 'students/edit_class.html',{'form': form, 'title': 'edit subject'})




def class_list(request):
    query = request.GET.get('q', '')  # Get the search query from the request
    if query:
        classes = CLASS.objects.filter(
            Q(name__icontains=query) 
          
        )
    else:
        classes = CLASS.objects.all()
    class_count = classes.count()  # Count the number of students
    return render(request, 'students/class_list.html', {'classes': classes, 'class_count': class_count})

#this views is the student registration form

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import PrimaryStudent, SecondaryStudent, SeniorSecondaryStudent
from .forms import PrimaryToSecondaryForm, SecondaryToSeniorForm

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db import IntegrityError
from students.models import PrimaryStudent, SecondaryStudent, CLASS
from students.forms import PrimaryToSecondaryForm

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db import IntegrityError
from students.models import PrimaryStudent, SecondaryStudent, CLASS
from students.forms import PrimaryToSecondaryForm

def re_register_primary_to_secondary(request):
    if request.method == "POST":
        form = PrimaryToSecondaryForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            # Get student from PrimaryStudent
            primary_student = get_object_or_404(PrimaryStudent, first_name=first_name, last_name=last_name)

            # Check if the student is already registered in SecondaryStudent
            if SecondaryStudent.objects.filter(admission_number=primary_student.admission_number).exists():
                messages.error(request, "This student is already registered in Secondary School.")
                return redirect('secondary_students')

            try:
                # Create new SecondaryStudent entry
                secondary_student = form.save(commit=False)
                secondary_student.admission_number = primary_student.admission_number  # Keep same admission number
                secondary_student.first_name = primary_student.first_name  # Pre-fill first name
                secondary_student.last_name = primary_student.last_name  # Pre-fill last name
                secondary_student.date_of_birth = primary_student.date_of_birth  # Pre-fill date of birth
                secondary_student.parent_contact = primary_student.parent_contact  # Pre-fill parent contact
                secondary_student.address = primary_student.address  # Pre-fill address
                secondary_student.re_registered = True  
                secondary_student.save()

                messages.success(request, "Student successfully re-registered in Secondary School.")
                return redirect('secondary_students')

            except IntegrityError:
                messages.error(request, "A student with this admission number already exists.")
                return redirect('secondary_students')

    else:
        form = PrimaryToSecondaryForm()

    classes = CLASS.objects.all()
    return render(request, 'students/re_register_primary_to_secondary.html', {'form': form, 'classes': classes})

def re_register_secondary_to_senior(request):
    if request.method == "POST":
        form = SecondaryToSeniorForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            # Get student from SecondaryStudent
            secondary_student = get_object_or_404(SecondaryStudent, first_name=first_name, last_name=last_name)

            # Create new SeniorSecondaryStudent entry
            senior_student = form.save(commit=False)
            senior_student.admission_number = secondary_student.admission_number  # Keep same admission number
            senior_student.re_registered = True
            senior_student.save()

            messages.success(request, "Student successfully re-registered in Senior Secondary School.")
            return redirect('senior_secondary_students')

    else:
        form = SecondaryToSeniorForm()
    classes = CLASS.objects.all()
    return render(request, 'students/re_register_secondary_to_senior.html', {'form': form,'classes':classes})


#this a select to delete 
def delete_selected_students(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist('selected_students')  # Get selected student IDs
        if selected_ids:
            PrimaryStudent.objects.filter(pk__in=selected_ids).delete()
            messages.success(request, "Selected students deleted successfully!")
        else:
            messages.error(request, "No students selected.")
    return redirect('primary_students')


#this a select to delete 
def delete_selected_primary(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist('selected_students')  # Get selected student IDs
        if selected_ids:
            PrimaryStudent.objects.filter(pk__in=selected_ids).delete()
            messages.success(request, "Selected students deleted successfully!")
        else:
            messages.error(request, "No students selected.")
    return redirect('primary_students')


#this a select to delete 
def delete_selected_secondary(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist('selected_students')  # Get selected student IDs
        if selected_ids:
            SecondaryStudent.objects.filter(pk__in=selected_ids).delete()
            messages.success(request, "Selected students deleted successfully!")
        else:
            messages.error(request, "No students selected.")
    return redirect('secondary_students')


#this a select to delete 
def delete_selected_senior(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist('selected_students')  # Get selected student IDs
        if selected_ids:
            SeniorSecondaryStudent.objects.filter(pk__in=selected_ids).delete()
            messages.success(request, "Selected students deleted successfully!")
        else:
            messages.error(request, "No students selected.")
    return redirect('senior_secondary_students')



#this a select to delete 
def delete_selected_teacher(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist('selected_teachers')  # Get selected student IDs
        if selected_ids:
            Teacher.objects.filter(pk__in=selected_ids).delete()
            messages.success(request, "Selected teachers deleted successfully!")
        else:
            messages.error(request, "No students selected.")
    return redirect('teacher_list')

#this a select to delete 
def delete_selected_subject(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist('selected_subject')  # Get selected student IDs
        if selected_ids:
            Subject.objects.filter(pk__in=selected_ids).delete()
            messages.success(request, "Selected subject deleted successfully!")
        else:
            messages.error(request, "No subject selected.")
    return redirect('subject_list')

def delete_selected_class(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist('selected_classes')  # Get selected student IDs
        if selected_ids:
            CLASS.objects.filter(pk__in=selected_ids).delete()
            messages.success(request, "Selected classes deleted successfully!")
        else:
            messages.error(request, "No class selected.")
    return redirect('class_list')
