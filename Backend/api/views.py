from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Availability, EmployeeProject, Notification, Project, Employee
from .serializers import AvailabilitySerializer, EmployeeProjectSerializer, NotificationSerializer, ProjectSerializer, EmployeeSerializer


@api_view(['GET'])
def kpi_dashboard(request):

    df = pd.read_csv('kpi_projects.csv', sep =',')
    
    # Calculer des KPI
    df['completion_rate'] = df['tasks_completed'] / df['total_tasks'] * 100  # Taux de complétion des tâches
    df['productivity'] = df['tasks_completed'] / df['hours_worked']  # Productivité des employés

    # Retourner les données sous forme de JSON
    data = df.to_dict(orient='records')  # Convertir le DataFrame en dictionnaire de records
    return JsonResponse(data, safe=False)


@api_view(['GET'])
def get_employees(request):
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_employee(request):
    serializer = EmployeeSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201) 
    return Response(serializer.errors, status=400) 


@api_view(['GET'])
def get_projects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def get_availability(request):
    availability = Availability.objects.all()
    serializer = AvailabilitySerializer(availability, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_employee_projects(request):
    employee_projects = EmployeeProject.objects.all()
    serializer = EmployeeProjectSerializer(employee_projects, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def get_notifications(request):
    notifications = Notification.objects.all()
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


