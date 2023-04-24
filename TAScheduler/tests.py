import unittest
from django.test import TestCase, Client
from django.urls import reverse

from TAScheduler.models import User, PublicInfo, PrivateInfo
from django import urls

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

    def test_toCreateAccountPage(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.get(reverse('accounts'))
        self.assertContains(resp, '<a class="btn btn-primary" href="%s">Create Accounts</a>' % reverse('createAccount'),
                            html=True)

    def test_toEditAccountPage(self):
        #HASN"T BEEN IMPLEMENTED YET
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.get(reverse('accounts'))
        self.assertContains(resp, '<a class="btn btn-primary" href="%s">Edit Accounts</a>' % reverse('editAccount'),
                            html=True)

    def test_toHomepage(self):
        #HASN"T BEEN IMPLEMENTED YET
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

    def test_checkFirstNameSuccessfully(self):
        resp = self.webpage.post("/createAccount/", {"first_name": "Anna", "last_name": "Fronk", "email":
            "avfronk@uwm.edu", "password": "annafronk", "account_type": "administrator"}, follow=True)
        self.assertRedirects(resp, "/dashboard/")

    def test_checkFirsNameFail(self):
        pass

    def test_checkLastNameSuccessfully(self):
        resp = self.webpage.post("/createAccount/", {"first_name": "Anna", "last_name": "Fronk", "email":
            "avfronk@uwm.edu", "password": "annafronk", "account_type": "administrator"}, follow=True)
        self.assertRedirects(resp, "/dashboard/")

    def test_checkLastNameFail(self):
        pass

    def test_checkEmailSuccessfully(self):
        resp = self.webpage.post("/createAccount/", {"first_name": "Anna", "last_name": "Fronk", "email":
            "avfronk@uwm.edu", "password": "annafronk", "account_type": "administrator"}, follow=True)
        self.assertRedirects(resp, "/dashboard/")

    def test_checkEmailFail(self):
        pass

    def test_checkPasswordSuccessfully(self):
        resp = self.webpage.post("/createAccount/", {"first_name": "Anna", "last_name": "Fronk", "email":
            "avfronk@uwm.edu", "password": "annafronk", "account_type": "administrator"}, follow=True)
        self.assertRedirects(resp, "/dashboard/")

    def test_checkPasswordFail(self):
        pass

    def test_checkAccountTypeSuccessfully(self):
        resp = self.webpage.post("/createAccount/", {"first_name": "Anna", "last_name": "Fronk", "email":
            "avfronk@uwm.edu", "password": "annafronk", "account_type": "administrator"}, follow=True)
        self.assertRedirects(resp, "/dashboard/")

    def test_checkAccountTypeFail(self):
        pass
