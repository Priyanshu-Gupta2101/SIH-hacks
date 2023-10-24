from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('student/', views.student, name="student"),
    path('personal_detail/', views.personal_detail, name="personal_detail"),
    path('contact_detail/', views.contact_detail, name="contact_detail"),
    path('guardian_detail/', views.guardian_detail, name="guardian_detail"),
    path('file_detail/', views.file_detail, name="file_detail"),
    path('institution/', views.institution, name="institution"),
    path('institution_detail/', views.institution_detail, name="institution_detail"),
    path('institution_doc/', views.institution_doc, name="institution_doc"),
    path('institute_select/', views.institute_select, name="institute_select"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('student_profile/', views.student_profile_dashboard, name='student_profile_dashboard'),
    path('applications/', views.applications, name='applications'),
    path('faqs/', views.faq, name='faq'),
    path('institution_profile/', views.institution_profile_dashboard, name='institution_profile_dashboard'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)