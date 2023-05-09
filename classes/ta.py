from TAScheduler.models import CourseTa as CourseTaModel, User as UserModel, Course as CourseModel, Lab as LabModel
from classes import account, course, section
from classes.account import Account


def account_to_ta(account_id: int):
    user = UserModel.objects.get(id=account_id)
    acc = Account(user)
    ta = Ta(acc)
    return ta


def get_course_tas(course_id: int):
    tas = CourseTaModel.objects.filter(course_id=course_id)
    ta_objects = [account_to_ta(ta_model.ta_id_id) for ta_model in tas]
    return ta_objects


def get_section_ta(section_id: int):
    section_model = LabModel.objects.get(id=section_id)
    ta_id = section_model.ta_id
    if ta_id is None:
        return None
    ta = account_to_ta(ta_id.id)
    return ta


def get_all_tas():
    tas = UserModel.objects.filter(account_type='ta')
    ta_objects = [account_to_ta(ta_model.pk) for ta_model in tas]
    return ta_objects


class Ta(Account):

    def __init__(self, account: Account):
        super().__init__(account.user_model)
        self.account = account

    def get_grader_status(self, course_id: int):
        try:
            course_ta = CourseTaModel.objects.get(ta_id=self.user_model, course_id=course_id)
            return course_ta.is_grader
        except CourseTaModel.DoesNotExist:
            return None

    def set_grader_status(self, course_id: int, is_grader: bool):
        course_ta = CourseTaModel.objects.get(ta_id=self.user_model, course_id=course_id)
        course_ta.is_grader = is_grader
        course_ta.save()

    def get_number_sections(self, course_id: int):
        try:
            course_ta = CourseTaModel.objects.get(ta_id=self.user_model, course_id=course_id)
            return course_ta.number_of_labs
        except CourseTaModel.DoesNotExist:
            return None

    def set_number_sections(self, course_id: int, number_sections: int):
        course_ta = CourseTaModel.objects.get(ta_id=self.user_model, course_id=course_id)
        course_ta.number_of_labs = number_sections
        course_ta.save()

    def get_courses(self):
        try:
            course_ta_objects = CourseTaModel.objects.filter(ta_id=self.user_model)
            course_ids = course_ta_objects.values_list('course_id', flat=True)
            course_models = CourseModel.objects.filter(id__in=course_ids)
            return [course.Course(course_model) for course_model in course_models]
        except CourseTaModel.DoesNotExist:
            return None

    def add_to_course(self, course_id: int):
        course = CourseModel.objects.get(id=course_id)
        if CourseTaModel.objects.filter(course_id=course, ta_id=self.user_model).exists():
            return None
        new_course_ta = CourseTaModel.objects.create(
            course_id=course,
            ta_id=self.user_model,
        )
        return CourseTaModel(new_course_ta)

    def remove_from_course(self, course_id: int):
        try:
            course_ta = CourseTaModel.objects.get(course_id=course_id, ta_id=self.user_model)
            course_ta.delete()
            return True
        except CourseTaModel.DoesNotExist:
            return False

    def get_sections(self):
        sections = LabModel.objects.filter(ta_id=self.user_model)
        section_objects = [section.Section(lab_model) for lab_model in sections]
        return section_objects

    def add_to_section(self, section_id: int):
        try:
            section = LabModel.objects.get(id=section_id)
            ta = UserModel.objects.get(id=self.get_primary_key())
            section.ta_id = ta
            section.save()
            return True
        except LabModel.DoesNotExist:
            return False

    def remove_from_section(self, section_id: int):
        try:
            section = LabModel.objects.get(id=section_id)
            ta = UserModel.objects.get(id=self.get_primary_key())
            if section.ta_id == ta:
                section.ta_id = None
                section.save()
                return True
            else:
                return False
        except LabModel.DoesNotExist:
            return False
