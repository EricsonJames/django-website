from django.contrib import admin
from .models import PrimaryStudent, SecondaryStudent, SeniorSecondaryStudent




admin.site.register(PrimaryStudent)
class PrimaryStudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'grade', 'date_of_birth','parent_contact','address','admission_number','image')
    search_fields = ('first_name', 'last_name')

admin.site.register(SecondaryStudent)
class SecondaryStudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'grade', 'date_of_birth','parent_contact','address','admission_number','image')
    search_fields = ('first_name', 'last_name')

admin.site.register(SeniorSecondaryStudent)
class SeniorSecondaryStudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'grade', 'date_of_birth','parent_contact','address','admission_number','image')
    search_fields = ('first_name', 'last_name')

from django.contrib import admin
from .models import Teacher, Subject

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'contact', 'is_class_master')
    list_filter = ('is_class_master', 'subjects')
    search_fields = ('first_name', 'last_name', 'contact')


#this one is for the custom user registration
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'role')
    list_filter = ('role', 'is_active')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_active', 'is_staff')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)

from django.contrib import admin
from .models import SchoolSetting

@admin.register(SchoolSetting)
class SchoolSettingAdmin(admin.ModelAdmin):
    list_display = ['max_students']  # Display the max_students field in the list view
    # Remove max_students from list_editable
    list_display_links = ['max_students']  # Make max_students clickable
    search_fields = ['max_students']  # Optional: Add search functionality
