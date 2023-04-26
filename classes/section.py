from typing import Dict
import account
import course
from TAScheduler.models import Lab as LabModel, Course as CourseModel


# def create_section(data: Dict[str, any]):
#     if _has_required_fields(data):
#         new_course = LabModel.objects.create(
#             course_id=data.get('course_id'),
#             ta_id=data.get('ta_id'),
#             lab_name=data.get('lab_name')
#         )
#         return new_course
#     else:
#         return None


def create_lab(data: Dict[str, any]):
    course_id = data.get('course_id')
    lab_name = data.get('lab_name')

    if not lab_name:
        return None

    try:
        course = CourseModel.objects.get(id=course_id)
    except CourseModel.DoesNotExist:
        return None

    new_lab = LabModel.objects.create(
        lab_name=lab_name,
        course_id=course,
        ta_id=data.get('ta_id')
    )

    return new_lab


def _has_required_fields(data: Dict[str, any]):
    required_fields = {"course_name", "lab_name"}
    return required_fields.issubset(data.keys())


class Section:
    def __init__(self, course_model: type[CourseModel], lab_model: type[LabModel]):
        self.course_model = course
        self.lab_model = lab_model

    def get_course_name(self):
        return self.course_model.course_name

    def get_lab_name(self):
        return self.lab_model.lab_name

    def set_lab_name(self, new_lab_name: str):
        self.lab_model.lab_name = new_lab_name
        self.lab_model.save()

    def get_ta(self):
        ta_id = self.course_model.instructor_id
        ta = account.get_account_by_id(ta_id)
        return ta

    def set_ta(self, ta: type[account.Account]):
        self.course_model.instructor_id = ta.get_primary_key()
        self.course_model.save()
