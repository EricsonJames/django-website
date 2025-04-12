from django.urls import path
from . import views


urlpatterns = [
    #this one is for the classes
     path('add_class',views.add_class, name='add_class'),
     path('class_list',views.class_list, name='class_list'),
     #the edit and delete class
     path('edit/class/<int:pk>',views.edit_class, name='edit_class'),
     path('delete/class/<int:pk>',views.delete_class, name='delete_class'),
    #this ajax is to get student data
    path("student-data/",views.student_data, name="student_data"),
    #this is gonna be the home view
     path('update_registration_limit',views.update_registration_limit,name='update_registration_limit'),
    path('logout/',views.logout_view, name='logout'),
    path('',views.login_view, name='login_view'),
    path('home', views.home, name='home'),
    path('primary/', views.primary_students, name='primary_students'),
    path('secondary/', views.secondary_students, name='secondary_students'),
    path('senior-secondary/', views.senior_secondary_students, name='senior_secondary_students'),
    path('generate-student-card/<str:level>/<int:student_id>/', views.generate_student_card, name='generate_student_card'),
    path('generate-teacher-card/<int:teacher_id>/', views.generate_teacher_card_pdf, name='generate_teacher_card'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    #the subject_views
    path('subject_list/',views.subjects,name='subject_list'),
    path('teachers/<int:teacher_id>/',views.teacher_detail, name='teacher_detail'),
    path('students/add/primary/', views.add_primary_student, name='add_primary_student'),
    path('students/add/secondary/', views.add_secondary_student, name='add_secondary_student'),
    path('students/add/senior/', views.add_senior_student, name='add_senior_student'),
    path('add_subject',views.add_subject,name='add_subject'),
    
    path('students/edit/primary/<int:pk>/', views.edit_primary_student, name='edit_primary_student'),
    path('students/edit/secondary/<int:pk>/', views.edit_secondary_student, name='edit_secondary_student'),
    path('students/edit/senior/<int:pk>/', views.edit_senior_student, name='edit_senior_student'),
    path('subjects/edit/subject/<int:pk>',views.edit_subject, name='edit_subject'),

    # Delete Student URLs
    path('students/delete/primary/<int:pk>/', views.delete_primary_student, name='delete_primary_student'),
    path('students/delete/secondary/<int:pk>/', views.delete_secondary_student, name='delete_secondary_student'),
    path('students/delete/senior/<int:pk>/', views.delete_senior_student, name='delete_senior_student'),
    path('subject/delete<int:pk>',views.delete_subject, name='delete_subject'),
    
    #is urls is for teachers
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/create/', views.add_teacher, name='create_teacher'),
    path('teachers/<int:pk>/edit/', views.edit_teacher, name='edit_teacher'),
    path('teachers/<int:pk>/delete/', views.delete_teacher, name='delete_teacher'),
    
    #this is for the student re-registration url
    path('re_register_primary_to_secondary', views.re_register_primary_to_secondary, name='re_register_primary_to_secondary'),
    path('re-register/secondary-to-senior/', views.re_register_secondary_to_senior, name='re_register_secondary_to_senior'),
 #an option to delete every thing
    path('delete-primary/', views.delete_selected_primary, name='delete_selected_primary'),
    path('delete-secondary/', views.delete_selected_secondary, name='delete_selected_secondary'),
    path('delete-senior/', views.delete_selected_senior, name='delete_selected_senior'),
    path('delete-seleted/', views.delete_selected_teacher, name='delete_selected_teacher'),
    path('delete-select/', views.delete_selected_subject, name='delete_selected_subject'),
    path('delete-class/',views.delete_selected_class, name='delete_selected_class')
    

]

