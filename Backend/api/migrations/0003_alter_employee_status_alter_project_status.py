# Generated by Django 4.2 on 2025-02-12 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_manager_id_project_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='status',
            field=models.CharField(choices=[('Travaille', 'Travaille'), ('Sortie', 'Sortie'), ('Congé', 'Congé')], default='Travaille', max_length=20),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('En cours', 'En cours'), ('Terminé', 'Terminé')], default='En cours', max_length=50),
        ),
    ]
