from django import forms
from .models import PrimaryStudent, SecondaryStudent, SeniorSecondaryStudent

class PrimaryStudentForm(forms.ModelForm):
    class Meta:
        model = PrimaryStudent
        fields = ['first_name', 'last_name', 'grades', 'date_of_birth', 'parent_contact', 'address', 'image', 'documents']

class SecondaryStudentForm(forms.ModelForm):
    class Meta:
        model = SecondaryStudent
        fields = ['first_name', 'last_name', 'grades', 'date_of_birth', 'parent_contact', 'address', 'image', 'documents']

class SeniorSecondaryStudentForm(forms.ModelForm):
    class Meta:
        model = SeniorSecondaryStudent
        fields = ['first_name', 'last_name', 'grades', 'date_of_birth', 'parent_contact', 'address', 'image', 'documents']



#this is the teachers form
from django import forms
from .models import Teacher, CLASS, Subject

class TeacherForm(forms.ModelForm):
    
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'contact', 'address', 'profile_photo', 'documents', 'subjects', 'is_class_master', 'salary', 'grades']


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Subject Name'}),
        }
        labels = {
            'name': 'Subject Name',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Subject.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("This subject already exists.")
        return name



#adding custom user form
#student update limit
from django import forms
from .models import SchoolSetting

class SchoolSettingForm(forms.ModelForm):
    class Meta:
        model = SchoolSetting
        fields = ['max_students']

#this for id for the grade
from django import forms
from .models import CLASS

class GradeForm(forms.ModelForm):
    class Meta:
        model = CLASS
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Grade Name'})
        }
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if CLASS.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("This Class already exists.")
        return name
    
    
    
    
    
    
    
    #this is for the registration
    
    from django import forms
from .models import PrimaryStudent, SecondaryStudent, SeniorSecondaryStudent

class PrimaryToSecondaryForm(forms.ModelForm):
    class Meta:
        model = SecondaryStudent
        fields = ['first_name', 'last_name', 'grades', 'date_of_birth', 'parent_contact', 'address', 'image', 'documents']

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        # Check if the student exists in PrimaryStudent
        primary_student = PrimaryStudent.objects.filter(first_name=first_name, last_name=last_name).first()
        if not primary_student:
            raise forms.ValidationError("No matching student found in Primary records.")

        return cleaned_data

class SecondaryToSeniorForm(forms.ModelForm):
    class Meta:
        model = SeniorSecondaryStudent
        fields = ['first_name', 'last_name', 'grades', 'date_of_birth', 'parent_contact', 'address', 'image', 'documents']

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        # Check if the student exists in SecondaryStudent
        secondary_student = SecondaryStudent.objects.filter(first_name=first_name, last_name=last_name).first()
        if not secondary_student:
            raise forms.ValidationError("No matching student found in Secondary records.")

        return cleaned_data
