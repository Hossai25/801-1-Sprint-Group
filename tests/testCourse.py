import unittest
from django.test import TestCase

from TAScheduler.models import Course as CourseModel, Lab as LabModel
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

    def test_getFullCourseList(self):
        course1 = CourseModel.objects.create(course_name="course1")
        course2 = CourseModel.objects.create(course_name="course2")
        self.assertEquals(course.course_list().__len__(), 2)

    def test_getEmptyCourseList(self):
        empty_list = course.course_list()
        self.assertEqual(empty_list, [])


class TestDeleteCourse(TestCase):

    def test_courseModelRemoved(self):
        course_model = CourseModel.objects.create(course_name="test_course")
        course.delete_course(course_model.pk)
        with self.assertRaises(CourseModel.DoesNotExist):
            CourseModel.objects.get(course_name="test_course")

    def test_sectionModelsRemoved(self):
        course_model = CourseModel.objects.create(course_name="test_course")
        LabModel.objects.create(lab_name="test_section", course_id=course_model)
        course.delete_course(course_model.pk)
        with self.assertRaises(LabModel.DoesNotExist):
            LabModel.objects.get(lab_name="test_section")

    def test_trueOnSuccess(self):
        course_model = CourseModel.objects.create(course_name="test_course")
        self.assertTrue(course.delete_course(course_model.pk))

    def test_falseOnFailure(self):
        course_model = CourseModel.objects.create(course_name="test_course")
        primary_key = course_model.pk
        course_model.delete()
        self.assertFalse(course.delete_course(primary_key))


if __name__ == '__main__':
    unittest.main()
