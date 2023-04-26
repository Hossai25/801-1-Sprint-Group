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
        course_model = CourseModel.objects.create(course_name="test")
        self.assertEqual(course_model, course.get_course_model("test"))

    def test_getUnmadeCourseModel(self):
        self.assertEqual(course.get_course_model("test"), None)

    def test_getCourseSuccessfully(self):
        course_object = course.create_course("test")
        self.assertEqual(course_object.get_course_name(), course.get_course("test").get_course_name())

    def test_getUnmadeCourse(self):
        self.assertEqual(None, course.get_course("test"))

    def test_getCourseByIDSuccessfully(self):
        course_model = CourseModel.objects.create(course_name="new name")
        course_model_id = course_model.pk
        course_class = course.Course(course_model)
        self.assertEqual(course_class.get_course_name(), course.get_course_by_id(course_model_id).get_course_name())

    def test_getUndeclaredClassByID(self):
        self.assertEqual(None, course.get_course_by_id(123))

    def test_getEmptyCourseList(self):
        emptyList = course.course_list()
        self.assertEqual(emptyList, [])


if __name__ == '__main__':
    unittest.main()
