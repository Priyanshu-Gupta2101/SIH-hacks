# Generated by Django 4.2.1 on 2023-09-10 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ScholarLink', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccreditationBody',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('abbreviation', models.CharField(blank=True, max_length=20, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('contact_email', models.EmailField(max_length=254)),
                ('contact_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('headquarters_location', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_email', models.EmailField(max_length=254)),
                ('contact_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FileDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academic_records', models.FileField(upload_to='academic_records/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GuardianDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guardian_name', models.CharField(blank=True, max_length=100, null=True)),
                ('guardian_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('abbreviation', models.CharField(blank=True, max_length=20, null=True)),
                ('location', models.CharField(max_length=100)),
                ('website', models.URLField(blank=True, null=True)),
                ('contact_email', models.EmailField(max_length=254)),
                ('contact_phone', models.CharField(max_length=15)),
                ('established_year', models.PositiveIntegerField()),
                ('registration_number', models.CharField(max_length=20, unique=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='institution_logos/')),
                ('affiliation_documents', models.FileField(upload_to='affiliation_documents/')),
                ('accreditations_offered', models.ManyToManyField(related_name='authorized_institutions', to='ScholarLink.accreditationbody')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('enrollment_number', models.CharField(max_length=20, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Scholarship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('eligibility_criteria', models.TextField()),
                ('award_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('provider', models.CharField(max_length=100)),
                ('website', models.URLField(blank=True, null=True)),
                ('contact_email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('contact_detail', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ScholarLink.contactdetail')),
                ('file_detail', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ScholarLink.filedetail')),
                ('guardian_detail', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ScholarLink.guardiandetail')),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ScholarLink.institution')),
                ('personal_detail', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ScholarLink.personaldetail')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='institution',
            name='scholarships_offered',
            field=models.ManyToManyField(related_name='scholarship_institutions', to='ScholarLink.scholarship'),
        ),
    ]