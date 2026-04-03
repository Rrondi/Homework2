import os
import unittest

from gradebook.gradebook.service import GradebookService


class TestGradebookService(unittest.TestCase):
    """Unit tests for Gradebook."""

    TEST_PATH = "data/test_gradebook.json"

    def setUp(self):
        """Create a fresh test service before each test."""
        if os.path.exists(self.TEST_PATH):
            os.remove(self.TEST_PATH)

        self.service = GradebookService(path=self.TEST_PATH)

    def tearDown(self):
        """Clean up test file after each test."""
        if os.path.exists(self.TEST_PATH):
            os.remove(self.TEST_PATH)

    def test_add_student(self):
        """Test adding a student successfully."""
        student_id = self.service.add_student("Rron")

        students = self.service.list_students()

        self.assertEqual(student_id, "1")
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0].name, "Rron")
        self.assertEqual(students[0].id, "1")

    def test_add_grade(self):
        """Test adding a grade successfully."""
        student_id = self.service.add_student("Rron")
        self.service.add_course("CS101", "Intro to CS")
        self.service.enroll(student_id, "CS101")

        self.service.add_grade(student_id, "CS101", 95)

        enrollments = self.service.list_enrollments()

        self.assertEqual(len(enrollments), 1)
        self.assertEqual(enrollments[0].grades, [95])

    def test_compute_average(self):
        """Test computing average successfully."""
        student_id = self.service.add_student("Rron")
        self.service.add_course("CS101", "Intro to CS")
        self.service.enroll(student_id, "CS101")
        self.service.add_grade(student_id, "CS101", 90)
        self.service.add_grade(student_id, "CS101", 80)

        average = self.service.compute_average(student_id, "CS101")

        self.assertEqual(average, 85.0)

    def test_add_grade_without_enrollment_raises_error(self):
        """Test adding a grade for a non-enrolled student raises ValueError."""
        student_id = self.service.add_student("Rron")
        self.service.add_course("CS101", "Intro to CS")

        with self.assertRaises(ValueError):
            self.service.add_grade(student_id, "CS101", 95)


if __name__ == "__main__":
    unittest.main()
