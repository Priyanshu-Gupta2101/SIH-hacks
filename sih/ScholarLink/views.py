from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage


import json

from .models import *
from .forms import *

# Create your views here.

@login_required(login_url="login/")
def index(request):
    return render(request, "ScholarLink/index.html", {
        "student": Student.objects.filter(student=request.user)
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "ScholarLink/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "ScholarLink/login.html")
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "ScholarLink/login.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "ScholarLink/login.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "ScholarLink/login.html")
    

def about(request):
    return render(request, "ScholarLink/about.html")


def contact(request):
    return render(request, "ScholarLink/contact.html")


def student(request):
    if request.method == 'POST':
        personal_detail = PersonalDetail.objects.get(user=request.user)
        contact_detail = ContactDetail.objects.get(user=request.user)
        guardian_detail = GuardianDetail.objects.get(user=request.user)
        file_detail = FileDetail.objects.get(user=request.user) 

        student = Student(student=request.user, personal_detail=personal_detail, contact_detail=contact_detail, guardian_detail=guardian_detail, file_detail=file_detail)
        student.save()
        return HttpResponse(status=204)
    else:    
        return render(request, "ScholarLink/registration.html")


def personal_detail(request):   
    if request.method == 'PUT':
        data = json.loads(request.body)

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        enrol_no = data.get('enrol_no')
        dob = data.get('dob')

        if PersonalDetail.objects.filter(user=request.user):
            personal_detail = PersonalDetail.objects.get(user=request.user)
            personal_detail.first_name=first_name
            personal_detail.last_name=last_name
            personal_detail.enrollment_number=enrol_no
            personal_detail.date_of_birth=dob
            personal_detail.save()
        else:
            personal_detail = PersonalDetail(
                user=request.user, first_name=first_name, last_name=last_name, enrollment_number=enrol_no, date_of_birth=dob)
            personal_detail.save()

        return HttpResponse(status=204)     

def contact_detail(request):
    if request.method == 'PUT':
        data = json.loads(request.body)

        email = data.get('email')
        phone_no = data.get('phone_no')
        address = data.get('address')
        city = data.get('city')
        state = data.get('state')
        pincode = data.get('pincode')
        country = data.get('country')


        if ContactDetail.objects.filter(user=request.user):
            contact_detail = ContactDetail.objects.get(user=request.user)
            contact_detail.contact_email=email
            contact_detail.contact_phone=phone_no
            contact_detail.address=address
            contact_detail.city=city
            contact_detail.state=state
            contact_detail.pincode=pincode
            contact_detail.country=country
            contact_detail.save()
        else:
            contact_detail = ContactDetail(user=request.user, contact_email=email, contact_phone=phone_no, address=address, city=city, state=state, pincode=pincode, country=country)
            contact_detail.save()

        return HttpResponse(status=204)  


def guardian_detail(request):
    if request.method == 'PUT':
        data = json.loads(request.body)

        guardian_name = data.get('guardian_name')
        guardian_phone = data.get('guardian_no')
        guardian_email = data.get('guardian_email')
        guardian_gender = data.get('guardian_gender')

        if GuardianDetail.objects.filter(user=request.user):
            guardian_detail = GuardianDetail.objects.get(user=request.user)
            guardian_detail.guardian_name = guardian_name
            guardian_detail.guardian_phone = guardian_phone
            guardian_detail.guardian_email = guardian_email
            guardian_detail.guardian_gender = guardian_gender
            guardian_detail.save()
        else:
            guardian_detail = GuardianDetail(
                user=request.user, guardian_name=guardian_name, guardian_phone=guardian_phone, guardian_email=guardian_email, guardian_gender=guardian_gender)
            guardian_detail.save()

        return HttpResponse(status=204)  
    

def file_detail(request):
    if request.method == 'POST':

        print(request.FILES)

        profile_pic = request.FILES.get('profile_pic')
        signature = request.FILES.get('signature')
        aadhaar = request.FILES.get('aadhaar')
        income_cert = request.FILES.get('income_cert')

        
        print(profile_pic, signature, aadhaar, income_cert)

        if FileDetail.objects.filter(user=request.user):
            file_detail = FileDetail.objects.get(user=request.user)
            file_detail.profile_pic = profile_pic
            file_detail.signature = signature
            file_detail.aadhaar = aadhaar
            if income_cert:
                file_detail.income_cert = income_cert
            file_detail.save()
        else:
            if income_cert:
                file_detail = FileDetail(user=request.user, profile_pic=profile_pic, signature=signature, aadhaar=aadhaar, income_cert=income_cert)
                file_detail.save()
            else:
                file_detail = FileDetail(user=request.user, profile_pic=profile_pic, signature=signature, aadhaar=aadhaar)
                file_detail.save()

        return HttpResponse(status=204)


'''
def file_detail(request):
    if request.method == 'PUT':
        fs = FileSystemStorage()

        print(request.FILES)

        profile_pic = request.FILES.get('profile_pic')
        profile_pic = fs.save(profile_pic.name, profile_pic)

        signature = request.FILES.get('signature')
        signature = fs.save(signature.name, signature)

        aadhaar = request.FILES.get('aadhaar')
        aadhaar = fs.save(aadhaar.name, aadhaar)

        income_cert = request.FILES.get('income_cert')
        income_cert = fs.save(income_cert.name, income_cert)

        
        print(profile_pic, signature, aadhaar, income_cert)

        if FileDetail.objects.filter(user=request.user):
            file_detail = FileDetail.objects.get(user=request.user)
            file_detail.profile_pic = profile_pic
            file_detail.signature = signature
            file_detail.aadhaar = aadhaar
            if income_cert:
                file_detail.income_cert = income_cert
            file_detail.save()
        else:
            if income_cert:
                file_detail = FileDetail(user=request.user, profile_pic=profile_pic, signature=signature, aadhaar=aadhaar, income_cert=income_cert)
                file_detail.save()
            else:
                file_detail = FileDetail(user=request.user, profile_pic=profile_pic, signature=signature, aadhaar=aadhaar)
                file_detail.save()

        return HttpResponse(status=204)

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = StudentForm()

    return render(request, 'ScholarLink/add_student.html', {'form': form})
'''


    


