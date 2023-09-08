from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.

@login_required(login_url="login/")
def index(request):
    return render(request, "ScholarLink/landing.html")

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

def student_register(request):
    if request.method == "POST":
        username = request.user.username
        Fullname = request.POST['name']
        gender = request.POST['gender']
        Fathername = request.POST['Fname']
        Mothername = request.POST['Mname']
        DOB = request.POST['dob']
        phoneno = request.POST['phoneno']
        email = request.POST['email']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']

        obj = student_details(student_username = username, student_name = Fullname, student_gender = gender, student_DOB= DOB,student_father = Fathername, student_mother = Mothername, student_phoneno = phoneno, student_email = email, student_address = address, student_city = city, student_state = state, student_pincode = pincode)
        obj.save()

        return render(request, 'landing.html')
    else:
        # if request.user.is_authenticated:
        #     username = request.user.username
        #     print(username)
        return render(request, 'ScholarLink/student_register.html')