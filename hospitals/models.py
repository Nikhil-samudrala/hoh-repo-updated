from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Doctor(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.IntegerField()
    special = models.CharField(max_length=50)

    def __str__(self):
       return self.name;

class PatientRecord(models.Model):
    shots = models.CharField(max_length=100, null=True)
    illness = models.CharField(max_length=100, null=True)

    def __str__(self):
        return (self.patient.name + " " + self.shots)
    

class Receptionist(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    receptionistFirstName = models.CharField(max_length=100)
    receptionistLastName = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    receptionistID = models.CharField(max_length=100)


class Patient(models.Model):
    receptionist = models.ForeignKey(Receptionist, on_delete=models.CASCADE, null=True)
    patient_record = models.OneToOneField(PatientRecord, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    mobile = models.IntegerField(null=True)
    address = models.CharField(max_length=50, null=True)
    patientId = models.CharField(max_length=100, null=True)

    def __str__(self):
       return self.name;

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date1 = models.DateField()
    time1 = models.TimeField()

    def __str__(self):
       return self.doctor.name+"--"+self.patient.name;

class ProcedureForm(models.Model):
     date1 = models.DateField()
     type = models.CharField(max_length=100)
     appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)

     def __str__(self):
         return self.type+"--"+self.appointment.doctor.name+"--"+self.appointment.patient.name;


class Contact(models.Model):
    name = models.CharField(max_length=100, null=True)
    contact = models.CharField(max_length=15, null=True)
    email = models.CharField(max_length=50, null=True)
    subject = models.CharField(max_length=100, null=True)
    message = models.CharField(max_length=300, null=True)
    msgdate = models.DateField(null=True)
    isread = models.CharField(max_length=10,null=True)

    def __str__(self):
        return self.id




     
