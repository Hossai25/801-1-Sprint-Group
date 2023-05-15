from django import test
from django.http.request import HttpRequest
from TAScheduler.models import User as UserModel, Course as CourseModel, \
    CourseTa as TaModel, Lab as LabModel, PublicInfo, PrivateInfo
from TAScheduler import views
from django.urls import reverse


class TestDisplayCourseGetContext(test.TestCase):
    def setUp(self):
        self.view = views.DisplayCourse()
        self.request = HttpRequest()
        self.request.session = {"email": "test_email", "account_type": "test_account_type", "user": -1}

        self.tas = []
        self.sections = []
        self.instructors = []

        instructor_data = ["instructor1", "instructor2", "instructor3"]
        for i in range(len(instructor_data)):
            temp_user = UserModel(email=instructor_data[i], password=instructor_data[i], account_type="instructor")
            temp_user.save()
            PublicInfo(user_id=temp_user).save()
            PrivateInfo(user_id=temp_user).save()
            self.instructors.append(temp_user)

        self.course_instructor = self.instructors[1]
        self.course = CourseModel(course_name="course1", instructor_id=self.course_instructor)
        self.course.save()

        ta_data = ["ta1", "ta2", "ta3", "ta4", "ta5"]
        section_data = ["section1", "section2", "section3", "section4", "section5"]
        for i in range(len(ta_data)):
            temp_user = UserModel(email=ta_data[i], password=ta_data[i], account_type="ta")
            temp_user.save()
            self.tas.append(temp_user)
            PublicInfo(user_id=temp_user).save()
            PrivateInfo(user_id=temp_user).save()
            temp_ta = TaModel(course_id=self.course, ta_id=temp_user, is_grader=(i < 4), number_of_labs=i)
            temp_ta.save()
            temp_section = LabModel(lab_name=section_data[i], course_id=self.course, ta_id=temp_user)
            temp_section.save()
            self.sections.append(temp_section)

    def test_method_exists(self):
        with self.assertRaises(TypeError):
            self.view.get_context()

    def test_two_parameters(self):
        try:
            self.view.get_context(self.request, 1)
        except TypeError:
            self.assertTrue(False, "Method should accept HttpResponse and int")
        except Exception:
            self.assertTrue(True, "This error message should never appear")

    def test_email(self):
        key = "email"
        result = self.view.get_context(self.request, self.course.pk)
        self.assertIn(key, result, f"key {key} not in result")
        self.assertEqual(result[key], self.request.session[key], f"value for key {key} was changed")

    def test_account_type(self):
        key = "account_type"
        result = self.view.get_context(self.request, self.course.pk)
        self.assertIn(key, result, f"key {key} not in result")
        self.assertEqual(result[key], self.request.session[key], f"value for key {key} was changed")

    def test_user(self):
        key = "user"
        result = self.view.get_context(self.request, self.course.pk)
        self.assertIn(key, result, f"key {key} not in result")
        self.assertEqual(result[key], self.request.session[key], f"value for key {key} was changed")

    def test_course(self):
        key = "course"
        result = self.view.get_context(self.request, self.course.pk)
        self.assertIn(key, result, f"key {key} not in result")
        self.assertEqual(result[key].course_model, self.course, f"unexpected value for key {key}")

    def test_course_tas(self):
        key = "course_tas"
        result = self.view.get_context(self.request, self.course.pk)
        self.assertIn(key, result, f"key {key} not in result")
        course_tas = [x.user_model for x in result[key]]
        for ta_result in course_tas:
            self.assertIn(ta_result, self.tas, f"unexpected account {ta_result.email} in {key}")
        for expected_ta in self.tas:
            self.assertIn(expected_ta, course_tas, f"ta {expected_ta.email} not found in {key}")

    def test_course_instructor(self):
        key = "course_instructor"
        result = self.view.get_context(self.request, self.course.pk)
        self.assertIn(key, result, f"key {key} not in result")
        self.assertEqual(result[key].user_model, self.course_instructor, f"unexpected value for key {key}")

    def test_ta_list(self):
        key = "ta_list"
        result = self.view.get_context(self.request, self.course.pk)
        self.assertIn(key, result, f"key {key} not in result")
        ta_list = [x.user_model for x in result[key]]
        for ta_result in ta_list:
            self.assertIn(ta_result, self.tas, f"unexpected account {ta_result.email} in {key}")
        for expected_ta in self.tas:
            self.assertIn(expected_ta, ta_list, f"ta {expected_ta.email} not found in {key}")

    def test_instructor_list(self):
        key = "instructor_list"
        result = self.view.get_context(self.request, self.course.pk)
        self.assertIn(key, result, f"key {key} not in result")
        instructor_list = [x.user_model for x in result[key]]
        for instructor_result in instructor_list:
            self.assertIn(instructor_result, self.instructors, f"unexpected account {instructor_result.email} in {key}")
        for expected_instructor in self.instructors:
            self.assertIn(expected_instructor, instructor_list, f"instructor {expected_instructor.email} not found in {key}")

    def test_sections(self):
        key = "sections"
        result = self.view.get_context(self.request, self.course.pk)
        self.assertIn(key, result, f"key {key} not in result")
        section_list = [x.lab_model for x in result[key]]
        for section_result in section_list:
            self.assertIn(section_result, self.sections, f"unexpected section {section_result.lab_name} in {key}")
        for expected_section in self.sections:
            self.assertIn(expected_section, section_list, f"section {expected_section.lab_name} not found in {key}")

    def test_course_instructor(self):
        key = "back_href"
        result = self.view.get_context(self.request, self.course.pk)
        self.assertIn(key, result, f"key {key} not in result")
        self.assertEqual(result[key], reverse('courses'), f"unexpected value for key {key}")


if __name__ == '__main__':
    test.unittest.main()
