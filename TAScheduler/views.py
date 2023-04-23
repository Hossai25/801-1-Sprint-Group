from django.shortcuts import render, redirect
from django.views import View
from classes import account, course, section

# Create your views here.
class Accounts(View):
    def get(self,request):
        return render(request,"accounts.html",{})

    def post(self,request):
        pass

class Courses(View):
    def get(self,request):
        return render(request, "courses.html", {})

    def post(self,request):
        pass

class CreateAccount(View):
    def get(self,request):
        # TODO
        return render(request, "createAccount.html", {})

    def post(self,request):
        # TODO
        pass

class CreateCourse(View):
    def get(self,request):
        # TODO
        return render(request, "createCourse.html", {})

    def post(self,request):
        # TODO
        pass

class CreateLab(View):
    def get(self,request):
        # TODO
        return render(request, "createLab.html", {})

    def post(self,request):
        # TODO
        pass

class Dashboard(View):
    def get(self,request):
        """
        Get method for the dashboard view.
        :param request: An HttpResponse object. request.session["email"] contains the logged in account's username.
        :return: If the user is not logged in, redirect the user to the login page. (is this right?)
            Else return a render of the dashboard.
        """
        if "email" not in request.session:
            return redirect('/')

        user = account.get_account(request.session["email"])
        if user is None:
            return redirect('/')

        return render(request, "dashboard.html", {})

    def post(self,request):
        # TODO: redirect to pressed button?
        pass

class Database(View):
    def get(self,request):
        return render(request, "database.html", {})

    def post(self,request):
        pass

class EditAccount(View):
    def get(self, request):
        return render(request, "editAccount.html", {})

    def post(self, request):
        pass

class LoginPage(View):
    def get(self, request):
        """
        Get method for the LoginPage.
        :param request: An HttpRequest object from the loginPage template.
        :return: A render of the request and loginPage.html.
        """
        return render(request, "loginPage.html", {})

    def post(self, request):
        """
        Post method for the LoginPage.
        :param request: An HttpRequest object from the loginPage template.
            request.POST['username'] and request.POST['password'] must be
            nonempty strings.
            If the login is successful, then the username will be added to
            the dictionary request.session with key "email".
        :return: If request.POST['username'] and
            request.POST['password'] match a username and password in the database,
            then returns a redirect to the dashboard page.
            Else returns the same as LoginPage.get, but with a failed login message.
        """
        email_attempt = request.POST["username"]
        password_attempt = request.POST["password"]

        if account.valid_login(email_attempt, password_attempt):
            request.session["email"] = email_attempt
            return redirect('/dashboard/')
        else:
            return render(request, "loginPage.html", {"login_error_message": "Invalid username or password."})

class Notifications(View):
    def get(self, request):
        return render(request, "notifications.html", {})

    def post(self, request):
        pass