from django.contrib import admin
from django.urls import path,include

from Backend import settings
from . import views
from django.conf.urls.static import static 

urlpatterns = [
    path('projects/', views.get_projects, name='get_projects'),
    path('projects/add', views.add_project, name='add_project'),
    path('projects/update/<str:pk>/', views.projectupdate, name='projectupdate'),
    path('kpi_dashboard/', views.kpi_dashboard, name='kpi_dashboard'), 
    path('kpi/', views.KPIDashboardView.as_view(), name='kpi'), 
    #employee
    path('employees/', views.get_employees, name='get_employees'),
    path('employee/add', views.add_employee, name='add_employee'),
    path('employee/update/<str:pk>/', views.employeeupdate, name='employeeupdate'),
    path('availability/', views.get_availability),  
    path('availability/add/', views.add_availability), 
    path('employee-projects/', views.get_employee_projects),
    path('employee-project/add/', views.add_employee_project), 
    path('notifications/', views.get_notifications),  
    path('notification/add/', views.add_notification), 
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)