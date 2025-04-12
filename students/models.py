from django.db import models
import datetime
from django.forms import ValidationError
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _




#this model is for grade
class CLASS(models.Model):  
    name = models.CharField(max_length=50, unique=True)  # e.g., "Grade 1", "Grade 2", "Primary"
    
    def __str__(self):
        return self.name

class SchoolSetting(models.Model):
    max_students = models.PositiveIntegerField(default=1000)  # Set default limit

    def __str__(self):
        return f"Max Students Allowed: {self.max_students}"






def get_next_admission_number():
    """Generate the next unique admission number across all student levels."""
    from .models import PrimaryStudent, SecondaryStudent, SeniorSecondaryStudent

    current_year = datetime.date.today().year

    # Get the highest admission number from all three student models
    last_primary = PrimaryStudent.objects.order_by('-admission_number').first()
    last_secondary = SecondaryStudent.objects.order_by('-admission_number').first()
    last_senior = SeniorSecondaryStudent.objects.order_by('-admission_number').first()

    # Extract last admission numbers
    last_numbers = [
        int(s.admission_number[-3:]) for s in [last_primary, last_secondary, last_senior] if s and s.admission_number.isdigit()
    ]
    
    next_number = max(last_numbers) + 1 if last_numbers else 1  # Start at 001 if no students exist

    return f"{current_year}{next_number:03d}"

class PrimaryStudent(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    grades = models.ForeignKey(CLASS, on_delete=models.CASCADE, related_name="primary_students", null=True, blank=True)
    date_of_birth = models.DateField()
    parent_contact = models.CharField(max_length=15)
    address = models.TextField()
    admission_number = models.CharField(max_length=10, unique=True, blank=True)
    image = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    documents = models.FileField(upload_to='student_documents/', blank=True, null=True)

    def save(self, *args, **kwargs):
        from .models import SchoolSetting, SecondaryStudent, SeniorSecondaryStudent

        max_students = SchoolSetting.objects.first().max_students if SchoolSetting.objects.exists() else 5000
        total_students = (
            PrimaryStudent.objects.count() +
            SecondaryStudent.objects.count() +
            SeniorSecondaryStudent.objects.count()
        )

        if total_students >= max_students:
            raise ValidationError(f"Cannot add student. Maximum limit of {max_students} students reached.")

        if not self.admission_number:
            self.admission_number = get_next_admission_number()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Grade {self.grades})"

class SecondaryStudent(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    grades = models.ForeignKey(CLASS, on_delete=models.CASCADE, related_name="secondary_students", null=True, blank=True)
    date_of_birth = models.DateField()
    parent_contact = models.CharField(max_length=15)
    address = models.TextField()
    admission_number = models.CharField(max_length=10, unique=True, blank=True)
    image = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    documents = models.FileField(upload_to='student_documents/', blank=True, null=True)
    re_registered = models.BooleanField(default=False) 

    def save(self, *args, **kwargs):
        from .models import SchoolSetting, PrimaryStudent, SeniorSecondaryStudent

        max_students = SchoolSetting.objects.first().max_students if SchoolSetting.objects.exists() else 5000
        total_students = (
            PrimaryStudent.objects.count() +
            SecondaryStudent.objects.count() +
            SeniorSecondaryStudent.objects.count()
        )

        if total_students >= max_students:
            raise ValidationError(f"Cannot add student. Maximum limit of {max_students} students reached.")

        # If student exists in PrimaryStudent, reuse admission number
        existing_student = PrimaryStudent.objects.filter(first_name=self.first_name, last_name=self.last_name).first()

        if existing_student:
            self.admission_number = existing_student.admission_number
        elif not self.admission_number:
            self.admission_number = get_next_admission_number()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Grade {self.grades})"

class SeniorSecondaryStudent(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    grades = models.ForeignKey(CLASS, on_delete=models.CASCADE, related_name="senior_secondary_students", null=True, blank=True)
    date_of_birth = models.DateField()
    parent_contact = models.CharField(max_length=15)
    address = models.TextField()
    admission_number = models.CharField(max_length=10, unique=True, blank=True)
    image = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    documents = models.FileField(upload_to='student_documents/', blank=True, null=True)
    re_registered = models.BooleanField(default=False) 

    def save(self, *args, **kwargs):
        from .models import SchoolSetting, PrimaryStudent, SecondaryStudent

        max_students = SchoolSetting.objects.first().max_students if SchoolSetting.objects.exists() else 5000
        total_students = (
            PrimaryStudent.objects.count() +
            SecondaryStudent.objects.count() +
            SeniorSecondaryStudent.objects.count()
        )

        if total_students >= max_students:
            raise ValidationError(f"Cannot add student. Maximum limit of {max_students} students reached.")

        # If student exists in SecondaryStudent, reuse admission number
        existing_student = SecondaryStudent.objects.filter(first_name=self.first_name, last_name=self.last_name).first()

        if existing_student:
            self.admission_number = existing_student.admission_number
        elif not self.admission_number:
            self.admission_number = get_next_admission_number()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Grade {self.grades})"

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

from django.db import models, transaction
import datetime

# Model to track the last used teacher number
class TeacherCount(models.Model):
    last_used_number = models.IntegerField(default=0)  # Tracks the last number used

    @classmethod
    def get_instance(cls):
        """Ensure there's always one instance available"""
        obj, created = cls.objects.get_or_create(id=1, defaults={'last_used_number': 0})
        return obj

    def increment(self):
        """Safely increment the last used number"""
        self.last_used_number += 1
        self.save()
        return self.last_used_number

# Teacher Model
class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    address = models.TextField()
    profile_photo = models.ImageField(upload_to='teachers/photos/', null=True, blank=True)
    documents = models.FileField(upload_to='teachers/documents/', null=True, blank=True)  # Document upload
    subjects = models.ManyToManyField('Subject', related_name="teachers")
    is_class_master = models.BooleanField(default=False)
    admission_number = models.CharField(max_length=15, unique=True, blank=True)  # Staff ID
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Salary field
    grades = models.ManyToManyField(CLASS, related_name="teachers") 
    def save(self, *args, **kwargs):
        if not self.admission_number:
            current_year = datetime.date.today().year % 100  # Get last two digits of the year

            # Locking the row to prevent race conditions
            with transaction.atomic():
                teacher_count = TeacherCount.get_instance()
                last_used_number = teacher_count.increment()

            self.admission_number = f'staff-{current_year}{last_used_number:03d}'  # Format: staff-YYXXX

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.admission_number})"





#this part is for the custom users

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    """Manager for CustomUser to create users and superusers."""
    
    def create_user(self, username, email, password=None, role=None):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """Create and return a superuser with admin privileges."""
        user = self.create_user(username, email, password, role='superadmin')
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

#Custom user 
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('superadmin', 'Super Admin'),
        ('student_admin', 'Student Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(Group, blank=True, related_name="customuser_set")
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name="customuser_permissions_set")

    def is_student_admin(self):
        return self.role == 'student_admin'

    def is_superadmin(self):
        return self.role == 'superadmin'

    def __str__(self):
        return f"{self.username} - {self.role}"
#his one is a try


#for the grade

