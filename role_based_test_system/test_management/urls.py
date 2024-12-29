from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Collector URLs
    path('collector_dashboard/', views.collector_dashboard, name='collector_dashboard'),
    path('add_test/', views.add_test, name='add_test'),
    path('toggle_test/<int:test_id>/', views.toggle_test_status, name='toggle_test'),
    path('student_ranking/', views.student_ranking, name='student_ranking'),
    path('student_report/', views.student_report, name='student_report'),

    # School URLs
    path('school_dashboard/', views.school_dashboard, name='school_dashboard'),
    path('add_student/', views.add_student, name='add_student'),
    path('edit_student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('add_marks/', views.add_marks, name='add_marks'),
    path('student_list/', views.student_list, name='student_list'),
    path('test_list/', views.test_list, name='test_list'),


    # Other URLs
    path('other_dashboard/', views.other_dashboard, name='other_dashboard'),
    path('top_students/', views.top_students, name='top_students'),
]
