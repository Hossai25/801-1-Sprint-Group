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

    def test_correctName(self):
        for i in self.users:
            resp = self.webpage.post("/", {"username": i+"@uwm.edu", "password": i},
                                     follow=True)
            self.assertEqual(resp.context["email"], i+"@uwm.edu", "username not passed from login")


    def test_successfulLogin(self):
        resp = self.webpage.post("/", {"username": "test1@uwm.edu", "password": "test1"},
                                 follow=True)
        self.assertRedirects(resp, "/dashboard/")

    def test_noPassword(self):
        resp = self.webpage.post("/", {"username": "test1@uwm.edu", "password": ""},
                                 follow=True)
        self.assertContains(resp, "Invalid username or password.")

    def test_wrongPassword(self):
        resp = self.webpage.post("/", {"username": "test1@uwm.edu", "password": "password"}, follow=True)
        self.assertContains(resp, "Invalid username or password.")

    def test_forgotPassword(self):
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
    def test_accountsClicked(self):
        session = self.webpage.session
        session["email"] = "test1@uwm.edu"
        session.save()
        resp = self.webpage.get(reverse('dashboard'))
        self.assertContains(resp, '<a class="btn btn-primary" href="%s">Create Accounts</a>' % reverse('createAccount'), html=True)

    def test_coursesClicked(self):
        pass

    def test_accessDataClicked(self):
        pass

    def test_notificationsClicked(self):
        pass

class Accounts(TestCase):
    webpage = None
    users = None

    def setUp(self):
        self.webpage = Client()
        self.users = ["test1", "test2"]

        for i in self.users:
            temp = User(email=i + "@uwm.edu", password=i, account_type="administrator")
            temp.save()

    def test_toCreateAccountPage(self):
        pass

    def test_toEditAccountPage(self):
        pass

    def test_toHomepage(self):
        pass


class CreateAccounts(TestCase):
    webpage = None
    users = None

    def setUp(self):
        self.webpage = Client()
        self.users = ["test1", "test2"]

        for i in self.users:
            temp = User(email=i + "@uwm.edu", password=i, account_type="administrator")
            temp.save()