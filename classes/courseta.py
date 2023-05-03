from TAScheduler.models import User as UserModel, CourseTa as TAModel
from typing import Dict
from classes import account, course


def create_courseta(course_object: course.Course, user_id: int, grader: bool, labs: int, ):
    user = UserModel.objects.get(id=user_id)
    if TAModel.objects.filter(ta_id=user_id).exists():
        return None
    new_course_ta = TAModel.objects.create(
        course_id=course_object.course_model,
        ta_id=user,
        is_grader=grader,
        number_of_labs=labs
    )

    return CourseTa(new_course_ta)


def delete_courseta(courseta_id):
    try:
        courseta_object = TAModel.objects.get(id=courseta_id)
        courseta_object.delete()
        return True
    except TAModel.DoesNotExist:
        return False


def course_ta_list(course_id):
    talist = TAModel.objects.filter(course_id=course_id)
    return talist


class CourseTa:
    def __init__(self, ta_model: TAModel):
        self.ta_model = ta_model
        self.course_model = self.ta_model.course_id
        self.user_model = self.ta_model.ta_id

    def get_course_name(self):
        return self.course_model.course_name

    def get_email(self):
        return self.user_model.email

    def get_is_grader(self):
        return self.ta_model.is_grader

    def get_number_of_labs(self):
        return self.ta_model.number_of_labs

    def get_ta(self):
        ta_id = self.course_model.instructor_id
        ta = account.get_account_by_id(ta_id)
        return ta

    def set_ta(self, ta: account.Account):
        self.course_model.instructor_id = ta.get_primary_key()
        self.course_model.save()
