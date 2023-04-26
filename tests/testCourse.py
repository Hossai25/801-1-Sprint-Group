import unittest
from django.test import TestCase

from TAScheduler.models import Course as CourseModel
from classes import course


class TestCourseMethods(TestCase):
    def test_createcourse(self):
        course_object = course.create_course("new name")
        self.assertIsInstance(course_object, course.Course)

    def test_createduplicatecourse(self):
        course_object1 = course.create_course("new name")
        course_object2 = course.create_course("new name")
        self.assertEqual(course_object2, None)

    def test_getCourseModelSuccessfully(self):
        pass

    def test_getUnmadeCourseModel(self):
        pass

    def test_getCourseSuccessfully(self):
        pass

    def test_getUnmadeCourse(self):
        pass

    def test_getCourseIDSuccessfully(self):
        pass

    def test_getUndeclaredClassID(self):
        pass

    def test_getEmptyCourseList(self):
        pass


if __name__ == '__main__':
    unittest.main()
