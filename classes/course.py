import account
import section
from TAScheduler.models import Course as CourseModel, Lab as LabModel


class Course:
    def __int__(self, course_model: type[CourseModel]):
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
