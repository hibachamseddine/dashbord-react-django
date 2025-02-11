from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Availability, EmployeeProject, Notification, Project, Employee
from .serializers import AvailabilitySerializer, EmployeeProjectSerializer, NotificationSerializer, ProjectSerializer, EmployeeSerializer


from rest_framework.response import Response
from rest_framework.views import APIView
import pandas as pd

from rest_framework.views import APIView
from rest_framework.response import Response

import pandas as pd
import matplotlib.pyplot as plt

from .models import Project, Employee





class KPIDashboardView(APIView):
    def get(self, request):
        # Récupérer les données des projets et des employés
        projets = Project.objects.all().values()
        employes = Employee.objects.all().values()

        # Transformer les données en DataFrame Pandas
        df_projets = pd.DataFrame(projets)
        df_employes = pd.DataFrame(employes)
 
       

        # Calculer des KPI pour les projets
        total_projets = df_projets.shape[0]  # Nombre total de projets
        projets_en_cours = df_projets[df_projets['status'] == 'En cours'].shape[0]  # Projets en cours
        projets_termines = df_projets[df_projets['status'] == 'terminé'].shape[0]  # Projets terminés
        taux_completion = (projets_en_cours / total_projets) * 100 if total_projets > 0 else 0  # Taux de complétion des projets

        # Calculer des KPI pour les employés (RH)
        total_employes = df_employes[df_employes['status'] != 'Sortis'].shape[0] 
        employes_actifs = df_employes[df_employes['status'] == 'Actif'].shape[0]  # Nombre d'employés actifs
        employes_en_conge = df_employes[df_employes['status'] == 'En congé'].shape[0]  # Nombre d'employés en congé
        employes_inactifs = df_employes[df_employes['status'] == 'Sortis'].shape[0]  
        taux_retention = (employes_actifs / total_employes) * 100 if total_employes > 0 else 0  # Taux de rétention des employés
        absenteeismRate = df_employes['absences'].mean()  # Calculate average absenteeism

        avgProductivityScore = (df_projets['hours_worked'] / df_projets['total_tasks']) * 100


        employes_info = df_employes.to_dict(orient='records')
        # Retourner les KPI sous forme de JSON
        return Response({
            "total_projets": total_projets,
            "projets_en_cours": projets_en_cours,
            "projets_termines": projets_termines,
            "taux_completion": round(taux_completion, 2),
            "total_employes": total_employes,
            "employes_actifs": employes_actifs,
            "employes_en_conge": employes_en_conge,
            "employes_inactifs": employes_inactifs,
            "taux_retention": round(taux_retention, 2),
            "taux_absentéisme": round(absenteeismRate, 2),  # Round to 2 decimals
            "productivity_score_moyenne": round(avgProductivityScore, 2),
            "employes_info": employes_info
        })




@api_view(['GET'])
def kpi_dashboard(request):

    df = pd.read_csv('kpi_projects.csv', sep =',')
    
    # Calculer des KPI
    df['completion_rate'] = df['tasks_completed'] / df['total_tasks'] * 100  # Taux de complétion des tâches
    df['productivity'] = df['tasks_completed'] / df['hours_worked']  # Productivité des employés

    # Retourner les données sous forme de JSON
    data = df.to_dict(orient='records')  # Convertir le DataFrame en dictionnaire de records
    return JsonResponse(data, safe=False)

#employees
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
def employeedetail(request,pk):
    employees = Employee.objects.get(id=pk)
    serializer = EmployeeSerializer(employees,many=False)
    return Response(serializer.data)
from rest_framework.parsers import MultiPartParser, FormParser
@api_view(['POST'])
def employeeupdate(request,pk):
    parser_classes = (MultiPartParser, FormParser) 
    
    employees = Employee.objects.get(id=pk)
    serializer = EmployeeSerializer(instance=employees,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteemployee(request,pk):
    employees = Employee.objects.get(id=pk)
    employees.delete()
    
   
    
    return Response()





#projects
@api_view(['GET'])
def get_projects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_project(request):
    serializer = ProjectSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201) 
    return Response(serializer.errors, status=400) 

@api_view(['POST'])
def projectupdate(request,pk):
    employees = Project.objects.get(id=pk)
    serializer = ProjectSerializer(instance=employees,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)




#Availability
@api_view(['GET'])
def get_availability(request):
    availability = Availability.objects.all()
    serializer = AvailabilitySerializer(availability, many=True)
    return Response(serializer.data)
@api_view(['POST'])
def add_availability(request):
    serializer = AvailabilitySerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201) 
    return Response(serializer.errors, status=400) 





#EmployeeProject
@api_view(['GET'])
def get_employee_projects(request):
    employee_projects = EmployeeProject.objects.all()
    serializer = EmployeeProjectSerializer(employee_projects, many=True)
    return Response(serializer.data)
@api_view(['POST'])
def add_employee_project(request):
    serializer = EmployeeProjectSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201) 
    return Response(serializer.errors, status=400) 




#notifications
@api_view(['GET'])
def get_notifications(request):
    notifications = Notification.objects.all()
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)
@api_view(['POST'])
def add_notification(request):
    serializer = NotificationSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201) 
    return Response(serializer.errors, status=400) 


