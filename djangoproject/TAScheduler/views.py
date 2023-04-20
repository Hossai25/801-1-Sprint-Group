from django.shortcuts import render, redirect
from django.views import View

# Create your views here.
class Accounts(View):
    def get(self,request):
        return render(request,"accounts.html",{})

    def post(self,request):

class Course(View):
    def get(self,request):
        return render(request, "courses.html", {})

    def post(self,request):

class CreateAccount(View):
    def get(self,request):
        return render(request, "createAccount.html", {})

    def post(self,request):

class CreateCourse(View):
    def get(self,request):
        return render(request, "createCourse.html", {})

    def post(self,request):

class CreateLab(View):
    def get(self,request):
        return render(request, "createLab.html", {})

    def post(self,request):

class Dashboard(View):
    def get(self,request):
        return render(request, "dashboard.html", {})

    def post(self,request):

class Database(View):
    def get(self,request):
        return render(request, "database.html", {})

    def post(self,request):

class EditAccount(View):
    def get(self, request):
        return render(request, "editAccount.html", {})

    def post(self, request):

class LoginPage(View):
    def get(self, request):
        return render(request, "loginPage.html", {})

    def post(self, request):

class Notifications(View):
    def get(self, request):
        return render(request, "notifications.html", {})

    def post(self, request):