from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('projects/', views.get_projects, name='get_projects'),
    path('kpi_dashboard/', views.kpi_dashboard, name='kpi_dashboard'),  # Route correcte ici
    path('employees/', views.get_employees, name='get_employees'),
    path('employees/add', views.add_employee, name='add_employee'),
]
