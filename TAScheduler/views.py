from django.shortcuts import render, redirect
from django.views import View
from classes import account, section, course


# Create your views here.
class Accounts(View):
    def get(self, request):
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        return render(request, "accounts.html", {"email": request.session["email"],
                                                 "account_type": request.session["account_type"]})

    def post(self, request):
        pass


class Courses(View):
    def get(self, request):
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        return render(request, "courses.html", {"email": request.session["email"],
                                                "account_type": request.session["account_type"]})

    def post(self, request):
        pass


class CreateAccount(View):
    def get(self, request):
        """
        Get method for the CreateAccount view.
        :param request: An HttpResponse object. request.session["email"] contains the logged in account's username,
            and request.session["account_type"] its type.
        :return: If the user is not logged in, redirect the user to the login page.
            Else return a render of the createAccount template.
        """
        # TODO check that the user is logged in as an admin?
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        return render(request, "createAccount.html", {"email": request.session["email"],
                                                      "account_type": request.session["account_type"]})

    def post(self, request):
        """
        Post method for the CreateAccount view. If request.POST.dict() contains the correct keys, then a new account
            is created using the values assigned to those keys.
        :param request: An HttpResponse object. request.session["email"] contains the logged in account's username,
            and request.session["account_type"] contains its account type.
            The dictionary request.POST.dict() must contain entries with keys "email", "password",
            "account_type", "first_name", and "last_name".
        :return: If request.POST.dict() does not contain the above fields, then return a render of
            the createAccount template. Else return a redirect to (the dashboard?).
        """
        # TODO improve error message?
        # TODO check that the user is logged in as an admin?
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        created_account = account.create_account(request.POST.dict())
        if created_account is None:
            return render(request, "createAccount.html",
                          {"email": request.session["email"], "account_type": request.session["account_type"],
                           "error_message": "Error creating the account. A user with this email may already exist."})
        return redirect('/accounts/', {"email": request.session["email"],
                                      "account_type": request.session["account_type"]})


class CreateCourse(View):
    def get(self, request):
        """

        """
        # TODO
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        return render(request, "createCourse.html", {"email": request.session["email"],
                                                     "account_type": request.session["account_type"]})

    def post(self, request):
        """

        """
        # TODO
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        created_course = course.create_course(request.POST["course_name"])
        if created_course is None:
            return render(request, "createCourse.html",
                          {"email": request.session["email"], "account_type": request.session["account_type"],
                           "error_message": "Error creating the course."})
        return redirect('/courses/', {"email": request.session["email"],
                                        "account_type": request.session["account_type"]})


class CreateLab(View):
    def get(self, request):
        # TODO
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        courses = course.course_list()
        return render(request, "createLab.html", {"email": request.session["email"],
                                                  "account_type": request.session["account_type"],
                                                  'courses': courses})

    def post(self, request):
        # TODO
        course_id = request.POST.get('course_id')
        course_object = course.get_course_by_id(course_id)
        if course_object is None:
            return render(request, "createLab.html",
                          {"email": request.session["email"], "account_type": request.session["account_type"],
                           "error_message": "Course not found."})
        else:
            lab_name = request.POST.get('lab_name')
            created_lab = section.create_section(lab_name, course_object)
        if created_lab is None:
            return render(request, "createLab.html",
                          {"email": request.session["email"], "account_type": request.session["account_type"],
                           "error_message": "Class ID or TA ID does not exist"})
        return redirect('/courses/', {"email": request.session["email"],
                                      "account_type": request.session["account_type"]})


class Dashboard(View):
    def get(self, request):
        """
        Get method for the dashboard view.
        :param request: An HttpResponse object. request.session["email"] contains the logged in account's username,
            and request.session["account_type"] contains the account's type.
        :return: If the user is not logged in, redirect the user to the login page.
            Else return a render of the dashboard.
        """
        if "email" not in request.session:
            return redirect('/', {"email": "", "account_type": ""})
        if "account_type" not in request.session:
            request.session["account_type"] = ""

        # I'm not sure if this next check is necessary
        user = account.get_account(request.session["email"])
        if user is None:
            return redirect('/', {"email": "", "account_type": ""})

        return render(request, "dashboard.html", {"email": request.session["email"],
                                                  "account_type": request.session["account_type"]})

    def post(self, request):
        pass


class Database(View):
    def get(self, request):
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        return render(request, "database.html", {"email": request.session["email"],
                                                 "account_type": request.session["account_type"]})

    def post(self, request):
        pass


class EditAccount(View):
    def get(self, request):
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        return render(request, "editAccount.html", {"email": request.session["email"],
                                                    "account_type": request.session["account_type"]})

    def post(self, request):
        pass


class LoginPage(View):
    def get(self, request):
        """
        Get method for the LoginPage.
        :param request: An HttpRequest object from the loginPage template.
        :return: A render of the request and loginPage.html.
        """
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        return render(request, "loginPage.html", {"email": "", "account_type": ""})

    def post(self, request):
        """
        Post method for the LoginPage.
        :param request: An HttpRequest object from the loginPage template.
            request.POST['username'] and request.POST['password'] must be
            nonempty strings.
            If the login is successful, then the username will be added to
            the dictionary request.session with key "email", and the account type with key "account_type".
        :return: If request.POST['username'] and
            request.POST['password'] match a username and password in the database,
            then returns a redirect to the dashboard page.
            Else returns the same as LoginPage.get, but with a failed login message.
        """
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        email_attempt = request.POST["username"]
        password_attempt = request.POST["password"]

        if account.valid_login(email_attempt, password_attempt):
            request.session["email"] = email_attempt
            request.session["account_type"] = ""  # TODO: get account type from a static account method
            return redirect('/dashboard/', {"email": request.session["email"],
                                            "account_type": request.session["account_type"]})
        else:
            return render(request, "loginPage.html",
                          {"email": "", "account_type": "", "login_error_message": "Invalid username or password."})


class Notifications(View):
    def get(self, request):
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        return render(request, "notifications.html", {"email": request.session["email"],
                                                      "account_type": request.session["account_type"]})

    def post(self, request):
        pass
