# Generated by Django 3.2.7 on 2023-09-07 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ScholarLink', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scholarship_DB',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('scholarship_name', models.CharField(max_length=100)),
                ('conditions', models.JSONField(default=dict)),
                ('state_specific', models.BooleanField()),
                ('state_name', models.CharField(max_length=50, null=True)),
                ('date_added', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='student_DB',
            fields=[
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('student_name', models.CharField(max_length=100)),
                ('student_number', models.IntegerField()),
                ('student_email', models.EmailField(max_length=254)),
                ('student_DOB', models.DateField()),
                ('student_address', models.CharField(max_length=150)),
                ('student_city', models.CharField(max_length=50)),
                ('student_pincode', models.IntegerField()),
                ('student_state', models.CharField(max_length=50)),
            ],
        ),
    ]
