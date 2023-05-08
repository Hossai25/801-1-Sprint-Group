from account import Account


def account_to_instructor(account_id: int):
    pass


def get_course_instructor(course_id: int):
    pass


class Instructor(Account):
    def get_courses(self):
        pass

    def add_to_course(self, course_id: int):
        pass

    def remove_from_course(self, course_id: int):
        pass
