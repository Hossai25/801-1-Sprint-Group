from typing import Dict

from django.shortcuts import render

from TAScheduler.models import Lab as LabModel, Course as CourseModel
from classes import account, course


def create_section(name: str, course_instance: course.Course):

    new_lab = LabModel.objects.create(
        course_id=data.get('course_id'),
        lab_name=data.get('lab_name')
    )
    return new_course


def _has_required_fields(data: Dict[str, any]):
    required_fields = {"course_name", "lab_name"}
    return required_fields.issubset(data.keys())


class Section:
    def __init__(self, lab_model: LabModel):
        self.lab_model = lab_model
        self.course_model = course.get_course_by_id(self.lab_model.course_id)

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
