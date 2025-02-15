from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Availability, EmployeeProject, Notification, Project, Employee
from .serializers import AvailabilitySerializer, EmployeeProjectSerializer, NotificationSerializer, ProjectSerializer, EmployeeSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
import matplotlib.pyplot as plt
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Employee
from .serializers import EmployeeSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import viewsets
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework.permissions import IsAuthenticated

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
        projets_termines = df_projets[df_projets['status'] == 'Terminé'].shape[0]  # Projets terminés
        
        taux_completion = (projets_en_cours / total_projets) * 100 if total_projets > 0 else 0  # Taux de complétion des projets

        # Calculer des KPI pour les employés (RH)
        total_employes = df_employes[df_employes['status'] != 'Sortie'].shape[0]  # Exclure les employés avec le statut 'Sortie'

        employes_actifs = df_employes[df_employes['status'] == 'Travaille'].shape[0]  # Nombre d'employés actifs
        employes_en_conge = df_employes[df_employes['status'] == 'Congé'].shape[0]  # Nombre d'employés en congé
        employes_Sortis = df_employes[df_employes['status'] == 'Sortie'].shape[0]  # Nombre d'employés sortis
        
        taux_retention = (employes_actifs / total_employes) * 100 if total_employes > 0 else 0  # Taux de rétention des employés
        absenteeismRate = df_employes['absences'].mean()  # Taux d'absentéisme

        # Calculer des KPI de productivité
        avgProductivityScore = (df_projets['hours_worked'] / df_projets['total_tasks']) * 100
        charge_travail_moyenne = df_projets['hours_worked'].mean()  # Charge de travail moyenne par projet

        # Ajouter d'autres KPI personnalisés si nécessaire
        taux_satisfaction_employe = df_employes['satisfaction_score'].mean() if 'satisfaction_score' in df_employes.columns else 0  # Taux de satisfaction des employés

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
            "employes_Sortis": employes_Sortis,
            "taux_retention": round(taux_retention, 2),
            "taux_absentéisme": round(absenteeismRate, 2),  # Arrondi à 2 décimales
            "productivity_score_moyenne": round(avgProductivityScore, 2),
            "charge_travail_moyenne": round(charge_travail_moyenne, 2),  # Charge de travail moyenne
            "taux_satisfaction_employe": round(taux_satisfaction_employe, 2),
            "employes_info": employes_info
        })

    






class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def perform_create(self, serializer):
        employee = serializer.save()
        
        # 🔥 Envoi du message WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "employees",
            {
                "type": "broadcast_employee",
                "message": f"Nouvel employé ajouté : {employee.name}",
                
            }
        )
        
        
    def perform_destroy(self, instance):
        employee_id = instance.id  # ✅ Récupère l'ID avant suppression
        instance.delete()
        
        # 🔥 Envoie le message WebSocket après suppression
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "employees",  # Groupe "employees"
            {
                "type": "broadcast_employee_deleted",  # Le type de l'événement est 'delete'
                "employee_id": employee_id,  # Envoyer l'ID de l'employé supprimé
                "message": f"L'employé avec ID {employee_id} a été supprimé.",
            }
        )

        
        
        
    
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all() 
    serializer_class = ProjectSerializer 
    #permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        project = serializer.save()
    
        # 🔥 Envoi du message WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "projects",
            {
                "type": "broadcast_project",
                "message": f"Nouvel project ajouté : {project.project_name}",
            }
        )
        
        
    def perform_destroy(self, instance):
        project_id = instance.id  
        instance.delete()
        
       
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "projects", 
            {
                "type": "broadcast_project_deleted", 
                "project_id": project_id, 
                "message": f"L'project avec ID {project_id} a été supprimé.",
            }
        )
    

    
    
class EmployeProjectViewSet(viewsets.ModelViewSet):
    queryset = EmployeeProject.objects.all() 
    serializer_class = EmployeeProjectSerializer 
    
    
class AvailabilityViewSet(viewsets.ModelViewSet):
    queryset = Availability.objects.all() 
    serializer_class = AvailabilitySerializer
    
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all() 
    serializer_class = NotificationSerializer