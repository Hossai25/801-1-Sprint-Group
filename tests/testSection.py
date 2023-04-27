import unittest
from TAScheduler.models import Lab
from classes.section import Section, create_section


class MyTestCase(unittest.TestCase):
    #def test_something(self):
        #self.assertEqual(True, False)  # add assertion here

    def test_createSectionSuccesful(self):
        self.assertEqual(create_section("testsection"), Lab(lab_name="testsection"))


if __name__ == '__main__':
    unittest.main()
