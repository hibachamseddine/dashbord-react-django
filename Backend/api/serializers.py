# serializers.py

from rest_framework import serializers
from .models import Availability, EmployeeProject, Notification, Project, Employee


class ProjectSerializer(serializers.ModelSerializer):
    manager = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.exclude(role='manager'))

    class Meta:
        model = Project
        fields = '__all__'
        
  

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        
    def get_photo_url(self,obj):
        request = self.context.get('request')
        photo_url=obj.fingerprint.url
        return request.build_absolute_uri(photo_url)
        
   

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
