from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from django.contrib import messages

from .tokens import account_activation_token


import json

from .models import *
from .forms import *

# Create your views here.

@login_required(login_url="login/")
def index(request):
    return render(request, "ScholarLink/index.html", {
        "student": Student.objects.filter(student=request.user),
        "institute": Institution.objects.filter(institute=request.user)
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


def activateEmail(request, user, email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('ScholarLink/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {email}, check if you typed it correctly.')


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Attempt to create new user
        if password != confirmation:
            return render(request, "ScholarLink/login.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            #user.is_active = False
            user.save()
            activateEmail(request, user, email)
        except IntegrityError:
            return render(request, "ScholarLink/login.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "ScholarLink/login.html")
    

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('index')
    

def about(request):
    return render(request, "ScholarLink/about.html")


def contact(request):
    return render(request, "ScholarLink/contact.html")

def faq(request):
    if request.user.is_authenticated:
        scholarship_data = Scholarship.objects.all().values()
        print(scholarship_data)
        username = request.user.username
        email = request.user.email
        
        print(username, email)

        return render(request, 'ScholarLink/faq.html', {'scholarship_data':scholarship_data, 'username': username, 'email':email})
    else:    
        return render(request, "ScholarLink/login.html")

def institution_profile_dashboard(req):
    return render(req, 'ScholarLink/institution_dashboard.html')


def student(request):
    if request.method == 'POST':
        personal_detail = PersonalDetail.objects.get(user=request.user)
        contact_detail = ContactDetail.objects.get(user=request.user)
        guardian_detail = GuardianDetail.objects.get(user=request.user)
        file_detail = FileDetail.objects.get(user=request.user) 

        student = Student.objects.get(student=request.user)
        student.personal_detail = personal_detail
        student.contact_detail = contact_detail
        student.guardian_detail = guardian_detail
        student.file_detail = file_detail
        student.save()

        return HttpResponse(status=204)
    else:    
        return render(request, "ScholarLink/registration.html", {
            "institutes": Institution.objects.all(),
        })


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

def student_profile_dashboard(request):
    try:
        student = Student.objects.get(student = request.user)
        data = []
        
        institute_detail = student.institution.institute_detail
        contact_detail = student.institution.contact_detail
        institution_doc = student.institution.institution_doc

        # Create a dictionary for InstituteDetail
        institute_detail_dict = {
            'name': institute_detail.name,
            'abbreviation': institute_detail.abbreviation,
            'website': institute_detail.website,
            'established_year': institute_detail.established_year,
            'registration_number': institute_detail.registration_number,
        }

        # Create a dictionary for ContactDetail
        contact_detail_dict = {
            'contact_email': contact_detail.contact_email,
            'contact_phone': contact_detail.contact_phone,
            'address': contact_detail.address,
            'city': contact_detail.city,
            'state': contact_detail.state,
            'pincode': contact_detail.pincode,
            'country': contact_detail.country,
        }

        # Create a dictionary for InstituteDoc
        institute_doc_dict = {
            'logo': institution_doc.logo.url if institution_doc.logo else None,
            'scholarships_offered': list(institution_doc.scholarships_offered.values_list('name', flat=True)),
            'accredited_by': list(institution_doc.accredited_by.values_list('name', flat=True)),
            'affiliation_document': institution_doc.affiliation_document.url if institution_doc.affiliation_document else None,
        }

        # Create a dictionary for PersonalDetail
        personal_detail_dict = {
            'First name': student.personal_detail.first_name,
            'Last name': student.personal_detail.last_name,
            'Enrollment number': student.personal_detail.enrollment_number,
            'Date of birth': student.personal_detail.date_of_birth,
        }

        # Create a dictionary for ContactDetail
        contact_detail_dict = {
            'Email id': student.contact_detail.contact_email,
            'Phone Number': student.contact_detail.contact_phone,
            'Address': student.contact_detail.address,
            'City': student.contact_detail.city,
            'State': student.contact_detail.state,
            'Pincode': student.contact_detail.pincode,
            'Country': student.contact_detail.country,
        }

        # Create a dictionary for GuardianDetail
        guardian_detail_dict = {
            'Guardian name': student.guardian_detail.guardian_name,
            'Guardian phone': student.guardian_detail.guardian_phone,
            'Guardian email': student.guardian_detail.guardian_email,
            'Guardian gender': student.guardian_detail.guardian_gender,
        }

        # Create a dictionary for FileDetail
        file_detail_dict = {
            'Profile picture': student.file_detail.profile_pic.url if student.file_detail.profile_pic else "thehe",
            'Signature': student.file_detail.signature.url if student.file_detail.signature else None,
            'Aadhaar': student.file_detail.aadhaar.url if student.file_detail.aadhaar else None,
            'Income certificate': student.file_detail.income_cert.url if student.file_detail.income_cert else None,
        }
        data.append(personal_detail_dict)
        data.append(contact_detail_dict)
        data.append(guardian_detail_dict)
        data.append(institute_detail_dict)
        data.append(institute_doc_dict)
        data.append(file_detail_dict)
        # print(data[0])

        username = request.user.username
        email = request.user.email
        
        return render(request, 'ScholarLink/profile.html' , {'data':data, 'username':username, 'email':email})
    except Exception as e:
        print(e)
        return HttpResponseRedirect(reverse("index"))

def dashboard(request):
    if request.user.is_authenticated:
        scholarship_data = Scholarship.objects.all().values()
        print(scholarship_data)
        username = request.user.username
        email = request.user.email
        
        print(username, email)

        return render(request, 'ScholarLink/Dashboard.html', {'scholarship_data':scholarship_data, 'username': username, 'email':email})
    else:
        return render(request, "ScholarLink/login.html")


def applications(request):
    try:
        student = Student.objects.get(student = request.user)
        data = []
        
        institute_detail = student.institution.institute_detail
        contact_detail = student.institution.contact_detail
        institution_doc = student.institution.institution_doc

        # Create a dictionary for InstituteDetail
        institute_detail_dict = {
            'name': institute_detail.name,
            'abbreviation': institute_detail.abbreviation,
            'website': institute_detail.website,
            'established_year': institute_detail.established_year,
            'registration_number': institute_detail.registration_number,
        }

        # Create a dictionary for ContactDetail
        contact_detail_dict = {
            'contact_email': contact_detail.contact_email,
            'contact_phone': contact_detail.contact_phone,
            'address': contact_detail.address,
            'city': contact_detail.city,
            'state': contact_detail.state,
            'pincode': contact_detail.pincode,
            'country': contact_detail.country,
        }

        # Create a dictionary for InstituteDoc
        institute_doc_dict = {
            'logo': institution_doc.logo.url if institution_doc.logo else None,
            'scholarships_offered': list(institution_doc.scholarships_offered.values_list('name', flat=True)),
            'accredited_by': list(institution_doc.accredited_by.values_list('name', flat=True)),
            'affiliation_document': institution_doc.affiliation_document.url if institution_doc.affiliation_document else None,
        }

        # Create a dictionary for PersonalDetail
        personal_detail_dict = {
            'Firstname': student.personal_detail.first_name,
            'Lastname': student.personal_detail.last_name,
            'Enrollment number': student.personal_detail.enrollment_number,
            'Date of birth': student.personal_detail.date_of_birth,
        }

        # Create a dictionary for ContactDetail
        contact_detail_dict = {
            'Email id': student.contact_detail.contact_email,
            'Phone Number': student.contact_detail.contact_phone,
            'Address': student.contact_detail.address,
            'City': student.contact_detail.city,
            'State': student.contact_detail.state,
            'Pincode': student.contact_detail.pincode,
            'Country': student.contact_detail.country,
        }

        # Create a dictionary for GuardianDetail
        guardian_detail_dict = {
            'Guardian name': student.guardian_detail.guardian_name,
            'Guardian phone': student.guardian_detail.guardian_phone,
            'Guardian email': student.guardian_detail.guardian_email,
            'Guardian gender': student.guardian_detail.guardian_gender,
        }

        # Create a dictionary for FileDetail
        file_detail_dict = {
            'Profile picture': student.file_detail.profile_pic.url if student.file_detail.profile_pic else "thehe",
            'Signature': student.file_detail.signature.url if student.file_detail.signature else None,
            'Aadhaar': student.file_detail.aadhaar.url if student.file_detail.aadhaar else None,
            'Income certificate': student.file_detail.income_cert.url if student.file_detail.income_cert else None,
        }
        # verification = {
        #     'is_verfied':student.is_verified,
        #     'Status' : student.status,
        #     'Reason' : student.reason
        # }
        data.append(personal_detail_dict)
        data.append(contact_detail_dict)
        data.append(guardian_detail_dict)
        data.append(institute_detail_dict)
        data.append(institute_doc_dict)
        data.append(file_detail_dict)
        # data.append(verification)
        # print(verification)

        return render(request, "ScholarLink/applications.html", {'data':data} )
    except Exception as e:
        print(e)
        print("in else")
        return redirect(reverse('dashboard'))


def institute_select(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        institute_name = data.get('institute_name')
        print(institute_name)
        institute_obj = Institution.objects.get(institute_detail__name=institute_name)
        student = Student(student=request.user, institution=institute_obj)
        student.save()

        return HttpResponse(status=204)  

    

def institution(request):
    if request.method == 'POST':
        institute_detail = InstituteDetail.objects.get(user=request.user)
        contact_detail = ContactDetail.objects.get(user=request.user)
        institute_doc = InstituteDoc.objects.get(user=request.user)

        institute = Institution(institute=request.user, institute_detail=institute_detail, contact_detail=contact_detail, institution_doc=institute_doc)
        institute.save()
        return HttpResponse(status=204)
    else:    
        return render(request, "ScholarLink/institution.html")
    

def institution_detail(request):
    if request.method == 'PUT':
        data = json.loads(request.body)

        name = data.get('name')
        abbreviation = data.get('abbreviation')
        established_year = data.get('established_year')
        registration_number = data.get('registration_number')
        website = data.get('website')

        if InstituteDetail.objects.filter(user=request.user):
            institute_detail = InstituteDetail.objects.get(user=request.user)
            institute_detail.name=name
            institute_detail.abbreviation=abbreviation
            institute_detail.established_year=established_year
            institute_detail.registration_number=registration_number
            institute_detail.website=website
            institute_detail.save()
        else:
            institute_detail = InstituteDetail(
                user=request.user, name=name, abbreviation=abbreviation, established_year=established_year, registration_number=registration_number, website=website)
            institute_detail.save()

        return HttpResponse(status=204) 


def institution_doc(request):
    if request.method == 'POST':

        print(request.FILES)

        logo = request.FILES.get('logo')
        affiliation_document = request.FILES.get('affiliation_document')

        print(logo, affiliation_document)

        if InstituteDoc.objects.filter(user=request.user):
            institute_doc = InstituteDoc.objects.get(user=request.user)
            institute_doc.logo = logo
            institute_doc.affiliation_document = affiliation_document
            institute_doc.save()
        else:
            institute_doc = InstituteDoc(user=request.user, logo=logo, affiliation_document=affiliation_document)
            institute_doc.save()

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


    


