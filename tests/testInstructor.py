from django.test import TestCase

from TAScheduler.models import Course as CourseModel, User as UserModel, PublicInfo, PrivateInfo
from classes import instructor
from classes.account import Account
from classes.instructor import Instructor


class TestStaticMethods(TestCase):

    def setUp(self):
        self.user = UserModel.objects.create(
            email="test@email.com",
            password="password123",
            account_type="instructor"
        )
        PublicInfo.objects.create(
            user_id=self.user,
            first_name="John",
            last_name="Doe"
        )
        PrivateInfo.objects.create(
            user_id=self.user
        )
        self.course_model = CourseModel.objects.create(
            course_name="test_course",
            instructor_id=self.user
        )

    def test_accountToInstructor(self):
        user_id = self.user.id
        instructor_object = instructor.account_to_instructor(user_id)
        self.assertIsInstance(instructor_object, instructor.Instructor)

    def test_wrongAccountToInstructor(self):
        self.user.account_type = "ta"
        self.user.save()
        user_id = self.user.id
        instructor_object = instructor.account_to_instructor(user_id)
        self.assertFalse(instructor_object)

    def test_getCourseInstructor(self):
        returned_instructor = instructor.get_course_instructor(self.course_model.id)
        self.assertEqual(returned_instructor.user_model, self.user)

    def test_noCourseInstructor(self):
        empty_course = CourseModel.objects.create(course_name="empty")
        returned_instructor = instructor.get_course_instructor(empty_course.id)
        self.assertIsNone(returned_instructor)

    def test_getAllInstructors(self):
        instructors = instructor.get_all_instructors()
        for instructor_obj in instructors:
            self.assertEqual(instructor_obj.user_model.account_type, "instructor")

    def test_noInstructors(self):
        self.user.account_type = "ta"
        self.user.save()
        instructors = instructor.get_all_instructors()
        self.assertEqual(instructors, [])


class TestInstructorClassMethods(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create(
            email="test@email.com",
            password="password123",
            account_type="instructor"
        )
        PublicInfo.objects.create(
            user_id=self.user,
            first_name="John",
            last_name="Doe"
        )
        PrivateInfo.objects.create(
            user_id=self.user
        )

    def test_getCourses(self):
        test_instructor = Instructor(Account(self.user))
        filled_course = CourseModel.objects.create(course_name="filled", instructor_id=self.user)
        CourseModel.objects.create(course_name="empty")
        courses_list = test_instructor.get_courses()
        for courses in courses_list:
            self.assertEqual(courses.get_primary_key(), filled_course.id)

    def test_getCoursesEmpty(self):
        test_instructor = Instructor(Account(self.user))
        courses_list = test_instructor.get_courses()
        self.assertEqual(courses_list, [])

    def test_addToCourse(self):
        test_instructor = Instructor(Account(self.user))
        empty_course = CourseModel.objects.create(course_name="empty")
        add = test_instructor.add_to_course(empty_course.id)
        self.assertTrue(add)

    def test_addToCourseDuplicate(self):
        test_instructor = Instructor(Account(self.user))
        fill_course = CourseModel.objects.create(course_name="empty")
        fill_course.instructor_id = self.user
        fill_course.save()
        add = test_instructor.add_to_course(fill_course.id)
        self.assertIsNone(add)

    def test_addToCourseNonexistent(self):
        test_instructor = Instructor(Account(self.user))
        add = test_instructor.add_to_course(123)
        self.assertFalse(add)

    def test_removeFromCourse(self):
        test_instructor = Instructor(Account(self.user))
        filled_course = CourseModel.objects.create(course_name="empty", instructor_id=self.user)
        remove = test_instructor.remove_from_course(filled_course.id)
        self.assertTrue(remove)

    def test_removeFromCourseNoCourse(self):
        test_instructor = Instructor(Account(self.user))
        remove = test_instructor.remove_from_course(123)
        self.assertFalse(remove)

    def test_removeFromCourseNoInstructor(self):
        test_instructor = Instructor(Account(self.user))
        empty_course = CourseModel.objects.create(course_name="empty")
        remove = test_instructor.remove_from_course(empty_course.id)
        self.assertFalse(remove)
