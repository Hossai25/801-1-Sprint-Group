from django.shortcuts import render, redirect
from django.views import View

# Create your views here.
from django.shortcuts import render, redirect
from django.views import View


# Create your views here.
class Accounts(View):
    def get(self, request):
        return render(request, "accounts.html", {})

    def post(self, request):
        pass


class Course(View):
    def get(self, request):
        return render(request, "courses.html", {})

    def post(self, request):
        pass


class CreateAccount(View):
    def get(self, request):
        return render(request, "createAccount.html", {})

    def post(self, request):
        pass


class CreateCourse(View):
    def get(self, request):
        return render(request, "createCourse.html", {})

    def post(self, request):
        pass


class CreateLab(View):
    def get(self, request):
        return render(request, "createLab.html", {})

    def post(self, request):
        pass


class Dashboard(View):
    def get(self, request):
        return render(request, "dashboard.html", {})

    def post(self, request):
        pass


class Database(View):
    def get(self, request):
        return render(request, "database.html", {})

    def post(self, request):
        pass


class EditAccount(View):
    def get(self, request):
        return render(request, "editAccount.html", {})

    def post(self, request):
        pass


class LoginPage(View):
    def get(self, request):
        """
        Get method for the login page.
        :param request:
        :return:
        """
        return render(request, "loginPage.html", {})

    def post(self, request):
        pass


class Notifications(View):
    def get(self, request):
        return render(request, "notifications.html", {})

    def post(self, request):
        pass


class Accounts(View):
    def get(self, request):
        return render(request, "accounts.html", {})

    def post(self, request):
        pass


class Course(View):
    def get(self, request):
        return render(request, "courses.html", {})

    def post(self, request):
        pass


class CreateAccount(View):
    def get(self, request):
        return render(request, "createAccount.html", {})

    def post(self, request):
        pass


class CreateCourse(View):
    def get(self, request):
        return render(request, "createCourse.html", {})

    def post(self, request):
        pass


class CreateLab(View):
    def get(self, request):
        return render(request, "createLab.html", {})

    def post(self, request):
        pass


class Dashboard(View):
    def get(self, request):
        return render(request, "dashboard.html", {})

    def post(self, request):
        pass


class Database(View):
    def get(self, request):
        return render(request, "database.html", {})

    def post(self, request):
        pass


class EditAccount(View):
    def get(self, request):
        return render(request, "editAccount.html", {})

    def post(self, request):
        pass


class LoginPage(View):
    def get(self, request):
        return render(request, "loginPage.html", {})

    def post(self, request):
        pass


class Notifications(View):
    def get(self, request):
        return render(request, "notifications.html", {})

    def post(self, request):
        pass
