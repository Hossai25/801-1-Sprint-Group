from classes import account
from classes.account import Account
from TAScheduler.models import User as UserModel, Course as CourseModel


def account_to_instructor(account_id: int):
    user = UserModel.objects.get(id=account_id)
    acc = Account(user)
    instructor = Instructor(acc)
    return instructor


def get_course_instructor(course_id: int):
    course = CourseModel.objects.get(id=course_id)
    instructor = account_to_instructor(course.instructor_id.pk)
    return instructor


def get_all_instructors():
    instructors = UserModel.objects.filter(account_type='instructor')
    instructor_objects = [account_to_instructor(instructor_model.pk) for instructor_model in instructors]
    return instructor_objects


class Instructor(Account):

    def __init__(self, account: Account):
        super().__init__(account.user_model)
        self.account = account

    def get_courses(self):
        pass

    def add_to_course(self, course_id: int):
        try:
            course = CourseModel.objects.get(id=course_id)
            # if course.instructor_id.id == self.get_primary_key():
            #     return None
            instructor = UserModel.objects.get(id=self.get_primary_key())
            course.instructor_id = instructor
            course.save()
            return True
        except CourseModel.DoesNotExist:
            return False

    def remove_from_course(self, course_id: int):
        pass
