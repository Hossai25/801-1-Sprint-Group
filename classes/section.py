from TAScheduler.models import Lab as LabModel
from classes import account, course


def create_section(name: str, course_object: course.Course):
    new_section_model = LabModel.objects.create(
        course_id=course_object.get_primary_key(),
        lab_name=name
    )
    return Section(new_section_model)


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
