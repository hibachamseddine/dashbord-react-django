# serializers.py

from rest_framework import serializers
from .models import Availability, EmployeeProject, Notification, Project, Employee


class ProjectSerializer(serializers.ModelSerializer):
    manager = serializers.StringRelatedField()  # Affiche le nom du responsable au lieu de l'ID

    class Meta:
        model = Project
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class AvailabilitySerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()

    class Meta:
        model = Availability
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()

    class Meta:
        model = Notification
        fields = '__all__'


class EmployeeProjectSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()
    project = ProjectSerializer()

    class Meta:
        model = EmployeeProject
        fields = '__all__'
