import account
import section
from TAScheduler.models import Course as CourseModel, Lab as LabModel
from typing import Dict


def create_course(data: Dict[str, any], null=None):
    if _has_required_fields(data):
        new_course = CourseModel.objects.create(
            course_name=data.get('course_name'),
            instructor_id=null
        )
        course_id = new_course
        return new_course
    else:
        return None


def delete_course(course_id: int):
    try:
        course = CourseModel.objects.get(id=course_id)
        course.delete()
        return True
    except CourseModel.DoesNotExist:
        return False


def _has_required_fields(data: Dict[str, any]):
    required_fields = {"course_name"}
    return required_fields.issubset(data.keys())


class Course:
    def __init__(self, course_model: type[CourseModel]):
        self.course_model = course_model

    def get_course_name(self):
        return self.course_model.course_name

    def set_course_name(self, new_course_name: str):
        self.course_model.course_name = new_course_name
        self.course_model.save()

    def get_instructor(self):
        instructor_id = self.course_model.instructor_id
        instructor = account.get_account_by_id(instructor_id)
        return instructor

    def set_instructor(self, instructor: type[account.Account]):
        self.course_model.instructor_id = instructor.get_primary_key()
        self.course_model.save()

    def get_sections(self):
        section_models = LabModel.objects.filter(course_id=self.course_model.pk)
        return [section.Section(section_model) for section_model in section_models]
