from django.db import models

class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    # username = models.CharField(max_length=50)
    # password = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name

class HealthInfo(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    checkup_date = models.DateField()
    blood_pressure = models.DecimalField(max_digits=5, decimal_places=2)
    heart_disease = models.DecimalField(max_digits=5, decimal_places=2)
    bmi = models.DecimalField(max_digits=5, decimal_places=2)
    hba1c = models.DecimalField(max_digits=5, decimal_places=2)
    blood_glucose = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.patient.full_name}'s Health Info"

class MedicalHistory(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    result = models.TextField()
    accuracy= models.FloatField(null=True)

    def __str__(self):
        return f"{self.patient.full_name}'s Medical History"
