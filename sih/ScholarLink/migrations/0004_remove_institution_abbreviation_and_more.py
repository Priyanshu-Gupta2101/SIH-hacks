# Generated by Django 4.2.1 on 2023-09-12 19:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ScholarLink', '0003_institution_city_institution_country_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institution',
            name='abbreviation',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='accreditations_offered',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='affiliation_documents',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='city',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='contact_email',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='contact_phone',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='country',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='established_year',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='location',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='logo',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='name',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='pincode',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='registration_number',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='scholarships_offered',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='state',
        ),
        migrations.RemoveField(
            model_name='institution',
            name='website',
        ),
        migrations.AddField(
            model_name='institution',
            name='contact_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ScholarLink.contactdetail'),
        ),
        migrations.AddField(
            model_name='institution',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='InstituteDoc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='institution_logo/')),
                ('affiliation_document', models.FileField(upload_to='affiliation_document/')),
                ('accredited_by', models.ManyToManyField(related_name='authorized_institutions', to='ScholarLink.accreditationbody')),
                ('scholarships_offered', models.ManyToManyField(related_name='scholarship_institutions', to='ScholarLink.scholarship')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InstituteDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('abbreviation', models.CharField(blank=True, max_length=20, null=True)),
                ('established_year', models.PositiveIntegerField()),
                ('registration_number', models.CharField(max_length=20, unique=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='institution',
            name='institute_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ScholarLink.institutedetail'),
        ),
        migrations.AddField(
            model_name='institution',
            name='institution_doc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ScholarLink.institutedoc'),
        ),
    ]
