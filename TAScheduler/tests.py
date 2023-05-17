import unittest
from django.test import TestCase, Client
from django.urls import reverse
from TAScheduler.models import Course as CourseModel

from TAScheduler.models import User, PublicInfo, PrivateInfo, Course, Lab, CourseTa
from django import urls

from classes.section import create_section


def set_default_session(session: Client.session):
    default_session = {"email": "",
                       "account_type": "",
                       "user": ""}
    for key in default_session.keys():
        if key not in session or session.get(key) is None:
            session[key] = default_session[key]
    session.save()


def login_to_session(user: User, session: Client.session):
    session["email"] = user.email
    session["account_type"] = user.account_type
    session["user"] = str(user.pk)
    session.save()


class Login(TestCase):
    webpage = None
    users = None

    def setUp(self):
        self.webpage = Client()
        self.users = ["test1", "test2"]

        # Fill test database with users
        for i in self.users:
            temp = User(email=i + "@uwm.edu", password=i, account_type="administrator")
            temp.save()
            temp2 = PublicInfo(user_id=temp, first_name=i, last_name=i)
            temp2.save()
            temp3 = PrivateInfo(user_id=temp)
            temp3.save()

    # This test checks to see if the username and password are passed from login into the database
    def test_correctName(self):
        for i in self.users:
            resp = self.webpage.post("/", {"username": i + "@uwm.edu", "password": i},
                                     follow=True)
            self.assertEqual(resp.context["email"], i + "@uwm.edu", "username not passed from login")

    # This test checks to see if upon a successful login the user is brought to the dashboard/homepage
    def test_successfulLogin(self):
        resp = self.webpage.post("/", {"username": "test1@uwm.edu", "password": "test1"},
                                 follow=True)
        self.assertRedirects(resp, "/dashboard/")

    # This test checks to see that if no password is used an error message appears
    def test_noPassword(self):
        resp = self.webpage.post("/", {"username": "test1@uwm.edu", "password": ""},
                                 follow=True)
        self.assertContains(resp, "Invalid username or password.")

    # This test checks to see if the wrong password is used an error message appears
    def test_wrongPassword(self):
        resp = self.webpage.post("/", {"username": "test1@uwm.edu", "password": "password"}, follow=True)
        self.assertContains(resp, "Invalid username or password.")


class Dashboard(TestCase):
    webpage = None
    users = None

    def setUp(self):
        self.webpage = Client()
        self.users = ["test1", "test2"]
        set_default_session(self.webpage.session)

        for i in self.users:
            temp = User(email=i + "@uwm.edu", password=i, account_type="administrator")
            temp.save()
            temp2 = PublicInfo(user_id=temp, first_name=i, last_name=i)
            temp2.save()
            temp3 = PrivateInfo(user_id=temp)
            temp3.save()

    # This test checks to see if the user is redirected to the accounts page when the button is pressed
    def test_accountsClicked(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.get(reverse('dashboard'))
        self.assertContains(resp, '<a class="btn btn-primary" href="%s">Accounts</a>' % reverse('accounts'), html=True)

    # This test checks to see if the user is redirected to the courses page when the button is pressed
    def test_coursesClicked(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.get(reverse('dashboard'))
        self.assertContains(resp, '<a class="btn btn-primary" href="%s">Courses/Labs</a>' % reverse('courses'),
                            html=True)

    # This test checks to see if the user is redirected to the notifications page when the button is pressed
    def test_notificationsClicked(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.get(reverse('dashboard'))
        self.assertContains(resp, '<a class="btn btn-primary" href="%s">Notifications</a>' % reverse('notifications'),
                            html=True)

    # This test checks to see that if the Change Personal info button is pressed it brings the user to the
    # right page
    def test_toEditAccountPage(self):
        session = self.webpage.session
        for user_obj in User.objects.all():
            login_to_session(user_obj, session)
            resp = self.webpage.get(reverse('accounts'))
            self.assertContains(resp,
                                '<a class="container-fluid text-light" href="%s">Change Personal Info</a>'
                                % reverse('editAccount', kwargs={'user_id': session["user"]}), html=True)


class Accounts(TestCase):
    webpage = None
    users = None

    def setUp(self):
        self.webpage = Client()
        self.users = ["test1", "test2"]
        self.account_objs = []
        set_default_session(self.webpage.session)

        # Fill test database with users
        for i in self.users:
            temp = User(email=i + "@uwm.edu", password=i, account_type="admin")
            temp.save()
            temp2 = PublicInfo(user_id=temp, first_name=i, last_name=i)
            temp2.save()
            temp3 = PrivateInfo(user_id=temp)
            temp3.save()
            self.account_objs.append(temp)

    # This test checks to see that if the create account button is pressed it brings the user to the
    # right page
    def test_toCreateAccountPage(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session["account_type"] = "admin"
        session.save()
        resp = self.webpage.get(reverse('accounts'))
        self.assertContains(resp, '<a class="btn btn-primary" href="%s">Create Accounts</a>' % reverse('createAccount'),
                            html=True)

    # This test checks to see that if the Change Personal info button is pressed it brings the user to the
    # right page
    def test_toEditAccountPage(self):
        session = self.webpage.session
        for user_obj in self.account_objs:
            login_to_session(user_obj, session)
            resp = self.webpage.get(reverse('accounts'))
            self.assertContains(resp,
                                '<a class="container-fluid text-light" href="%s">Change Personal Info</a>'
                                % reverse('editAccount', kwargs={'user_id': session["user"]}), html=True)

    # This test checks to see that if the back to dashboard button is pressed it brings the user to
    # the right page
    def test_toHomepage(self):
        session = self.webpage.session
        for user_obj in User.objects.all():
            login_to_session(user_obj, session)
            resp = self.webpage.get(reverse('accounts'))
            self.assertContains(resp,
                                '<a class="btn btn-primary" href="%s">Back to Dashboard</a>' % reverse('dashboard'),
                                html=True)


class CreateAccounts(TestCase):
    webpage = None
    users = None

    def setUp(self):
        self.webpage = Client()
        self.users = ["test1", "test2"]
        set_default_session(self.webpage.session)

        # Fill test database with users
        for i in self.users:
            temp = User(email=i + "@uwm.edu", password=i, account_type="administrator")
            temp.save()
            temp2 = PublicInfo(user_id=temp, first_name=i, last_name=i)
            temp2.save()
            temp3 = PrivateInfo(user_id=temp)
            temp3.save()

    # This test checks to see that when the information is entered correctly user is brought back
    # to dashboard
    def test_checkSuccessfully(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.post(reverse("createAccount"), {"first_name": "Anna", "last_name": "Fronk", "email":
            "avfronk@uwm.edu", "password": "annafronk", "account_type": "administrator"}, follow=True)
        self.assertRedirects(resp, "/accounts/")

    # This test checks if the first name has an invalid input then an error message appears
    def test_checkFirstNameFail(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.post(reverse("createAccount"), {"first_name": "", "last_name": "Fronk", "email":
            "avfronk@uwm.edu", "password": "annafronk", "account_type": "administrator"}, follow=True)
        self.assertContains(resp, "Error creating the account. A user with this email may already exist.")

    # This test checks if the last name has an invalid input that an error message appears
    def test_checkLastNameFail(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.post(reverse("createAccount"), {"first_name": "Anna", "last_name": "", "email":
            "avfronk@uwm.edu", "password": "annafronk", "account_type": "administrator"}, follow=True)
        self.assertContains(resp, "Error creating the account. A user with this email may already exist.")

    # This test checks if the check email has an invalid input that an error message appears
    def test_checkEmailFail(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.post(reverse("createAccount"), {"first_name": "Anna", "last_name": "Fronk", "email":
            "avfronk", "password": "annafronk", "account_type": "administrator"}, follow=True)
        self.assertContains(resp, "Error creating the account. A user with this email may already exist.")

    # This test checks if there is a duplicate email then an error message appears
    def test_duplicateEmail(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.post(reverse("createAccount"), {"first_name": "Anna", "last_name": "Fronk", "email":
            "test1@uwm.edu", "password": "annafronk", "account_type": "administrator"}, follow=True)
        self.assertContains(resp, "Error creating the account. A user with this email may already exist.")

    # This test checks if the password has an invalid input then an error message appears
    def test_checkPasswordFail(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.post(reverse("createAccount"), {"first_name": "Anna", "last_name": "Fronk", "email":
            "avfronk@uwm.edu", "password": "", "account_type": "administrator"}, follow=True)
        self.assertContains(resp, "Error creating the account. A user with this email may already exist.")

    # This test checks if the account type has an invalid input then an error message appears
    def test_checkAccountTypeFail(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.post(reverse("createAccount"), {"first_name": "Anna", "last_name": "Fronk", "email":
            "avfronk@uwm.edu", "password": "annafronk", "account_type": ""}, follow=True)
        self.assertContains(resp, "Error creating the account. A user with this email may already exist.")

    # This test checks to see that if the back to dashboard button is pressed it brings the user to
    # the right page
    def test_toHomepage(self):
        session = self.webpage.session
        for user_obj in User.objects.all():
            login_to_session(user_obj, session)
            resp = self.webpage.get(reverse('createAccount'))
            self.assertContains(resp,
                                '<a class="btn btn-primary" href="%s">Back to Dashboard</a>' % reverse('dashboard'),
                                html=True)

    # This test checks to see if a successful submission is added to the database
    def test_accountAddedToDatabase(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.post(reverse("createAccount"), {"first_name": "Anna", "last_name": "Fronk", "email":
            "avfronk@uwm.edu", "password": "annafronk", "account_type": "administrator"}, follow=True)
        self.assertNotEqual(User.objects.get(email="avfronk@uwm.edu"), None)


class Courses(TestCase):
    webpage = None
    users = None

    def setUp(self):
        self.webpage = Client()
        self.users = ["test1", "test2"]
        set_default_session(self.webpage.session)

        # Fill test database with users
        for i in self.users:
            temp = User(email=i + "@uwm.edu", password=i, account_type="administrator")
            temp.save()
            temp2 = PublicInfo(user_id=temp, first_name=i, last_name=i)
            temp2.save()
            temp3 = PrivateInfo(user_id=temp)
            temp3.save()

    # This test checks to see that if the create course button is pressed it brings the user to the
    # right page
    def test_toCreateCoursePage(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session["account_type"] = "admin"
        session.save()
        resp = self.webpage.get(reverse('courses'))
        self.assertContains(resp, '<a class="btn btn-primary" href="%s">Create Courses</a>' % reverse('createCourse'),
                            html=True)

    # This test checks to see that if the create lab button is pressed it brings the user to the
    # right page
    # def test_toCreateLabPage(self):
    #     session = self.webpage.session
    #     session["email"] = "test1@uwm.edu"
    #     session.save()
    #     resp = self.webpage.get(reverse('courses'))
    #     self.assertContains(resp, '<a class="btn btn-primary" href="%s">Create Courses</a>' % reverse('createCourse'),
    #                         html=True)

    # This test checks to see that if the back to dashboard button is pressed it brings the user to the
    # right page
    def test_toHomepage(self):
        session = self.webpage.session
        for user_obj in User.objects.all():
            login_to_session(user_obj, session)
            resp = self.webpage.get(reverse('courses'))
            self.assertContains(resp,
                                '<a class="btn btn-primary" href="%s">Back to Dashboard</a>' % reverse('dashboard'),
                                html=True)

    # This test checks to see that if the Change Personal info button is pressed it brings the user to the
    # right page
    def test_toEditAccountPage(self):
        session = self.webpage.session
        for user_obj in User.objects.all():
            login_to_session(user_obj, session)
            resp = self.webpage.get(reverse('accounts'))
            self.assertContains(resp,
                                '<a class="container-fluid text-light" href="%s">Change Personal Info</a>'
                                % reverse('editAccount', kwargs={'user_id': session["user"]}), html=True)


class CreateCourse(TestCase):
    webpage = None
    users = None
    courses = None

    def setUp(self):
        self.webpage = Client()
        self.users = ["test1"]
        self.courses = ["Course1", "Course2"]
        set_default_session(self.webpage.session)

        # Fill test database with users
        for i in self.users:
            temp = User(email=i + "@uwm.edu", password=i, account_type="admin")
            temp.save()
            temp2 = PublicInfo(user_id=temp, first_name=i, last_name=i)
            temp2.save()
            temp3 = PrivateInfo(user_id=temp)
            temp3.save()
            for j in self.courses:
                Course(course_name=j, instructor_id=temp).save()

    # This test checks to see after a course is created the user is redirected to the dashboard
    def test_successfulCourseCreation(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.post(reverse("createCourse"), {"course_name": "Course3"}, follow=True)
        self.assertRedirects(resp, "/courses/")

    # This test checks to see if an error appears if a duplicate course is created
    def test_duplicateCourse(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.post(reverse("createCourse"), {"course_name": "Course1"}, follow=True)
        self.assertContains(resp, "Error creating the course.")

    # This test checks to see if an error appears if a blank field is entered
    def test_blankFields(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.post(reverse("createCourse"), {"course_name": ""}, follow=True)
        self.assertContains(resp, "Error creating the course.")

    # This test checks to see if the course is successfully added to the database when it is submitted
    def test_courseAddedToDatabase(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.post(reverse("createCourse"), {"course_name": "Course3"}, follow=True)
        self.assertNotEqual(Course.objects.get(course_name="Course3"), None)

    # This test checks to see that if the Change Personal info button is pressed it brings the user to the
    # right page
    def test_toEditAccountPage(self):
        session = self.webpage.session
        for user_obj in User.objects.all():
            login_to_session(user_obj, session)
            resp = self.webpage.get(reverse('accounts'))
            self.assertContains(resp,
                                '<a class="container-fluid text-light" href="%s">Change Personal Info</a>'
                                % reverse('editAccount', kwargs={'user_id': session["user"]}), html=True)

    # This test checks to see that if the back to dashboard button is pressed it brings the user to
    # the right page
    def test_toHomepage(self):
        session = self.webpage.session
        for user_obj in User.objects.filter(account_type="admin"):
            login_to_session(user_obj, session)
            resp = self.webpage.get(reverse('createCourse'))
            self.assertContains(resp,
                                '<a class="btn btn-primary" href="%s">Back to Dashboard</a>' % reverse('dashboard'),
                                html=True)


class DeleteAccount(TestCase):
    webpage = None
    users = None

    def setUp(self):
        self.webpage = Client()
        self.users = ["test1", "test2"]
        set_default_session(self.webpage.session)
        self.account_objs = []

        # Fill test database with users
        for i in self.users:
            temp = User(email=i + "@uwm.edu", password=i, account_type="admin")
            temp.save()
            temp2 = PublicInfo(user_id=temp, first_name=i, last_name=i)
            temp2.save()
            temp3 = PrivateInfo(user_id=temp)
            temp3.save()
            self.account_objs.append(temp)

        # Instructor User
        newUser = User(email="teacher@uwm.edu", password="teacher", account_type="instructor")
        newUser.save()
        newUser2 = PublicInfo(user_id=newUser, first_name="Tom", last_name="Teacher")
        newUser2.save()
        newUser3 = PrivateInfo(user_id=newUser)
        newUser3.save()

        # TA User
        newta = User(email="ta@uwm.edu", password="ta", account_type="ta")
        newta.save()
        newta2 = PublicInfo(user_id=newta, first_name="Tina", last_name="TA")
        newta2.save()
        newta3 = PrivateInfo(user_id=newta)
        newta3.save()

    # This test checks that once an account is deleted, a user is redirected to the account page
    def test_successfuldeletion(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        temp = User(email="delete@uwm.edu", password="delete", account_type="administrator")
        temp.save()
        temp2 = PublicInfo(user_id=temp, first_name="first", last_name="last")
        temp2.save()
        temp3 = PrivateInfo(user_id=temp)
        temp3.save()
        resp = self.webpage.get(reverse('deleteAccount', args=[temp.pk]))
        self.assertRedirects(resp, "/accounts/")

    # This test checks when deleting an account, any courses connected still exist in the database
    def test_anyclassesconnectedstillexist(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        temp = User(email="delete@uwm.edu", password="delete", account_type="instructor")
        temp.save()
        temp2 = PublicInfo(user_id=temp, first_name="first", last_name="last")
        temp2.save()
        temp3 = PrivateInfo(user_id=temp)
        temp3.save()
        Course(course_name="test", instructor_id=temp).save()
        resp = self.webpage.get(reverse('deleteAccount', args=[temp.pk]))
        self.assertNotEqual(Course(course_name="test", instructor_id=temp), None)

    # This test checks to make sure that a TA can't delete a user account
    def test_tacantdeleteaccount(self):
        session = self.webpage.session
        session["email"] = "ta@uwm.edu"
        session["account_type"] = "ta"
        session.save()
        temp = User(email="delete@uwm.edu", password="delete", account_type="administrator")
        temp.save()
        temp2 = PublicInfo(user_id=temp, first_name="first", last_name="last")
        temp2.save()
        temp3 = PrivateInfo(user_id=temp)
        temp3.save()
        resp = self.webpage.get(reverse('deleteAccount', args=[temp.pk]))
        self.assertEqual(None, self.assertRedirects(resp, "/accounts/"))

    # This test checks to make sure that an instructor can't delete an account
    def test_instructorcantdeleteaccount(self):
        session = self.webpage.session
        session["email"] = "teacher@uwm.edu"
        session["account_type"] = "instructor"
        session.save()
        temp = User(email="delete@uwm.edu", password="delete", account_type="administrator")
        temp.save()
        temp2 = PublicInfo(user_id=temp, first_name="first", last_name="last")
        temp2.save()
        temp3 = PrivateInfo(user_id=temp)
        temp3.save()
        resp = self.webpage.get(reverse('deleteAccount', args=[temp.pk]))
        self.assertEqual(None, self.assertRedirects(resp, "/accounts/"))


class DeleteCourse(TestCase):
    webpage = None
    users = None
    courses = None

    def setUp(self):
        self.webpage = Client()
        self.users = ["test1"]
        self.courses = ["Course1", "Course2"]
        set_default_session(self.webpage.session)

        # Fill test database with users
        for i in self.users:
            temp = User(email=i + "@uwm.edu", password=i, account_type="administrator")
            temp.save()
            temp2 = PublicInfo(user_id=temp, first_name=i, last_name=i)
            temp2.save()
            temp3 = PrivateInfo(user_id=temp)
            temp3.save()
            for j in self.courses:
                Course(course_name=i, instructor_id=temp).save()

            # Instructor User
            newUser = User(email="teacher@uwm.edu", password="teacher", account_type="instructor")
            newUser.save()
            newUser2 = PublicInfo(user_id=newUser, first_name="Tom", last_name="Teacher")
            newUser2.save()
            newUser3 = PrivateInfo(user_id=newUser)
            newUser3.save()

            # TA User
            newta = User(email="ta@uwm.edu", password="ta", account_type="ta")
            newta.save()
            newta2 = PublicInfo(user_id=newta, first_name="Tina", last_name="TA")
            newta2.save()
            newta3 = PrivateInfo(user_id=newta)
            newta3.save()

    # This test checks to see if once a course is successfully created, the user is navigated back to the courses page
    def test_successfuldeletion(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        set_default_session(session)
        session.save()
        temp = User(email="delete@uwm.edu", password="delete", account_type="administrator")
        temp.save()
        temp2 = PublicInfo(user_id=temp, first_name="first", last_name="last")
        temp2.save()
        temp3 = PrivateInfo(user_id=temp)
        temp3.save()
        testcourse = CourseModel.objects.create(course_name="test_course")
        resp = self.webpage.get(reverse('deleteCourse', args=[testcourse.pk]))
        self.assertRedirects(resp, "/courses/")

    # This test checks to see that an insturctor that is connected to a course that is deleted still exists
    def test_instructorstillexists(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        temp = User(email="delete@uwm.edu", password="delete", account_type="instructor")
        temp.save()
        temp2 = PublicInfo(user_id=temp, first_name="first", last_name="last")
        temp2.save()
        temp3 = PrivateInfo(user_id=temp)
        temp3.save()
        tempcourse = Course(course_name="test", instructor_id=temp)
        tempcourse.save()
        resp = self.webpage.get(reverse('deleteCourse', args=[tempcourse.pk]))
        self.assertNotEqual(User(email="delete@uwm.edu", password="delete", account_type="instructor"), None)

    # This test checks that a TA can't delete a course
    def test_tacantdeletecourse(self):
        session = self.webpage.session
        session["email"] = "ta@uwm.edu"
        session["account_type"] = "ta"
        session.save()
        temp = User(email="delete@uwm.edu", password="delete", account_type="administrator")
        temp.save()
        temp2 = PublicInfo(user_id=temp, first_name="first", last_name="last")
        temp2.save()
        temp3 = PrivateInfo(user_id=temp)
        temp3.save()
        testcourse = CourseModel.objects.create(course_name="test_course")
        resp = self.webpage.get(reverse('deleteCourse', args=[testcourse.pk]))
        self.assertEqual(None, self.assertRedirects(resp, "/courses/"))

    # This test checks that an instructor can't delete an a course
    def test_instructorcantdeletecourse(self):
        session = self.webpage.session
        session["email"] = "teacher@uwm.edu"
        session.save()
        temp = User(email="delete@uwm.edu", password="delete", account_type="administrator")
        temp.save()
        temp2 = PublicInfo(user_id=temp, first_name="first", last_name="last")
        temp2.save()
        temp3 = PrivateInfo(user_id=temp)
        temp3.save()
        testcourse = CourseModel.objects.create(course_name="test_course")
        resp = self.webpage.get(reverse('deleteCourse', args=[testcourse.pk]))
        self.assertEqual(None, self.assertRedirects(resp, "/courses/"))


class EditAccount(TestCase):
    webpage = None
    users = None

    def setUp(self):
        self.webpage = Client()
        self.users = ["test1", "test2"]
        set_default_session(self.webpage.session)
        self.account_objs = []

        # Fill test database with users
        for i in self.users:
            temp = User(email=i + "@uwm.edu", password=i, account_type="admin")
            temp.save()
            temp2 = PublicInfo(user_id=temp, first_name=i, last_name=i)
            temp2.save()
            temp3 = PrivateInfo(user_id=temp)
            temp3.save()
            self.account_objs.append(temp)

    # This test checks that you can successfully edit an account
    def test_checkSuccessful(self):
        session = self.webpage.session
        current_user = self.account_objs[0]
        login_to_session(current_user, session)
        temp = User(email="avfronk@uwm.edu", password="annafronk", account_type="admin")
        temp.save()
        temp2 = PublicInfo(user_id=temp, first_name="Anna", last_name="Fronk")
        temp2.save()
        temp3 = PrivateInfo(user_id=temp)
        temp3.save()
        resp = self.webpage.post(reverse("editAccount", kwargs={"user_id": temp.pk}),
                                 {"first_name": "New", "last_name": "Name", "email":
                                     "test1@uwm.edu", "password": "annafronk", "account_type": "admin"})
        self.assertRedirects(resp, "/accounts/")

    # This test checks to see that if the back to dashboard button is pressed it brings the user to
    # the right page
    def test_toHomepage(self):
        session = self.webpage.session
        for user_obj in User.objects.all():
            login_to_session(user_obj, session)
            resp = self.webpage.get(reverse('editAccount', kwargs={'user_id': user_obj.pk}))
            self.assertContains(resp,
                                '<a class="btn btn-primary" href="%s">Back to Dashboard</a>' % reverse('dashboard'),
                                html=True)

    # This test checks to make sure an error is thrown if an invalid first name is entered
    def test_editFirstNameFail(self):
        session = self.webpage.session
        current_user = self.account_objs[0]
        login_to_session(current_user, session)
        temp = User(email="avfronk@uwm.edu", password="annafronk", account_type="admin")
        temp.save()
        temp2 = PublicInfo(user_id=temp, first_name="Anna", last_name="Fronk")
        temp2.save()
        temp3 = PrivateInfo(user_id=temp)
        temp3.save()
        resp = self.webpage.post(reverse("editAccount", kwargs={'user_id': temp.pk}),
                                 {"first_name": "", "last_name": "Name", "email":
                                     "test1@uwm.edu", "password": "annafronk", "account_type": "administrator"})
        self.assertContains(resp, "Error editing the account. Invalid input")

    # This test checks to make sure an error is thrown if an invalid last name is entered
    def test_editLastNameFail(self):
        session = self.webpage.session
        current_user = self.account_objs[0]
        login_to_session(current_user, session)
        temp = User(email="avfronk@uwm.edu", password="annafronk", account_type="admin")
        temp.save()
        temp2 = PublicInfo(user_id=temp, first_name="Anna", last_name="Fronk")
        temp2.save()
        temp3 = PrivateInfo(user_id=temp)
        temp3.save()
        resp = self.webpage.post(reverse("editAccount", kwargs={'user_id': temp.pk}),
                                 {"first_name": "NEw", "last_name": "", "email":
                                     "test1@uwm.edu", "password": "annafronk", "account_type": "administrator"})
        self.assertContains(resp, "Error editing the account. Invalid input")

    # This test checks to make sure an error is thrown if an invalid password is entered
    def test_editPasswordFail(self):
        session = self.webpage.session
        current_user = self.account_objs[0]
        login_to_session(current_user, session)
        temp = User(email="avfronk@uwm.edu", password="annafronk", account_type="admin")
        temp.save()
        temp2 = PublicInfo(user_id=temp, first_name="Anna", last_name="Fronk")
        temp2.save()
        temp3 = PrivateInfo(user_id=temp)
        temp3.save()
        resp = self.webpage.post(reverse("editAccount", kwargs={'user_id': temp.pk}),
                                 {"first_name": "New", "last_name": "Name", "email":
                                     "test1@uwm.edu", "password": "", "account_type": "administrator"})
        self.assertContains(resp, "Error editing the account. Invalid input")

    # This test checks to see if the edited account is updated to the database
    def test_accountUpdatedInDatabase(self):
        session = self.webpage.session
        current_user = self.account_objs[0]
        login_to_session(current_user, session)
        temp = User(email="avfronk@uwm.edu", password="annafronk", account_type="admin")
        temp.save()
        temp2 = PublicInfo(user_id=temp, first_name="Anna", last_name="Fronk")
        temp2.save()
        temp3 = PrivateInfo(user_id=temp)
        temp3.save()
        new_data = {"first_name": "New", "last_name": "Name", "office_hours": "Tues 1-3", "address": "1 Locust St"}
        resp = self.webpage.post(reverse("editAccount", kwargs={"user_id": temp.pk}), new_data)
        self.assertNotEqual(PublicInfo.objects.get(user_id=temp,
                                                   first_name=new_data["first_name"], last_name=new_data["last_name"],
                                                   office_hours=new_data["office_hours"]), PublicInfo.DoesNotExist)
        self.assertNotEqual(PrivateInfo.objects.get(user_id=temp, address=new_data["address"]), PrivateInfo.DoesNotExist)

class EditSection(TestCase):
    webpage = None
    users = None

    def setUp(self):
        self.webpage = Client()
        self.users = ["test1", "test2"]
        set_default_session(self.webpage.session)
        self.account_objs = []

        # Fill test database with users
        for i in self.users:
            temp = User(email=i + "@uwm.edu", password=i, account_type="admin")
            temp.save()
            temp2 = PublicInfo(user_id=temp, first_name=i, last_name=i)
            temp2.save()
            temp3 = PrivateInfo(user_id=temp)
            temp3.save()
            self.account_objs.append(temp)

    #This test checks that a successful edit section takes the user back to the display course page
    def test_successfulEditSection(self):
        session = self.webpage.session
        current_user = self.account_objs[0]
        login_to_session(current_user, session)
        temp = User(email="avfronk@uwm.edu", password="annafronk", account_type="admin")
        temp.save()
        temp2 = PublicInfo(user_id=temp, first_name="Anna", last_name="Fronk")
        temp2.save()
        temp3 = PrivateInfo(user_id=temp)
        temp3.save()
        testcourse = CourseModel.objects.create(course_name="test_course")
        testsection = Lab.objects.create(lab_name="testlab", course_id=testcourse, ta_id=None)
        resp = self.webpage.post(reverse("editSection", kwargs={"course_id": testcourse.pk, "section_id": testsection.pk}),
                                 {"lab_name": "testsection"})
        self.assertRedirects(resp, reverse('displayCourse', kwargs={'course_id': testcourse.id}))

    #This test checks that the back to homepage button works on the edit section page
    def test_toHomepage(self):
        session = self.webpage.session
        for user_obj in User.objects.all():
            login_to_session(user_obj, session)
            testcourse = CourseModel.objects.create(course_name="test_course")
            testsection = Lab.objects.create(lab_name="testlab", course_id=testcourse, ta_id=None)
            resp = self.webpage.get(reverse('editSection', kwargs={"course_id": testcourse.pk, "section_id": testsection.pk}))
            self.assertContains(resp,
                                '<a class="btn btn-primary" href="%s">Back to Dashboard</a>' % reverse('dashboard'),
                                html=True)

    #This test checks that the cancel button appears on the screen
    def test_displayCourseButton(self):
        session = self.webpage.session
        for user_obj in User.objects.all():
            login_to_session(user_obj, session)
            testcourse = CourseModel.objects.create(course_name="test_course")
            testsection = Lab.objects.create(lab_name="testlab", course_id=testcourse, ta_id=None)
            resp = self.webpage.get(reverse('editSection', kwargs={"course_id": testcourse.pk, "section_id": testsection.pk}))
            self.assertContains(resp,
                            '<a class="btn btn-primary" href="%s">Cancel</a>' % reverse('displayCourse', kwargs={'course_id':testcourse.pk}),
                            html=True)


class DisplayCourse(TestCase):
    webpage = None
    users = None
    courses = None

    def setUp(self):
        self.webpage = Client()
        self.users = ["test1"]
        self.courses = ["Course1", "Course2"]
        self.course_objs = []
        set_default_session(self.webpage.session)

        # Fill test database with users
        for i in self.users:
            temp = User(email=i + "@uwm.edu", password=i, account_type="admin")
            temp.save()
            temp2 = PublicInfo(user_id=temp, first_name=i, last_name=i)
            temp2.save()
            temp3 = PrivateInfo(user_id=temp)
            temp3.save()
            for j in self.courses:
                temp_model = Course(course_name=i, instructor_id=temp)
                self.course_objs.append(temp_model)
                temp_model.save()

                # Instructor User
        newUser = User(email="teacher@uwm.edu", password="teacher", account_type="instructor")
        newUser.save()
        newUser2 = PublicInfo(user_id=newUser, first_name="Tom", last_name="Teacher")
        newUser2.save()
        newUser3 = PrivateInfo(user_id=newUser)
        newUser3.save()

        # TA User
        newta = User(email="ta@uwm.edu", password="ta", account_type="ta")
        newta.save()
        newta2 = PublicInfo(user_id=newta, first_name="Tina", last_name="TA")
        newta2.save()
        newta3 = PrivateInfo(user_id=newta)
        newta3.save()

    # This test checks to see if the user is navigated back to the homepage from the display course page
    def test_backToHomepage(self):
        session = self.webpage.session
        for user_obj in User.objects.all():
            login_to_session(user_obj, session)
            resp = self.webpage.get(reverse('displayCourse', kwargs={'course_id': self.course_objs[1].pk}))
            self.assertContains(resp,
                                '<a class="btn btn-primary" href="%s">Back to Dashboard</a>' % reverse('dashboard'),
                                html=True)

    # This test checks to see that if the Change Personal info button is pressed it brings the user to the
    # right page
    def test_toEditAccountPage(self):
        session = self.webpage.session
        for user_obj in User.objects.all():
            login_to_session(user_obj, session)
            resp = self.webpage.get(reverse('accounts'))
            self.assertContains(resp,
                                '<a class="container-fluid text-light" href="%s">Change Personal Info</a>'
                                % reverse('editAccount', kwargs={'user_id': session["user"]}), html=True)

    # This test checks that all the courses from the database are displayed in the graph
    def test_displaysAllCourses(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        pass

    # This test checks that a submitted TA is added to the database
    def test_submitTAtoDatabase(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        testcourse = CourseModel.objects.create(course_name="test_course")
        ta_to_add = User.objects.get(email="ta@uwm.edu")
        self.webpage.post(reverse("displayCourse", kwargs={'course_id': testcourse.pk}),
                          {"submitTa": "", "ta_id": ta_to_add.pk, "is_grader": True, "number_of_labs": 1}, follow=True)
        self.assertNotEqual(CourseTa.objects.filter(ta_id=ta_to_add, course_id=testcourse), None)

    # This test checks that a submitted instructor is added to the database
    def test_submitInstructortoDatabase(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        testcourse = CourseModel.objects.create(course_name="test_course")
        instructor_to_add = User.objects.get(email="teacher@uwm.edu")
        self.webpage.post(reverse("displayCourse", kwargs={'course_id': testcourse.pk}),
                          {"submitInstructor": "", "new_user": instructor_to_add.pk}, follow=True)
        self.assertNotEqual(User.objects.filter(account_type="instructor"), None)

    # This test checks that a submitted section  is added to the database
    def test_submitSectiontoDatabase(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        testcourse = CourseModel.objects.create(course_name="test_course")
        section_to_add = Lab.objects.create(lab_name="testlab", course_id=testcourse, ta_id=None)
        self.webpage.post(reverse("displayCourse", kwargs={'course_id': testcourse.pk}),
                          {"submitSection": "", "section_name": section_to_add.pk}, follow=True)
        self.assertNotEqual(Lab.objects.filter(lab_name="testlab"), None)

    def test_duplicateSection(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        testcourse = CourseModel.objects.create(course_name="test_course")
        section_to_add = Lab.objects.create(lab_name="testlab", course_id=testcourse, ta_id=None)
        section_to_add.save()
        resp = self.webpage.post(reverse("displayCourse", kwargs={'course_id': testcourse.pk}),
                                 {"submitSection": "", "section_name": section_to_add.lab_name}, follow=True)
        self.assertContains(resp, "A section with this name already exists")

    # This test checks that the page displays the add ta button
    def test_tabutton(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session["account_type"] = "admin"
        session.save()
        resp = self.webpage.get(reverse('displayCourse', kwargs={'course_id': self.course_objs[1].pk}))
        self.assertContains(resp,
                            '<input type="submit" class="btn btn-primary" name="submitTa" value="Add TA">',
                            html=True)

    # This test checks that the page displays the add section button
    def test_sectionbutton(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session["account_type"] = "admin"
        session.save()
        resp = self.webpage.get(reverse('displayCourse', kwargs={'course_id': self.course_objs[1].pk}))
        self.assertContains(resp,
                            '<input type="submit" class="btn btn-primary" name="submitSection" value="Add Section">',
                            html=True)

    # This test checks that the page displays the add instructor button
    def test_instructorbutton(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session["account_type"] = "admin"
        session.save()
        resp = self.webpage.get(reverse('displayCourse', kwargs={'course_id': self.course_objs[1].pk}))
        self.assertContains(resp,
                            '<input type="submit" class="btn btn-primary btn-sm" name="submitInstructor" value="Submit" formnovalidate>',
                            html=True)
