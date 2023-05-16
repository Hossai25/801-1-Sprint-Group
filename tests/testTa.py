from django.test import TestCase
from TAScheduler.models import Course as CourseModel, Lab as SectionModel, User as UserModel
from TAScheduler.models import PublicInfo, PrivateInfo, CourseTa as CourseTaModel
from classes import ta
from classes.ta import Ta
from classes.account import Account
from classes.course import Course
from classes.section import Section


class TestTaStaticMethods(TestCase):

    def setUp(self):
        self.user_model = UserModel.objects.create(
            email="test@email.com",
            password="password123",
            account_type="ta"
        )
        PublicInfo.objects.create(
            user_id=self.user_model,
            first_name="John",
            last_name="Doe"
        )
        PrivateInfo.objects.create(
            user_id=self.user_model
        )
        self.course_model = CourseModel.objects.create(
            course_name="test_course"
        )
        self.section_model = SectionModel.objects.create(
            lab_name="lab1",
            course_id=self.course_model
        )

    def test_accountToTaSuccess(self):
        test_key = self.user_model.pk
        result = ta.account_to_ta(test_key)
        self.assertIsInstance(result, Ta)

    def test_accountToTaFailure(self):
        test_key = self.user_model.pk + 1
        result = ta.account_to_ta(test_key)
        self.assertIsNone(result)

    def test_accountToTaWrongType(self):
        instructor_model = UserModel.objects.create(
            email="1",
            password="1",
            account_type="instructor"
        )
        test_key = instructor_model.pk
        result = ta.account_to_ta(test_key)
        self.assertIsNone(result)

    def test_getCourseTasBadCourse(self):
        ta_list = ta.get_course_tas(self.course_model.pk + 1)
        self.assertIsNone(ta_list)

    def test_getCourseTasNoTas(self):
        ta_list = ta.get_course_tas(self.course_model.pk)
        self.assertEqual(ta_list, [])

    def test_getCourseTasSuccess(self):
        CourseTaModel.objects.create(course_id=self.course_model, ta_id=self.user_model)
        ta_list = ta.get_course_tas(self.course_model.pk)
        is_list_of_tas = isinstance(ta_list, list) and isinstance(ta_list.pop(), Ta)
        self.assertTrue(is_list_of_tas)

    def test_getSectionTaBadSection(self):
        section_ta = ta.get_section_ta(self.section_model.pk + 1)
        self.assertIsNone(section_ta)

    def test_getSectionTaNoTa(self):
        section_ta = ta.get_section_ta(self.section_model.pk)
        self.assertIsNone(section_ta)

    def test_getSectionTaSuccess(self):
        self.section_model.ta_id = self.user_model
        section_ta = ta.get_section_ta(self.section_model.pk)
        self.assertIsInstance(section_ta, Ta)

    def test_getAllTasReturnsTaList(self):
        ta_list = ta.get_all_tas()
        self.assertIsInstance(ta_list, list)
        self.assertIsInstance(ta_list.pop(), Ta)

    def test_getAllTasCorrectAccountType(self):
        UserModel.objects.create(
            email="1",
            password="1",
            account_type="instructor"
        )
        ta_list = ta.get_all_tas()
        self.assertEqual(len(ta_list), 1)
        self.assertEqual(ta_list.pop().get_account_type(), "ta")


class TestTaClassMethods(TestCase):

    def setUp(self):
        self.user_model = UserModel.objects.create(
            email="test@email.com",
            password="password123",
            account_type="ta"
        )
        PublicInfo.objects.create(
            user_id=self.user_model,
            first_name="John",
            last_name="Doe"
        )
        PrivateInfo.objects.create(
            user_id=self.user_model
        )
        self.course_model = CourseModel.objects.create(
            course_name="test_course"
        )
        self.section_model = SectionModel.objects.create(
            lab_name="lab1",
            course_id=self.course_model
        )
        self.ta_instance = Ta(Account(self.user_model))

    def test_getGraderStatusBadCourse(self):
        CourseTaModel.objects.create(course_id=self.course_model, ta_id=self.user_model, is_grader=True)
        grader_status = self.ta_instance.get_grader_status(self.course_model.pk + 1)
        self.assertIsNone(grader_status)

    def test_getGraderStatusSuccess(self):
        CourseTaModel.objects.create(course_id=self.course_model, ta_id=self.user_model, is_grader=True)
        grader_status = self.ta_instance.get_grader_status(self.course_model.pk)
        self.assertTrue(grader_status)

    def test_setGraderStatusBadCourse(self):
        CourseTaModel.objects.create(course_id=self.course_model, ta_id=self.user_model, is_grader=False)
        grader_status = self.ta_instance.set_grader_status(self.course_model.pk + 1, True)
        self.assertFalse(grader_status)

    def test_setGraderStatusModelChanged(self):
        CourseTaModel.objects.create(course_id=self.course_model, ta_id=self.user_model, is_grader=True)
        self.ta_instance.set_grader_status(self.course_model.pk, False)
        self.assertFalse(CourseTaModel.objects.get(course_id=self.course_model, ta_id=self.user_model).is_grader)

    def test_setGraderStatusTrueOnSuccess(self):
        CourseTaModel.objects.create(course_id=self.course_model, ta_id=self.user_model, is_grader=True)
        function_return = self.ta_instance.set_grader_status(self.course_model.pk, False)
        self.assertTrue(function_return)

    def test_getNumberSectionsBadCourse(self):
        CourseTaModel.objects.create(course_id=self.course_model, ta_id=self.user_model, number_of_labs=2)
        number_sections = self.ta_instance.get_number_sections(self.course_model.pk + 1)
        self.assertIsNone(number_sections)

    def test_getNumberSectionsSuccess(self):
        CourseTaModel.objects.create(course_id=self.course_model, ta_id=self.user_model, number_of_labs=2)
        number_sections = self.ta_instance.get_number_sections(self.course_model.pk)
        self.assertEqual(number_sections, 2)

    def test_setNumberSectionsBadCourse(self):
        CourseTaModel.objects.create(course_id=self.course_model, ta_id=self.user_model, number_of_labs=2)
        self.assertFalse(self.ta_instance.set_number_sections(self.course_model.pk + 1, 1))

    def test_setNumberSectionsModelChanged(self):
        CourseTaModel.objects.create(course_id=self.course_model, ta_id=self.user_model, number_of_labs=2)
        self.ta_instance.set_number_sections(self.course_model.pk, 1)
        new_count = CourseTaModel.objects.get(course_id=self.course_model, ta_id=self.user_model).number_of_labs
        self.assertEqual(new_count, 1)

    def test_setNumberSectionsTrueOnSuccess(self):
        CourseTaModel.objects.create(course_id=self.course_model, ta_id=self.user_model, number_of_labs=2)
        function_return = self.ta_instance.set_number_sections(self.course_model.pk, 1)
        self.assertTrue(function_return)

    def test_getCoursesNoMatches(self):
        my_list = self.ta_instance.get_courses()
        self.assertEqual(my_list, [])

    def test_getCoursesSuccess(self):
        CourseTaModel.objects.create(course_id=self.course_model, ta_id=self.user_model)
        course_list = self.ta_instance.get_courses()
        self.assertIsInstance(course_list.pop(), Course)

    def test_addToCourseBadCourse(self):
        self.assertFalse(self.ta_instance.add_to_course(self.course_model.pk + 1))

    def test_addToCourseAlreadyAdded(self):
        CourseTaModel.objects.create(course_id=self.course_model, ta_id=self.user_model)
        self.assertFalse(self.ta_instance.add_to_course(self.course_model))

    def test_addToCourseSuccess(self):
        self.assertTrue(self.ta_instance.add_to_course(self.course_model.pk))

    def test_removeFromCourseBadCourse(self):
        self.assertFalse(self.ta_instance.remove_from_course(self.course_model.pk + 1))

    def test_removeFromCourseAlreadyRemoved(self):
        self.assertFalse(self.ta_instance.remove_from_course(self.course_model.pk))

    def test_removeFromCourseSuccess(self):
        CourseTaModel.objects.create(course_id=self.course_model, ta_id=self.user_model)
        self.assertTrue(self.ta_instance.remove_from_course(self.course_model.pk))

    def test_getSectionsNoMatches(self):
        sections_list = self.ta_instance.get_sections()
        self.assertEqual(sections_list, [])

    def test_getSectionsSuccess(self):
        SectionModel.objects.create(lab_name="1", course_id=self.course_model, ta_id=self.user_model)
        section_list = self.ta_instance.get_sections()
        self.assertIsInstance(section_list.pop(), Section)

    def test_addToSectionBadSection(self):
        self.assertFalse(self.ta_instance.add_to_section(self.section_model.pk + 1))

    def test_addToSectionAlreadyAdded(self):
        SectionModel.objects.create(lab_name="1", course_id=self.course_model, ta_id=self.user_model)
        self.assertTrue(self.ta_instance.add_to_section(self.section_model.pk))

    def test_addToSectionSuccess(self):
        self.assertTrue(self.ta_instance.add_to_section(self.section_model.pk))

    def test_removeFromSectionBadSection(self):
        self.assertFalse(self.ta_instance.remove_from_section(self.section_model.pk + 1))

    def test_removeFromSectionAlreadyRemoved(self):
        self.assertFalse(self.ta_instance.remove_from_section(self.section_model.pk))

    def test_removeFromSectionSuccess(self):
        SectionModel.objects.create(lab_name="1", course_id=self.course_model, ta_id=self.user_model)
        self.assertTrue(self.ta_instance.remove_from_section(self.section_model.pk))
