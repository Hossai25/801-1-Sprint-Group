from django.db import models


class User(models.Model):
    email = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    account_type = models.CharField(max_length=25)


class Course(models.Model):
    pass


class Lab(models.Model):
    pass


class PublicInformation(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    office_hours = models.CharField(max_length=25)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)


class PrivateInformation(models.Model):
    address = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=25)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)


class CourseTA(models.Model):
    pass
