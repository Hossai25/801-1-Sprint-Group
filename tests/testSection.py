import unittest
from django.test import TestCase
from TAScheduler.models import Lab as LabModel, Course as CourseModel
from django.core.exceptions import ObjectDoesNotExist
from classes import section
from classes.section import Section, create_section, delete_section
from classes.course import create_course


class TestSectionStaticMethods(TestCase):
    def test_createSectionSuccessful(self):
        course1 = create_course("course1")
        self.assertIsInstance(create_section("testSection", course1), Section)

    def test_createDuplicateSection(self):
        test_course = create_course("testCourse")
        create_section("testSection", test_course)
        section2 = create_section("testSection", test_course)
        self.assertEqual(section2, None)

    def test_getSectionById(self):
        course_model = CourseModel.objects.create(course_name="test_course")
        section_model = LabModel.objects.create(lab_name="new name", course_id=course_model)
        section_model_id = section_model.pk
        section_class = section.Section(section_model)
        self.assertEqual(section_class.get_lab_name(), section.get_section_by_id(section_model_id).get_lab_name())

    def test_getUndeclaredSectionByID(self):
        self.assertEqual(None, section.get_section_by_id(123))

    def test_getFullCourseList(self):
        course1 = CourseModel.objects.create(course_name="course1")
        LabModel.objects.create(lab_name="sect1", course_id=course1)
        LabModel.objects.create(lab_name="sect2", course_id=course1)
        self.assertEquals(section.section_list(course1).__len__(), 2)

    def test_getEmptyCourseList(self):
        course1 = CourseModel.objects.create(course_name="course1")
        empty_list = section.section_list(course1)
        self.assertEqual(empty_list, [])


class TestDeleteSection(TestCase):

    def test_modelRemovedOnSuccess(self):
        course_model = CourseModel.objects.create(course_name="test_course")
        section_model = LabModel.objects.create(lab_name="test_section", course_id=course_model)
        delete_section(section_model.pk)
        with self.assertRaises(ObjectDoesNotExist):
            LabModel.objects.get(lab_name="test_section")

    def test_trueOnSuccess(self):
        course_model = CourseModel.objects.create(course_name="test_course")
        section_model = LabModel.objects.create(lab_name="test_section", course_id=course_model)
        self.assertTrue(delete_section(section_model.pk))

    def test_falseOnFailure(self):
        course_model = CourseModel.objects.create(course_name="test_course")
        section_model = LabModel.objects.create(lab_name="test_section", course_id=course_model)
        primary_key = section_model.pk
        section_model.delete()
        self.assertFalse(delete_section(primary_key))


if __name__ == '__main__':
    unittest.main()
