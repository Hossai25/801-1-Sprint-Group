from typing import Dict

import account
import course
from TAScheduler.models import Lab as LabModel

"""
getCourse
setCourse
getLabName
setLabName
getTA
setTA
courseID
"""


def create_section(data: Dict[str, any]):
    if _has_required_fields(data):
        new_course = LabModel.objects.create(
            course_id=data.get('course_id'),
            ta_id=data.get('ta_id'),
            lab_name=data.get('lab_name')
        )
        return new_course
    else:
        return None


def delete_section(lab_id: int):
    try:
        lab = LabModel.objects.get(id=lab_id)
        lab.delete()
        return True
    except LabModel.DoesNotExist:
        return False


def _has_required_fields(data: Dict[str, any]):
    required_fields = {"course_name"}
    return required_fields.issubset(data.keys())


class Section:
    def __init__(self, lab_model: type[LabModel]):
        self.lab_model = lab_model

    def get_ta(self):
        ta_id = self.course_model.instructor_id
        ta = account.get_account_by_id(ta_id)
        return ta

    def set_ta(self, ta: type[account.Account]):
        self.course_model.instructor_id = ta.get_primary_key()
        self.course_model.save()
