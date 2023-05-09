import unittest
from django.test import TestCase, Client
from django.urls import reverse
from TAScheduler.models import Course as CourseModel

from TAScheduler.models import User, PublicInfo, PrivateInfo, Course, Lab
from django import urls

from classes.section import create_section


class Login(TestCase):
    webpage = None
    users = None

    def setUp(self):
        self.webpage = Client()
        self.users = ["test1", "test2"]

        #Fill test database with users
        for i in self.users:
            temp = User(email=i+"@uwm.edu", password=i, account_type="administrator")
            temp.save()
            temp2 = PublicInfo(user_id=temp, first_name=i, last_name=i)
            temp2.save()
            temp3 = PrivateInfo(user_id=temp)
            temp3.save()


    #This test checks to see if the username and password are passed from login into the database
    def test_correctName(self):
        for i in self.users:
            resp = self.webpage.post("/", {"username": i+"@uwm.edu", "password": i},
                                     follow=True)
            self.assertEqual(resp.context["email"], i+"@uwm.edu", "username not passed from login")


    #This test checks to see if upon a successful login the user is brought to the dashboard/homepage
    def test_successfulLogin(self):
        resp = self.webpage.post("/", {"username": "test1@uwm.edu", "password": "test1"},
                                 follow=True)
        self.assertRedirects(resp, "/dashboard/")

    #This test checks to see that if no password is used an error message appears
    def test_noPassword(self):
        resp = self.webpage.post("/", {"username": "test1@uwm.edu", "password": ""},
                                 follow=True)
        self.assertContains(resp, "Invalid username or password.")

    #This test checks to see if the wrong password is used an error message appears
    def test_wrongPassword(self):
        resp = self.webpage.post("/", {"username": "test1@uwm.edu", "password": "password"}, follow=True)
        self.assertContains(resp, "Invalid username or password.")

    #This test checks to see if the forgot password redirects to the right page
    def test_forgotPassword(self):
        #HASN'T BEEN IMPLEMENTED YET
        pass

class Dashboard(TestCase):
    webpage = None
    users = None

    def setUp(self):
        self.webpage = Client()
        self.users = ["test1", "test2"]

        for i in self.users:
            temp = User(email=i + "@uwm.edu", password=i, account_type="administrator")
            temp.save()
            temp2 = PublicInfo(user_id=temp, first_name=i, last_name=i)
            temp2.save()
            temp3 = PrivateInfo(user_id=temp)
            temp3.save()

    #This test checks to see if the user is redirected to the accounts page when the button is pressed
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
        self.assertContains(resp, '<a class="btn btn-primary" href="%s">Courses/Labs</a>' % reverse('courses'), html=True)

    # This test checks to see if the user is redirected to the access data page when the button is pressed
    def test_accessDataClicked(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.get(reverse('dashboard'))
        self.assertContains(resp, '<a class="btn btn-primary" href="%s">Access Data</a>' % reverse('database'),
                            html=True)

    # This test checks to see if the user is redirected to the notifications page when the button is pressed
    def test_notificationsClicked(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.get(reverse('dashboard'))
        self.assertContains(resp, '<a class="btn btn-primary" href="%s">Notifications</a>' % reverse('notifications'),
                            html=True)

class Accounts(TestCase):
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

    #This test checks to see that if the create account button is pressed it brings the user to the
    # right page
    def test_toCreateAccountPage(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.get(reverse('accounts'))
        self.assertContains(resp, '<a class="btn btn-primary" href="%s">Create Accounts</a>' % reverse('createAccount'),
                            html=True)

    # This test checks to see that if the edit account button is pressed it brings the user to the
    # right page
    def test_toEditAccountPage(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.get(reverse('accounts'))
        self.assertContains(resp, '<a class="btn btn-primary" href="%s">Edit Accounts</a>' % reverse('editAccount'),
                            html=True)

    # This test checks to see that if the back to dashboard button is pressed it brings the user to
    # the right page
    def test_toHomepage(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.get(reverse('accounts'))
        self.assertContains(resp, '<a class="btn btn-primary" href="%s">Back to Dashboard</a>' % reverse('dashboard'),
                            html=True)


class CreateAccounts(TestCase):
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

    #This test checks to see that when the information is entered correctly user is brought back
    # to dashboard
    def test_checkSuccessfully(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.post(reverse("createAccount"), {"first_name": "Anna", "last_name": "Fronk", "email":
            "avfronk@uwm.edu", "password": "annafronk", "account_type": "administrator"}, follow=True)
        self.assertRedirects(resp, "/accounts/")

    #This test checks if the first name has an invalid input then an error message appears
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
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.get(reverse('createAccount'))
        self.assertContains(resp, '<a class="btn btn-primary" href="%s">Back to Dashboard</a>' % reverse('dashboard'),
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
        session.save()
        resp = self.webpage.get(reverse('courses'))
        self.assertContains(resp, '<a class="btn btn-primary" href="%s">Create Courses</a>' % reverse('createCourse'),
                            html=True)

    # This test checks to see that if the create lab button is pressed it brings the user to the
    # right page
    def test_toCreateLabPage(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.get(reverse('courses'))
        self.assertContains(resp, '<a class="btn btn-primary" href="%s">Create Courses</a>' % reverse('createCourse'),
                            html=True)

    # This test checks to see that if the back to dashboard button is pressed it brings the user to the
    # right page
    def test_toHomepage(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.get(reverse('courses'))
        self.assertContains(resp, '<a class="btn btn-primary" href="%s">Back to Dashboard</a>' % reverse('dashboard'),
                            html=True)

class CreateCourse(TestCase):
    webpage = None
    users = None
    courses = None

    def setUp(self):
        self.webpage = Client()
        self.users = ["test1"]
        self.courses = ["Course1", "Course2"]

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

    #This test checks to see after a course is created the user is redirected to the dashboard
    def test_successfulCourseCreation(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.post(reverse("createCourse"), {"course_name": "Course3"}, follow=True)
        self.assertRedirects(resp, "/courses/")

    #This test checks to see if an error appears if a duplicate course is created
    def test_duplicateCourse(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.post(reverse("createCourse"), {"course_name": "Course1"}, follow=True)
        self.assertContains(resp, "Error creating the course.")

    #This test checks to see if an error appears if a blank field is entered
    def test_blankFields(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.post(reverse("createCourse"), {"course_name": ""}, follow=True)
        self.assertContains(resp, "Error creating the course.")

    #This test checks to see if the course is successfully added to the database when it is submitted
    def test_courseAddedToDatabase(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.post(reverse("createCourse"), {"course_name": "Course3"}, follow=True)
        self.assertNotEqual(Course.objects.get(course_name="Course3"), None)

class CreateSection(TestCase):
    webpage = None
    users = None
    courses = None

    def setUp(self):
        self.webpage = Client()
        self.users = ["test1"]
        self.courses = ["Course1", "Course2"]

        # Fill test database with users
        for i in self.users:
            #Instructor
            temp = User(email=i + "@uwm.edu", password=i, account_type="instructor")
            temp.save()
            temp2 = PublicInfo(user_id=temp, first_name=i, last_name=i)
            temp2.save()
            temp3 = PrivateInfo(user_id=temp)
            temp3.save()

            #TA
            tatemp= User(email=i + "ta@uwm.edu", password=i, account_type="ta")
            tatemp.save()
            tatemp2 = PublicInfo(user_id=tatemp, first_name=i, last_name=i)
            tatemp2.save()
            tatemp3 = PrivateInfo(user_id=tatemp)
            tatemp3.save()
            for j in self.courses:
                tempCourse = Course(course_name=j, instructor_id=temp).save()
                Lab(lab_name=j+" Section", course_id=tempCourse, ta_id=tatemp)

    def test_successfulSectionCreation(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        temp = User(email="instructor@uwm.edu", password="instructor", account_type="instructor")
        temp.save()
        temp2 = PublicInfo(user_id=temp, first_name="first", last_name="last")
        temp2.save()
        temp3 = PrivateInfo(user_id=temp)
        temp3.save()
        testcourse = CourseModel.objects.create(course_name="test_course")
        resp = self.webpage.post(reverse("createLab"), {"course_id": testcourse.id, "course_object": testcourse, "lab_name": "New Section"}, follow=True)
        self.assertRedirects(resp, "/courses/")

    def test_duplicateSection(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        temp = User(email="ta@uwm.edu", password="ta", account_type="ta")
        temp.save()
        temp2 = PublicInfo(user_id=temp, first_name="first", last_name="last")
        temp2.save()
        temp3 = PrivateInfo(user_id=temp)
        temp3.save()
        testcourse = CourseModel.objects.create(course_name="test_course")
        testlab = Lab.objects.create(lab_name= "testsection", course_id= testcourse , ta_id= temp)
        resp = self.webpage.post(reverse('createLab'), {"course_id": testcourse.id, "course_object": testcourse, "lab_name": "testsection"}, follow=True)
        self.assertContains(resp, "Section name blank or already exists.")

    def test_blankSectionFields(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        temp = User(email="ta@uwm.edu", password="ta", account_type="ta")
        temp.save()
        temp2 = PublicInfo(user_id=temp, first_name="first", last_name="last")
        temp2.save()
        temp3 = PrivateInfo(user_id=temp)
        temp3.save()
        testcourse = CourseModel.objects.create(course_name="test_course")
        resp = self.webpage.post(reverse('createLab'), {"course_id": testcourse.id, "course_object": testcourse, "lab_name": ""}, follow=True)
        self.assertContains(resp, "Section name blank or already exists.")

    def test_noCourseForSection(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.post(reverse("createLab"), {"course_id": 000, "course_object": "", "lab_name": "New Section"}, follow=True)
        self.assertContains(resp, "Course not found.")

    def test_sectionAddedToDatabase(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        temp = User(email="instructor@uwm.edu", password="instructor", account_type="instructor")
        temp.save()
        temp2 = PublicInfo(user_id=temp, first_name="first", last_name="last")
        temp2.save()
        temp3 = PrivateInfo(user_id=temp)
        temp3.save()
        testcourse = CourseModel.objects.create(course_name="test_course")
        resp = self.webpage.post(reverse("createLab"), {"course_id": testcourse.id, "course_object": testcourse, "lab_name": "New Section"}, follow=True)
        self.assertNotEqual(Lab.objects.get(lab_name="New Section"), None)

class DeleteAccount(TestCase):
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

        #Instructor User
        newUser = User(email="teacher@uwm.edu", password="teacher", account_type="instructor")
        newUser.save()
        newUser2 = PublicInfo(user_id=newUser, first_name="Tom", last_name="Teacher")
        newUser2.save()
        newUser3 = PrivateInfo(user_id=newUser)
        newUser3.save()

        #TA User
        newta = User(email="ta@uwm.edu", password="ta", account_type="ta")
        newta.save()
        newta2 = PublicInfo(user_id=newta, first_name="Tina", last_name="TA")
        newta2.save()
        newta3 = PrivateInfo(user_id=newta)
        newta3.save()

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

    def test_anyclassesconnectedstillexist(self):
        pass

    def test_tacantdeleteaccount(self):
        session = self.webpage.session
        session["email"] = "ta@uwm.edu"
        session.save()
        temp = User(email="delete@uwm.edu", password="delete", account_type="administrator")
        temp.save()
        temp2 = PublicInfo(user_id=temp, first_name="first", last_name="last")
        temp2.save()
        temp3 = PrivateInfo(user_id=temp)
        temp3.save()
        resp = self.webpage.get(reverse('deleteAccount', args=[temp.pk]))
        self.assertEqual(False, self.assertRedirects(resp, "/accounts/"))

    def test_instructorcantdeleteaccount(self):
        session = self.webpage.session
        session["email"] = "teacher@uwm.edu"
        session.save()
        temp = User(email="delete@uwm.edu", password="delete", account_type="administrator")
        temp.save()
        temp2 = PublicInfo(user_id=temp, first_name="first", last_name="last")
        temp2.save()
        temp3 = PrivateInfo(user_id=temp)
        temp3.save()
        resp = self.webpage.get(reverse('deleteAccount', args=[temp.pk]))
        self.assertEqual(False, self.assertRedirects(resp, "/accounts/"))
class DeleteCourse(TestCase):
    webpage = None
    users = None
    courses = None

    def setUp(self):
        self.webpage = Client()
        self.users = ["test1"]
        self.courses = ["Course1", "Course2"]

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
        testcourse = CourseModel.objects.create(course_name="test_course")
        resp = self.webpage.get(reverse('deleteCourse', args=[testcourse.pk]))
        self.assertRedirects(resp, "/courses/")

    def test_instructorstillexists(self):
        pass

    def test_tastillexists(self):
        pass

    def test_tacantdeleteaccount(self):
        session = self.webpage.session
        session["email"] = "ta@uwm.edu"
        session.save()
        temp = User(email="delete@uwm.edu", password="delete", account_type="administrator")
        temp.save()
        temp2 = PublicInfo(user_id=temp, first_name="first", last_name="last")
        temp2.save()
        temp3 = PrivateInfo(user_id=temp)
        temp3.save()
        testcourse = CourseModel.objects.create(course_name="test_course")
        resp = self.webpage.get(reverse('deleteCourse', args=[testcourse.pk]))
        self.assertEqual(False, self.assertRedirects(resp, "/courses/"))

    def test_instructorcantdeleteaccount(self):
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
        self.assertEqual(False, self.assertRedirects(resp, "/courses/"))

