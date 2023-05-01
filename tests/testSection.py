import unittest
from django.test import TestCase
from TAScheduler.models import Lab, Course as CourseModel
from classes.section import Section, create_section, delete_section
from classes.course import Course


class MyTestCase(unittest.TestCase):
    # def test_something(self):
    # self.assertEqual(True, False)  # add assertion here

    def test_createSectionSuccesful(self):
        self.assertEqual(create_section("testsection"), Lab(lab_name="testsection"))


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
