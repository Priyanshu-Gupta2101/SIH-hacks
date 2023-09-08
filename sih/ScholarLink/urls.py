from django.urls import path

from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
    path('student_register/', views.student_register, name="student_register"),

]