# Generated by Django 4.1.7 on 2023-11-26 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospitals', '0005_patient_patientid_alter_patient_address_receptionist_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='receptionist',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='hospitals.receptionist'),
        ),
    ]
