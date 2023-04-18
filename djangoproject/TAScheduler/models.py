from django.db import models


class User(models.Model):
    email = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    account_type = models.CharField(max_length=25)


class PublicInfo(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    office_hours = models.CharField(max_length=25)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)


class PrivateInfo(models.Model):
    address = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=25)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)


class Course(models.Model):
    course_name = models.CharField(max_length=25)
    instructor_id = models.ForeignKey(User, on_delete=models.SET_NULL)


class Lab(models.Model):
    lab_name = models.CharField(max_length=25)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    ta_id = models.ForeignKey(User, on_delete=models.SET_NULL)


class CourseTa(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    ta_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_grader = models.BooleanField(null=True)
    number_of_labs = models.IntegerField(null=True)
