from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    productivity_score = models.DecimalField(max_digits=5, decimal_places=2)
    absences = models.IntegerField()
    status = models.CharField(max_length=20, default='Actif')
    
    SEXE_CHOICES = [
        ('M', 'Homme'),
        ('F', 'Femme'),
        
    ]
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES,default='F')
    photo = models.ImageField(upload_to='employees/', blank=True)

    age = models.IntegerField()
    email = models.EmailField(max_length=100, unique=True) 
    
    class Meta:
        db_table = 'employee'



    def __str__(self):
        return self.name
    
    

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    total_tasks = models.IntegerField()
    tasks_completed = models.IntegerField()
    hours_worked = models.IntegerField()
    project_budget = models.DecimalField(max_digits=10, decimal_places=2)
    budget_used = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    manager_id = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='managed_projects')
    class Meta:
        db_table = 'project'



    def __str__(self):
        return self.project_name



# Modèle pour la disponibilité des employés
class Availability(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    available_from = models.DateField()
    available_to = models.DateField()
    class Meta:
        db_table = 'available'



    def __str__(self):
        return f"{self.employee.name} Availability"

# Modèle pour les notifications
class Notification(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'notification'  



    def __str__(self):
        return f"Notification for {self.employee.name}"

# Modèle pour la relation plusieurs à plusieurs entre les employés et les projets
class EmployeeProject(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    class Meta:
        db_table = 'EmployeeProject'  
        unique_together = ('employee', 'project')

    def __str__(self):
        return f"{self.employee.name} - {self.project.project_name}"
