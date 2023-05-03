import unittest
from django.test import TestCase
from TAScheduler.models import Lab, Course as CourseModel
from classes.section import Section, create_section, delete_section
from classes.course import Course


class MyTestCase(TestCase):
    def test_createSectionSuccesful(self):
        course1 = CourseModel.objects.create(course_name="course1")
        self.assertIsInstance(create_section("testsection", course1), Section)

    def test_createDuplicateSection(self):
        testCourse = CourseModel.objects.create(course_name="testCourse")
        section1 = create_section("testsection", testCourse)
        section2 = create_section("testsection", testCourse)
        self.assertEqual(section2, None)

    def test_illegalSection(self):
        testCourse = CourseModel.objects.create(course_name="testCourse")
        testsection = create_section("", testCourse)
        self.assertEqual(testsection, None)

class TestDeleteSection(TestCase):

    def test_modelRemovedOnSuccess(self):
        course_model = CourseModel.objects.create(course_name="test_course")
        section_model = Lab.objects.create(lab_name="test_section", course_id=course_model)
        delete_section(section_model.pk)
        with self.assertRaises(Lab.DoesNotExist):
            Lab.objects.get(lab_name="test_section")

    def test_trueOnSuccess(self):
        course_model = CourseModel.objects.create(course_name="test_course")
        section_model = Lab.objects.create(lab_name="test_section", course_id=course_model)
        self.assertTrue(delete_section(section_model.pk))

    def test_falseOnFailure(self):
        course_model = CourseModel.objects.create(course_name="test_course")
        section_model = Lab.objects.create(lab_name="test_section", course_id=course_model)
        primary_key = section_model.pk
        section_model.delete()
        self.assertFalse(delete_section(primary_key))


if __name__ == '__main__':
    unittest.main()
