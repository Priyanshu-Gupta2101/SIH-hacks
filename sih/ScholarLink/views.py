from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

import json

from .models import *
from .forms import *

# Create your views here.

@login_required(login_url="login/")
def index(request):
    return render(request, "ScholarLink/index.html")

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

        student = Student(student=request.user, personal_detail=personal_detail, contact_detail=contact_detail, guardian_detail=guardian_detail)
        student.save()
        return HttpResponse(status=204)
    else:    
        return render(request, "ScholarLink/registration.html")


def personal_detail(request):   
    if request.method == 'PUT':
        data = json.loads(request.body)

        full_name = data.get('full_name')
        enrol_no = data.get('enrol_no')

        if PersonalDetail.objects.filter(user=request.user):
            personal_detail = PersonalDetail.objects.get(user=request.user)
            personal_detail.full_name=full_name
            personal_detail.enrollment_number=enrol_no
            personal_detail.save()
        else:
            personal_detail = PersonalDetail(user=request.user, full_name=full_name, enrollment_number=enrol_no)
            personal_detail.save()

        print(data)

        return HttpResponse(status=204)     

def contact_detail(request):
    if request.method == 'PUT':
        data = json.loads(request.body)

        email = data.get('email')
        phone_no = data.get('phone_no')

        if ContactDetail.objects.filter(user=request.user):
            contact_detail = ContactDetail.objects.get(user=request.user)
            contact_detail.contact_email=email
            contact_detail.contact_phone=phone_no
            contact_detail.save()
        else:
            contact_detail = ContactDetail(user=request.user, contact_email=email, contact_phone=phone_no)
            contact_detail.save()

        print(data)
        return HttpResponse(status=204)  


def guardian_detail(request):
    if request.method == 'PUT':
        data = json.loads(request.body)

        guardian_name = data.get('guardian_name')
        guardian_phone = data.get('guardian_no')

        if GuardianDetail.objects.filter(user=request.user):
            guardian_detail = GuardianDetail.objects.get(user=request.user)
            guardian_detail.guardian_name = guardian_name
            guardian_detail.guardian_phone = guardian_phone
            guardian_detail.save()
        else:
            guardian_detail = GuardianDetail(user=request.user, guardian_name=guardian_name, guardian_phone=guardian_phone)
            guardian_detail.save()

        print(data)
        return HttpResponse(status=204)  
        

'''
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


    


