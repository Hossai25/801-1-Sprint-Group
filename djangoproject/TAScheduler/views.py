from django.shortcuts import render, redirect
from django.views import View

# Create your views here.
class LoginPage(View):
    def get(self, request):
        return render(request, "loginPage.html", {})

    def post(self, request):