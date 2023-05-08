from django import test
from TAScheduler import views

class TestDisplayCourseGetContext(test.TestCase):
    def setUp(self):
        self.view = views.DisplayCourse()
        self.request = {"email": "test_email", "account_type": "test_account_type"}

    def test_method_exists(self):
        with self.assertRaises(TypeError):
            self.view.get_context()

    def test_x(self):
        pass


if __name__ == '__main__':
    test.unittest.main()
