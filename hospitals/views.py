from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login
from .models import *
from datetime import date

# Create your views here.

def About(request):
    return render(request,'about.html')

def Index(request):
    return render(request,'index.html')

def contact(request):
    error = ""
    if request.method == 'POST':
        n = request.POST['name']
        c = request.POST['contact']
        e = request.POST['email']
        s = request.POST['subject']
        m = request.POST['message']
        try:
            Contact.objects.create(name=n, contact=c, email=e, subject=s, message=m, msgdate=date.today(), isread="no")
            error = "no"
        except:
            error = "yes"
    return render(request, 'contact.html', locals())

def adminlogin(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        fn= request.POST['firstName']
        ln = request.POST['lastName']
        id = request.POST['id']
        email = request.POST['email']
        user = authenticate(username=u, password=p)
        try:
            receptionist = Receptionist.objects.get(
                receptionistFirstName=fn, 
                receptionistLastName=ln, 
                receptionistID=id, 
                email=email, 
                admin=user)
        except Receptionist.DoesNotExist:
            error="yes"
        try:
            if user.is_staff and receptionist:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request,'login.html', locals())

def admin_home(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    dc = Doctor.objects.all().count()
    pc = Patient.objects.all().count()
    ac = Appointment.objects.all().count()
    user = request.user
    receptionist = Receptionist.objects.get(admin=user)
    patients = Patient.objects.filter(receptionist=receptionist)

    appointments_of_patients = Appointment.objects.filter(patient__in=patients)

    procedure_records = ProcedureForm.objects.filter(appointment__in=appointments_of_patients)

    d = {'dc': dc, 'pc': pc, 'ac': ac, "records": procedure_records}
    print(procedure_records)
    return render(request,'admin_home.html', d)

def Logout(request):
    logout(request)
    return redirect('index')

def add_doctor(request):
    error=""
    if not request.user.is_staff:
        return redirect('login')
    if request.method=='POST':
        n = request.POST['name']
        m = request.POST['mobile']
        sp = request.POST['special']
        try:
            Doctor.objects.create(name=n,mobile=m,special=sp)
            error="no"
        except:
            error="yes"
    return render(request,'add_doctor.html', locals())

def view_doctor(request):
    if not request.user.is_staff:
        return redirect('login')
    doc = Doctor.objects.all()
    d = {'doc':doc}
    return render(request,'view_doctor.html', d)

def Delete_Doctor(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    doctor = Doctor.objects.get(id=pid)
    doctor.delete()
    return redirect('view_doctor')

def edit_doctor(request,pid):
    error = ""
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    doctor = Doctor.objects.get(id=pid)
    if request.method == "POST":
        n1 = request.POST['name']
        m1 = request.POST['mobile']
        s1 = request.POST['special']

        doctor.name = n1
        doctor.mobile = m1
        doctor.special = s1

        try:
            doctor.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'edit_doctor.html', locals())

def add_patient(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    if request.method == 'POST':
        n = request.POST['name']
        g = request.POST['gender']
        m = request.POST['mobile']
        a = request.POST['address']
        id = request.POST['id']
        user = request.user
        receptionist = Receptionist.objects.get(admin=user)
        print(receptionist)
        try:
            new_patient = Patient.objects.create(name=n, gender=g, mobile=m, address=a, patientId=id, receptionist=receptionist)
            print(new_patient)
            error = "no"
        except:
            error = "yes"
    return render(request,'add_patient.html', locals())

def view_patient(request):
    if not request.user.is_staff:
        return redirect('login')
    pat = Patient.objects.all()
    d = {'pat':pat}
    return render(request,'view_patient.html', d)

def Delete_Patient(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    patient = Patient.objects.get(id=pid)
    patient.delete()
    return redirect('view_patient')

def edit_patient(request,pid):
    error = ""
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    patient = Patient.objects.get(id=pid)
    if request.method == "POST":
        n1 = request.POST['name']
        m1 = request.POST['mobile']
        g1 = request.POST['gender']
        a1 = request.POST['address']
        patient_id = request.POST['patient_id']

        patient.name = n1
        patient.mobile = m1
        patient.gender = g1
        patient.address = a1
        patient.patientId = patient_id
        try:
            patient.save()
            error = "no"
        except:
            error = "yes"
    return render(request, 'edit_patient.html', locals())



def add_appointment(request):
    error=""
    if not request.user.is_staff:
        return redirect('login')
    doctor1 = Doctor.objects.all()
    patient1 = Patient.objects.all()
    if request.method=='POST':
        d = request.POST['doctor']
        p = request.POST['patient']
        d1 = request.POST['date']
        t = request.POST['time']
        doctor = Doctor.objects.filter(name=d).first()
        patient = Patient.objects.filter(name=p).first()
        try:
            Appointment.objects.create(doctor=doctor, patient=patient, date1=d1, time1=t)
            error="no"
        except:
            error="yes"
    d = {'doctor':doctor1,'patient':patient1,'error':error}
    return render(request,'add_appointment.html', d)

def add_procedure(request):
    error=""
    if not request.user.is_staff:
        return redirect('login')
    appointments = Appointment.objects.all()
    appointments_count = Appointment.objects.all().count()
    if request.method=='POST':
        print(request.POST)
        appointment = int(request.POST['appointment'])
        type = request.POST['type']
        date = request.POST['date']
        required_appointment = Appointment.objects.filter(id=appointment).first()
        print(required_appointment)
        try:
            ProcedureForm.objects.create(appointment=required_appointment, type=type, date1=date)
            error="no"
        except:
            error="yes"
    d = {'appointments':appointments, "appointments_count": appointments_count, 'error':error}
    return render(request,'add_procedure.html', d)

def view_appointment(request):
    if not request.user.is_staff:
        return redirect('login')
    appointment = Appointment.objects.all()
    d = {'appointment':appointment}
    return render(request,'view_appointment.html', d)

def view_procedure(request):
    if not request.user.is_staff:
        return redirect('login')
    procedures = ProcedureForm.objects.all()
    d = {'procedures':procedures}
    return render(request,'view_procedure.html', d)


def Delete_Appointment(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    appointment1 = Appointment.objects.get(id=pid)
    appointment1.delete()
    return redirect('view_appointment')

def Delete_procedure(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    procedure = ProcedureForm.objects.get(id=pid)
    procedure.delete()
    return redirect('view_procedure')

def update_patient_record(request):
    error = ""
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    patients = Patient.objects.all()
    if request.method == "POST":
        patient = request.POST['patient']
        shots = request.POST['shots']
        illness = request.POST['illness']

        patient = Patient.objects.get(patientId = patient)
        new_record = PatientRecord.objects.create(shots=shots, illness=illness)
        patient.patient_record = new_record

        try:
            patient.save()
            error = "no"
        except:
            error = "yes"
    d = {"patients": patients, "error": error}
    return render(request, 'update_patient_record.html', d)

def unread_queries(request):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.filter(isread="no")
    return render(request,'unread_queries.html', locals())

def read_queries(request):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.filter(isread="yes")
    return render(request,'read_queries.html', locals())

def view_queries(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.get(id=pid)
    contact.isread = "yes"
    contact.save()
    return render(request,'view_queries.html', locals())

