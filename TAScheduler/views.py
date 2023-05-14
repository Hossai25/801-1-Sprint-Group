from django.shortcuts import render, redirect
from django.views import View
from classes import account, section, course, ta, instructor
from django.urls import reverse
import re  # regular expressions for parsing strings

from classes.course import Course


class Accounts(View):
    def get(self, request):
        """
        Get method for the Accounts view.
        :param request: An HttpResponse object. request.session["email"] contains the logged in account's username,
            and request.session["account_type"] contains the account's type.
        :return: a render of the accounts page.
        """
        accounts = account.account_list()
        current_account = account.get_account(request.session["email"])
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        return render(request, "accounts.html", {"email": request.session["email"],
                                                 "account_type": request.session["account_type"],
                                                 "user": request.session["user"],
                                                 "current_account": current_account,
                                                 'accounts': accounts,
                                                 "back_href": reverse('dashboard')})

    def post(self, request):
        pass


def deleteAccount(request, user_id):
    account.delete_account(user_id)
    return redirect("/accounts/")


class Courses(View):
    def get(self, request):
        """
        Get method for the Courses view.
        :param request: An HttpResponse object. request.session["email"] contains the logged in account's username,
            and request.session["account_type"] its type.
        :return: a render of the courses page.
        """
        courses = course.course_list()
        user = account.get_account(request.session["email"])
        if user.get_account_type() == "ta":
            assistant = ta.account_to_ta(user.get_primary_key())
            assistant_courses = assistant.get_courses()
            return render(request, "courses.html", {"email": request.session["email"],
                                                    "account_type": request.session["account_type"],
                                                    "user": request.session["user"],
                                                    'courses': courses,
                                                    "assistant_courses": assistant_courses,
                                                    "back_href": reverse('dashboard')})
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        return render(request, "courses.html", {"email": request.session["email"],
                                                "account_type": request.session["account_type"],
                                                "user": request.session["user"],
                                                'courses': courses,
                                                "back_href": reverse('dashboard')})

    def post(self, request):
        pass


def deleteCourse(request, course_id):
    course.delete_course(course_id)
    return redirect("/courses/")


class CreateAccount(View):
    def get(self, request):
        """
        Get method for the CreateAccount view.
        :param request: An HttpResponse object. request.session["email"] contains the logged in account's username,
            and request.session["account_type"] its type.
        :return: Return a render of the createAccount template.
        """
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        return render(request, "createAccount.html", {"email": request.session["email"],
                                                      "account_type": request.session["account_type"],
                                                      "user": request.session["user"],
                                                      "back_href": reverse('accounts')})

    def post(self, request):
        """
        Post method for the CreateAccount view. If request.POST.dict() contains the correct keys, then a new account
            is created using the values assigned to those keys.
        :param request: An HttpResponse object. request.session["email"] contains the logged in account's username,
            and request.session["account_type"] contains its account type.
            The dictionary request.POST.dict() must contain entries with keys "email", "password",
            "account_type", "first_name", and "last_name".
        :return: If request.POST.dict() does not contain the above fields, then return a render of
            the createAccount template with a relevant error message. Else return a redirect to the Accounts page.
        """
        # TODO improve error messages and update acceptance tests accordingly
        if "account_type" not in request.session:
            request.session["account_type"] = ""

        for key in ('email', 'password', 'account_type', 'first_name', 'last_name'):
            if key not in request.POST or request.POST[key] == '':
                return render(request, "createAccount.html",
                              {"email": request.session["email"], "account_type": request.session["account_type"],
                               "user": request.session["user"],
                               "back_href": reverse('accounts'),
                               "error_message": "Error creating the account. A user with this email may already exist."})

        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", request.POST['email']):
            return render(request, "createAccount.html",
                          {"email": request.session["email"], "account_type": request.session["account_type"],
                           "user": request.session["user"],
                           "back_href": reverse('accounts'),
                           "error_message": "Error creating the account. A user with this email may already exist."})
        created_account = account.create_account(request.POST.dict())
        if created_account is None:
            return render(request, "createAccount.html",
                          {"email": request.session["email"], "account_type": request.session["account_type"],
                           "user": request.session["user"],
                           "back_href": reverse('accounts'),
                           "error_message": "Error creating the account. A user with this email may already exist."})
        return redirect('/accounts/', {"email": request.session["email"],
                                       "account_type": request.session["account_type"]})


class CreateCourse(View):
    def get(self, request):
        """
        Get method for the CreateCourse view.
        :param request: An HttpResponse object. request.session["email"] contains the logged in account's username,
            and request.session["account_type"] its type.
        :return: If the user is not logged in, redirect the user to the login page.
            Else return a render of the createAccount template.
        """
        if "account_type" not in request.session:
            request.session["account_type"] = ""

        return render(request, "createCourse.html", {"email": request.session["email"],
                                                     "account_type": request.session["account_type"],
                                                     "user": request.session["user"],
                                                     "back_href": reverse('courses')})

    def post(self, request):
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        key = 'course_name'
        if key not in request.POST or request.POST[key] == '':
            return render(request, "createCourse.html", {"email": request.session["email"],
                                                         "account_type": request.session["account_type"],
                                                         "user": request.session["user"],
                                                         "back_href": reverse('courses'),
                                                         "error_message": "Error creating the course."})

        created_course = course.create_course(request.POST["course_name"])
        if created_course is None:
            return render(request, "createCourse.html",
                          {"email": request.session["email"], "account_type": request.session["account_type"],
                           "user": request.session["user"],
                           "back_href": reverse('courses'),
                           "error_message": "Error creating the course."})
        return redirect('/courses/', {"email": request.session["email"],
                                      "account_type": request.session["account_type"],
                                      "user": request.session["user"]})


class CreateLab(View):
    error_duplicate = "Section name blank or already exists."
    error_no_course = "Course not found."

    # def get(self, request):
    #     if "account_type" not in request.session:
    #         request.session["account_type"] = ""
    #     courses = course.course_list()
    #     return render(request, "createLab.html", {"email": request.session["email"],
    #                                               "account_type": request.session["account_type"],
    #                                               "user": request.session["user"],
    #                                               'courses': courses})
    #
    #
    # def post(self, request):
    #     if "account_type" not in request.session:
    #         request.session["account_type"] = ""
    #     course_id = request.POST.get('course_id')
    #     course_object = course.get_course_by_id(course_id)
    #     if course_object is None:
    #         return render(request, "createLab.html",
    #                       {"email": request.session["email"], "account_type": request.session["account_type"],
    #                        "user": request.session["user"],
    #                        "error_message": CreateLab.error_no_course})
    #     else:
    #         lab_name = request.POST.get('lab_name')
    #         created_lab = section.create_section(lab_name, course_object)
    #     if created_lab is None:
    #         return render(request, "createLab.html",
    #                       {"email": request.session["email"], "account_type": request.session["account_type"],
    #                        "user": request.session["user"],
    #                        "error_message": CreateLab.error_duplicate})
    #     return redirect('/courses/', {"email": request.session["email"],
    #                                   "account_type": request.session["account_type"],
    #                                   "user": request.session["user"]})


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
        user = account.get_account(request.session["email"])
        if user.get_account_type() == "instructor":
            teacher = instructor.account_to_instructor(user.get_primary_key())
            teacher_courses = teacher.get_courses()
            return render(request, "dashboard.html", {"email": request.session["email"],
                                                      "account_type": request.session["account_type"],
                                                      "user": request.session["user"],
                                                      "first_name": user.get_first_name(),
                                                      "last_name": user.get_last_name(),
                                                      "office_hours": user.get_office_hours(),
                                                      "address": user.get_address(),
                                                      "phone_number": user.get_phone_number(),
                                                      "instructor": teacher,
                                                      "teacher_courses": teacher_courses})
        if user.get_account_type() == "ta":
            assistant = ta.account_to_ta(user.get_primary_key())
            assistant_courses = assistant.get_courses()
            assistant_sections = assistant.get_sections()
            return render(request, "dashboard.html", {"email": request.session["email"],
                                                      "account_type": request.session["account_type"],
                                                      "user": request.session["user"],
                                                      "first_name": user.get_first_name(),
                                                      "last_name": user.get_last_name(),
                                                      "office_hours": user.get_office_hours(),
                                                      "address": user.get_address(),
                                                      "phone_number": user.get_phone_number(),
                                                      "ta": assistant,
                                                      "assistant_courses": assistant_courses,
                                                      "assistant_sections": assistant_sections})
        if user is None:
            return redirect('/', {"email": "", "account_type": ""})

        if "account_type" not in request.session:
            request.session["account_type"] = ""

        return render(request, "dashboard.html", {"email": request.session["email"],
                                                  "account_type": request.session["account_type"],
                                                  "user": request.session["user"],
                                                  "first_name": user.get_first_name(),
                                                  "last_name": user.get_last_name(),
                                                  "office_hours": user.get_office_hours(),
                                                  "address": user.get_address(),
                                                  "phone_number": user.get_phone_number()})

    def post(self, request):
        pass

    #
    #
    # class Database(View):
    #     def get(self, request):
    #         """
    #         Get method for the Database view.
    #         :param request: An HttpResponse object. request.session["email"] contains the logged in account's username,
    #             and request.session["account_type"] contains the account's type.
    #         :return: a render of the dashboard.
    #         """
    #         if "account_type" not in request.session:
    #             request.session["account_type"] = ""
    #         return render(request, "database.html", {"email": request.session["email"],
    #                                                  "account_type": request.session["account_type"],
    #                                                  "user": request.session["user"]})
    #
    # def post(self, request):
    #     pass


class DisplayCourse(View):
    error_duplicateta = "TA is already in this course"
    error_duplicateinstructor = "Instructor is already in this course"
    error_duplicatesection = "A section with this name already exists"
    error_nosuchinstructor = "The instructor could not be found"
    error_nosuchta = "The TA could not be found"

    def get_context(self, request, course_id):
        # TODO: unit tests
        course_obj = course.get_course_by_id(course_id)
        ta_list = ta.get_all_tas()
        instructor_list = instructor.get_all_instructors()
        course_tas = ta.get_course_tas(course_id)
        for course_ta in course_tas:
            course_ta.grader_status = course_ta.get_grader_status(course_id)
            course_ta.number_sections = course_ta.get_number_sections(course_id)
            course_ta.current_number_sections = len(course_ta.get_sections())
        course_instructor = instructor.get_course_instructor(course_id)
        sections = section.section_list(course_id)
        for section_obj in sections:
            section_obj.ta = ta.get_section_ta(section_obj.get_primary_key())
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        context = {"email": request.session["email"],
                   "account_type": request.session["account_type"],
                   "user": request.session["user"],
                   'course': course_obj,
                   'course_tas': course_tas,
                   'course_instructor': course_instructor,
                   'ta_list': ta_list,
                   'instructor_list': instructor_list,
                   "sections": sections,
                   "back_href": reverse('courses')}
        return context

    def get(self, request, course_id):
        context = self.get_context(request, course_id)
        return render(request, "displayCourse.html", context)

    def post(self, request, course_id):
        if 'submitTa' in request.POST:
            new_ta = ta.account_to_ta(request.POST.get('ta_id'))
            if new_ta is None:
                context = self.get_context(request, course_id)
                context["error_ta"] = DisplayCourse.error_nosuchta
                return render(request, "displayCourse.html", context)
            new_course_ta = new_ta.add_to_course(course_id)
            if new_course_ta is None:
                context = self.get_context(request, course_id)
                context["error_ta"] = DisplayCourse.error_duplicateta
                return render(request, "displayCourse.html", context)
            else:
                new_ta.set_grader_status(course_id, request.POST.get('is_grader'))
                new_ta.set_number_sections(course_id, request.POST.get('number_of_labs'))
                context = self.get_context(request, course_id)
        elif 'submitInstructor' in request.POST:
            new_user = account.get_account_by_id(request.POST.get('instructor_id'))
            if new_user is None:
                context = self.get_context(request, course_id)
                context["error_instructor"] = DisplayCourse.error_nosuchinstructor
                return render(request, "displayCourse.html", context)
            new_instructor = instructor.Instructor(new_user)
            new_course_instructor = new_instructor.add_to_course(course_id)
            if new_course_instructor is None:
                context = self.get_context(request, course_id)
                context["error_instructor"] = DisplayCourse.error_duplicateinstructor
                return render(request, "displayCourse.html", context)
            else:
                context = self.get_context(request, course_id)
        elif 'submitSection' in request.POST:
            section_name = request.POST.get('section_name')
            new_section = section.create_section(section_name, course.get_course_by_id(course_id))
            if new_section is None:
                context = self.get_context(request, course_id)
                context["error_section"] = DisplayCourse.error_duplicatesection
            elif 'ta' in request.POST and request.POST.get('ta') != 'None':
                new_section_ta = ta.account_to_ta(request.POST.get('ta'))
                if new_section_ta is None:
                    context = self.get_context(request, course_id)
                    context["error_section"] = DisplayCourse.error_nosuchta
                    return render(request, "displayCourse.html", context)
                new_section_ta.add_to_section(new_section.get_primary_key())
                context = self.get_context(request, course_id)
        return render(request, "displayCourse.html", context)


def deleteCourseTa(request, course_id, user_id):
    ta_obj = ta.account_to_ta(user_id)
    ta_obj.remove_from_course(course_id)
    return redirect(f"/courses/view/{course_id}/")


def deleteSection(request, course_id, section_id):
    section.delete_section(section_id)
    return redirect(f"/courses/view/{course_id}")


class EditAccount(View):
    def get(self, request, user_id):
        """
        Get method for the EditAccount view.
        :param request: An HttpResponse object. request.session["email"] contains the logged in account's username,
            and request.session["account_type"] contains the account's type.
        :return: a render of the editAccount page.
        """
        userView = account.get_account_by_id(user_id)
        current_user = account.get_account_by_id(request.session["user"])
        if "account_type" not in request.session:
            request.session["account_type"] = ""

        if current_user.get_primary_key() == userView.get_primary_key():
            back_href = reverse('dashboard')
        else:
            back_href = reverse('accounts')

        return render(request, "editAccount.html", {"email": request.session["email"],
                                                    "account_type": request.session["account_type"],
                                                    "user": request.session["user"],
                                                    'account': userView,
                                                    "current_user": current_user,
                                                    "back_href": back_href})

    def post(self, request, user_id):
        userView = account.get_account_by_id(user_id)
        current_user = account.get_account_by_id(request.session["user"])
        edited_account = account.edit_account(user_id, request.POST.dict())
        accounts = account.account_list()

        if current_user.get_primary_key() == userView.get_primary_key():
            return redirect(reverse('dashboard'))
        else:
            return redirect(reverse('accounts'))


class EditCourseTa(View):
    def get(self, request, course_id, user_id):
        """
        Get method for the EditCourseTa view.
        :param request: An HttpResponse object. request.session["email"] contains the logged in account's username,
            and request.session["account_type"] contains the account's type.
        :return: a render of the EditCourseTa page.
        """
        selected_ta = ta.account_to_ta(user_id)
        course_obj = course.get_course_by_id(course_id)
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        selected_ta.grader_status = selected_ta.get_grader_status(course_id)
        selected_ta.number_sections = selected_ta.get_number_sections(course_id)
        return render(request, "editCourseTa.html", {"email": request.session["email"],
                                                     "account_type": request.session["account_type"],
                                                     "user": request.session["user"],
                                                     'selected_ta': selected_ta,
                                                     'course': course_obj,
                                                     "back_href": reverse("displayCourse",
                                                                          kwargs={'course_id': course_id})})

    def post(self, request, course_id, user_id):
        selected_ta = ta.account_to_ta(user_id)
        course_obj = course.get_course_by_id(course_id)
        selected_ta.set_grader_status(course_id, request.POST.get('is_grader'))
        selected_ta.set_number_sections(course_id, request.POST.get('number_of_labs'))
        return redirect(reverse('displayCourse', kwargs={'course_id': course_id}))


class EditSection(View):
    def get(self, request, course_id, section_id):
        selected_section = section.get_section_by_id(section_id)
        course_obj = course.get_course_by_id(course_id)
        selected_section.ta = ta.get_section_ta(section_id)
        course_obj.tas = ta.get_course_tas(course_id)
        for course_ta in course_obj.tas:
            course_ta.number_sections = course_ta.get_number_sections(course_id)
            course_ta.current_number_sections = len(course_ta.get_sections())
        return render(request, "editSection.html", {"email": request.session["email"],
                                                    "account_type": request.session["account_type"],
                                                    "user": request.session["user"],
                                                    'selected_section': selected_section,
                                                    'course': course_obj,
                                                    "back_href": reverse("displayCourse",
                                                                         kwargs={'course_id': course_id})})

    def post(self, request, course_id, section_id):
        selected_section = section.get_section_by_id(section_id)
        course_obj = course.get_course_by_id(course_id)
        selected_section_ta = ta.get_section_ta(section_id)

        if "ta" in request.POST and request.POST.get("ta") != "":
            new_ta = ta.account_to_ta(request.POST.get("ta"))
        else:
            new_ta = ""

        if selected_section_ta is not None:
            if new_ta == "":
                selected_section_ta.remove_from_section(selected_section.get_primary_key())
            elif new_ta.get_primary_key() != selected_section_ta.get_primary_key():
                selected_section_ta.remove_from_section(selected_section.get_primary_key())
                new_ta.add_to_section(selected_section.get_primary_key())
        else:
            if new_ta != "":
                new_ta.add_to_section(selected_section.get_primary_key())

        """
        if False:  # if bad data
            selected_section.ta = selected_session_ta
            course_obj.tas = ta.get_course_tas(course_id)
            for course_ta in course_obj.tas:
                course_ta.number_sections = course_ta.get_number_sections(course_id)
                course_ta.current_number_sections = len(course_ta.get_sections())
            return render(request, "editSection.html", {"email": request.session["email"],
                                                        "account_type": request.session["account_type"],
                                                        "user": request.session["user"],
                                                        'selected_section': selected_section,
                                                        'course': course_obj,
                                                        "error_message": '',
                                                        "back_href": reverse('displayCourse', kwargs={'course_id': course_id})})
        """
        return redirect(reverse('displayCourse', kwargs={'course_id': course_id}))


class LoginPage(View):
    def get(self, request):
        """
        Get method for the LoginPage.
        :param request: An HttpRequest object from the loginPage template.
        :return: A render of the loginPage.
        """
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        return render(request, "loginPage.html", {"email": "", "account_type": "", "user": ""})

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
            Else returns a render of the loginPage with a failed login message.
        """
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        email_attempt = request.POST["username"]
        password_attempt = request.POST["password"]

        if account.valid_login(email_attempt, password_attempt):
            user = account.get_account(email_attempt)
            request.session["email"] = user.get_email()
            request.session["account_type"] = user.get_account_type()
            request.session["user"] = user.get_primary_key()
            return redirect('/dashboard/', {"email": request.session["email"],
                                            "account_type": request.session["account_type"],
                                            "user": request.session["user"]})
        else:
            return render(request, "loginPage.html",
                          {"email": "", "account_type": "", "user": "",
                           "login_error_message": "Invalid username or password."})


class Notifications(View):
    def get(self, request):
        """
        Get method for the Notifications view.
        :param request: An HttpResponse object. request.session["email"] contains the logged in account's username,
            and request.session["account_type"] contains the account's type.
        :return: a render of the notifications page.
        """
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        return render(request, "notifications.html", {"email": request.session["email"],
                                                      "account_type": request.session["account_type"],
                                                      "user": request.session["user"],
                                                      "back_href": reverse("dashboard")})

    def post(self, request):
        pass
