from typing import Dict

from TAScheduler.models import Lab as LabModel
from classes import account, course


def create_section(name: str, course_object: course.Course):
    if LabModel.objects.filter(lab_name=name).exists():
        return None

    new_section_model = LabModel.objects.create(
        course_id=course_object.course_model,
        lab_name=name
    )
    return Section(new_section_model)


def delete_section(lab_id):
    try:
        lab_object = LabModel.objects.get(id=lab_id)
        lab_object.delete()
        return True
    except LabModel.DoesNotExist:
        return False


def __has_required_fields(data: Dict[str, any]):
    required_fields = {"lab_name"}
    return required_fields.issubset(data.keys())


def section_list(course_id):
    pass


class Section:
    def __init__(self, lab_model: LabModel):
        self.lab_model = lab_model
        self.course_model = self.lab_model.course_id

    def get_course_name(self):
        return self.course_model.course_name

    def get_lab_name(self):
        return self.lab_model.lab_name
