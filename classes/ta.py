from TAScheduler.models import CourseTa as CourseTaModel, User as UserModel, Course as CourseModel, Lab as LabModel
from classes import course
from classes.account import Account
from classes.section import Section


def account_to_ta(account_id: int):
    try:
        user = UserModel.objects.get(id=account_id)
        if user.account_type != "ta":
            return None
        acc = Account(user)
        ta = Ta(acc)
        return ta
    except UserModel.DoesNotExist:
        return None


def get_course_tas(course_id: int):
    try:
        CourseModel.objects.get(id=course_id)
    except CourseModel.DoesNotExist:
        return None
    tas = CourseTaModel.objects.filter(course_id=course_id)
    ta_objects = [account_to_ta(ta_model.ta_id_id) for ta_model in tas]
    return ta_objects


def get_section_ta(section_id: int):
    try:
        section_model = LabModel.objects.get(id=section_id)
        if section_model.ta_id is None:
            return None
        ta_id = section_model.ta_id.pk
        ta = account_to_ta(ta_id)
        return ta
    except LabModel.DoesNotExist:
        return None


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
        try:
            course_ta = CourseTaModel.objects.get(ta_id=self.user_model, course_id=course_id)
            course_ta.is_grader = is_grader
            course_ta.save()
            return True
        except CourseTaModel.DoesNotExist:
            return False

    def get_number_sections(self, course_id: int):
        try:
            course_ta = CourseTaModel.objects.get(ta_id=self.user_model, course_id=course_id)
            return course_ta.number_of_labs
        except CourseTaModel.DoesNotExist:
            return None

    def set_number_sections(self, course_id: int, number_sections: int):
        try:
            course_ta = CourseTaModel.objects.get(ta_id=self.user_model, course_id=course_id)
            course_ta.number_of_labs = number_sections
            course_ta.save()
            return True
        except CourseTaModel.DoesNotExist:
            return False

    def get_courses(self):
        try:
            course_ta_objects = CourseTaModel.objects.filter(ta_id=self.user_model)
            course_ids = course_ta_objects.values_list('course_id', flat=True)
            course_models = CourseModel.objects.filter(id__in=course_ids)
            return [course.Course(course_model) for course_model in course_models]
        except CourseTaModel.DoesNotExist:
            return None

    def add_to_course(self, course_id: int):
        try:
            CourseTaModel.objects.get(ta_id=self.user_model, course_id=course_id)
            return False
        except CourseTaModel.DoesNotExist:
            try:
                course_model = CourseModel.objects.get(id=course_id)
                CourseTaModel.objects.create(ta_id=self.user_model, course_id=course_model)
                return True
            except CourseModel.DoesNotExist:
                return False

    def remove_from_course(self, course_id: int):
        try:
            course_ta = CourseTaModel.objects.get(course_id=course_id, ta_id=self.user_model)
            sections = LabModel.objects.filter(course_id=course_id, ta_id=self.user_model)
            ta = UserModel.objects.get(id=self.get_primary_key())
            course_ta.delete()
            for sect in sections:
                if sect.ta_id == ta:
                    sect.ta_id = None
                    sect.save()
            return True
        except CourseTaModel.DoesNotExist:
            return False

    def get_sections(self):
        try:
            section_models = LabModel.objects.filter(ta_id=self.user_model)
            return [Section(section_model) for section_model in section_models]
        except LabModel.DoesNotExist:
            return None

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
            section_model = LabModel.objects.get(id=section_id)
            ta = UserModel.objects.get(id=self.get_primary_key())
            if section_model.ta_id == ta:
                section_model.ta_id = None
                section_model.save()
                return True
            else:
                return False
        except LabModel.DoesNotExist:
            return False
