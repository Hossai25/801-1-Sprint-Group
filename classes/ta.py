from TAScheduler.models import CourseTa as CourseTaModel
from account import Account


def account_to_ta(account_id: int):
    pass


def get_course_tas(course_id: int):
    pass


def get_section_ta(section_id: int):
    pass


class Ta(Account):
    def get_grader_status(self, course_id: int):
        pass

    def set_grader_status(self, course_id: int, is_grader: bool):
        pass

    def get_number_sections(self, course_id: int):
        pass

    def set_number_sections(self, course_id: int, number_sections: int):
        pass

    def get_courses(self):
        pass

    def add_to_course(self, course_id: int):
        pass

    def remove_from_course(self, course_id: int):
        pass

    def get_sections(self):
        pass

    def add_to_section(self, section_id: int):
        pass

    def remove_from_section(self, section_id: int):
        pass
