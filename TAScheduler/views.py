from django.shortcuts import render, redirect
from django.views import View
from TAScheduler import forms
from classes import account, section, course, ta, instructor
from django.urls import reverse
import re  # regular expressions for parsing strings


class Accounts(View):
    def get(self, request):
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


def deleteAccount(request, user_id):
    account.delete_account(user_id)
    return redirect("/accounts/")


class Courses(View):
    def get(self, request):
        courses = course.course_list()
        user = account.get_account(request.session["email"])
        assistant_courses = []

        if user.get_account_type() == "ta":
            assistant = ta.account_to_ta(user.get_primary_key())
            assistant_courses = assistant.get_courses()

        if "account_type" not in request.session:
            request.session["account_type"] = ""

        return render(request, "courses.html", {"email": request.session["email"],
                                                "account_type": request.session["account_type"],
                                                "user": request.session["user"],
                                                'courses': courses,
                                                "assistant_courses": assistant_courses,
                                                "back_href": reverse('dashboard')})


def deleteCourse(request, course_id):
    course.delete_course(course_id)
    return redirect("/courses/")


class CreateAccount(View):

    def get(self, request):
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        return render(request, "createAccount.html", {"email": request.session["email"],
                                                      "account_type": request.session["account_type"],
                                                      "user": request.session["user"],
                                                      "back_href": reverse('accounts')})

    def render_error(self, request, error_message):
        return render(request, "createAccount.html", {"email": request.session["email"],
                                                      "account_type": request.session["account_type"],
                                                      "user": request.session["user"],
                                                      "back_href": reverse('accounts'),
                                                      "error_message": error_message})

    def post(self, request):
        if "account_type" not in request.session:
            request.session["account_type"] = ""

        for key in ('email', 'password', 'account_type', 'first_name', 'last_name'):
            if key not in request.POST or request.POST[key] == '':
                return self.render_error(request, "Error creating the account. A user with this email may already "
                                                  "exist.")

        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", request.POST['email']):
            return self.render_error(request, "Error creating the account. A user with this email may already exist.")
        created_account = account.create_account(request.POST.dict())
        if created_account is None:
            return self.render_error(request, "Error creating the account. A user with this email may already exist.")
        return redirect('/accounts/', {"email": request.session["email"],
                                       "account_type": request.session["account_type"]})


class CreateCourse(View):
    def get(self, request):
        if "account_type" not in request.session:
            request.session["account_type"] = ""

        return render(request, "createCourse.html", {"email": request.session["email"],
                                                     "account_type": request.session["account_type"],
                                                     "user": request.session["user"],
                                                     "back_href": reverse('courses')})

    def render_error(self, request, error_message):
        return render(request, "createAccount.html", {"email": request.session["email"],
                                                      "account_type": request.session["account_type"],
                                                      "user": request.session["user"],
                                                      "back_href": reverse('courses'),
                                                      "error_message": error_message})

    def post(self, request):
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        key = 'course_name'
        if key not in request.POST or request.POST[key] == '':
            return self.render_error(request, "Error creating the course.")

        created_course = course.create_course(request.POST["course_name"])
        if created_course is None:
            return self.render_error(request, "Error creating the course.")
        return redirect('/courses/', {"email": request.session["email"],
                                      "account_type": request.session["account_type"],
                                      "user": request.session["user"]})


class Dashboard(View):
    def get(self, request):
        if "email" not in request.session:
            return redirect('/', {"email": "", "account_type": ""})

        user = account.get_account(request.session["email"])
        account_type = request.session.get("account_type", "")

        if user is None:
            return redirect('/', {"email": "", "account_type": ""})

        common_data = {
            "email": request.session["email"],
            "account_type": account_type,
            "user": request.session["user"],
            "first_name": user.get_first_name(),
            "last_name": user.get_last_name(),
            "office_hours": user.get_office_hours(),
            "address": user.get_address(),
            "phone_number": user.get_phone_number()
        }

        if user.get_account_type() == "instructor":
            teacher = instructor.account_to_instructor(user.get_primary_key())
            teacher_courses = teacher.get_courses()
            common_data.update({"instructor": teacher, "teacher_courses": teacher_courses})

        if user.get_account_type() == "ta":
            assistant = ta.account_to_ta(user.get_primary_key())
            assistant_courses = assistant.get_courses()
            for course_obj in assistant_courses:
                course_obj.ta_is_grader = assistant.get_grader_status(course_obj.get_primary_key())
            assistant_sections = assistant.get_sections()
            common_data.update(
                {"ta": assistant, "assistant_courses": assistant_courses, "assistant_sections": assistant_sections})

        return render(request, "dashboard.html", common_data)


class DisplayCourse(View):
    error_duplicateta = "TA is already in this course"
    error_duplicateinstructor = "Instructor is already in this course"
    error_duplicatesection = "A section with this name already exists"
    error_nosuchinstructor = "The instructor could not be found"
    error_nosuchta = "The TA could not be found"

    def get_context(self, request, course_id):
        course_obj = course.get_course_by_id(course_id)
        current_user = account.get_account(request.session["email"])
        ta_list = ta.get_all_tas()
        instructor_list = instructor.get_all_instructors()
        course_tas = ta.get_course_tas(course_id)
        for course_ta in course_tas:
            course_ta.grader_status = course_ta.get_grader_status(course_id)
            course_ta.number_sections = course_ta.get_number_sections(course_id)
            course_ta.current_number_sections = 0
            for ta_lab in course_ta.get_sections():
                if ta_lab.course_model.pk == course_obj.get_primary_key():
                    course_ta.current_number_sections += 1
        course_instructor = instructor.get_course_instructor(course_id)
        sections = section.section_list(course_id)
        for section_obj in sections:
            section_obj.ta = ta.get_section_ta(section_obj.get_primary_key())
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        context = {"email": request.session["email"],
                   "account_type": request.session["account_type"],
                   "user": request.session["user"],
                   'current_user': current_user,
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
            if new_course_ta is False:
                context = self.get_context(request, course_id)
                context["error_ta"] = DisplayCourse.error_duplicateta
                return render(request, "displayCourse.html", context)
            else:
                new_ta.set_grader_status(course_id, request.POST.get('is_grader'))
                new_ta.set_number_sections(course_id, request.POST.get('number_of_labs'))

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

        elif 'submitSection' in request.POST:
            section_name = request.POST.get('section_name')
            new_section = section.create_section(section_name, course.get_course_by_id(course_id))
            if new_section is None:
                context = self.get_context(request, course_id)
                context["error_section"] = DisplayCourse.error_duplicatesection
                return render(request, "displayCourse.html", context)
            if 'ta' in request.POST and request.POST.get('ta') != 'None':
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
    error_invalidinput = "Error editing the account. Invalid input"

    def get(self, request, user_id):
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

        form = forms.EditAccountForm(request.POST)
        if not form.is_valid():
            if current_user.get_primary_key() == userView.get_primary_key():
                back_href = reverse('dashboard')
            else:
                back_href = reverse('accounts')
            return render(request, "editAccount.html", {"email": request.session["email"],
                                                        "account_type": request.session["account_type"],
                                                        "user": request.session["user"],
                                                        'account': userView,
                                                        "current_user": current_user,
                                                        "back_href": back_href,
                                                        "error_message": self.error_invalidinput})

        account.edit_account(user_id, request.POST.dict())

        if current_user.get_primary_key() == userView.get_primary_key():
            return redirect(reverse('dashboard'))
        else:
            return redirect(reverse('accounts'))


class EditCourseTa(View):
    def get(self, request, course_id, user_id):
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
        course.get_course_by_id(course_id)
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
            course_ta.current_number_sections = 0
            for ta_lab in course_ta.get_sections():
                if ta_lab.course_model.pk == course_obj.get_primary_key():
                    course_ta.current_number_sections += 1
        return render(request, "editSection.html", {"email": request.session["email"],
                                                    "account_type": request.session["account_type"],
                                                    "user": request.session["user"],
                                                    'selected_section': selected_section,
                                                    'course': course_obj,
                                                    "back_href": reverse("displayCourse",
                                                                         kwargs={'course_id': course_id})})

    def post(self, request, course_id, section_id):
        selected_section = section.get_section_by_id(section_id)
        course.get_course_by_id(course_id)
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
        return redirect(reverse('displayCourse', kwargs={'course_id': course_id}))


class LoginPage(View):
    def get(self, request):
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        return render(request, "loginPage.html", {"email": "", "account_type": "", "user": ""})

    def post(self, request):
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


def logout(request):
    request.session.clear()
    return redirect(reverse('login'))


class Notifications(View):
    def get(self, request):
        if "account_type" not in request.session:
            request.session["account_type"] = ""
        return render(request, "notifications.html", {"email": request.session["email"],
                                                      "account_type": request.session["account_type"],
                                                      "user": request.session["user"],
                                                      "back_href": reverse("dashboard")})
