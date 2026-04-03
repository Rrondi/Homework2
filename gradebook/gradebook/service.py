from gradebook.models import Student, Course, Enrollment
from gradebook.storage import load_data, save_data


class GradebookService:
    def __init__(self, path="data/gradebook.json"):
        self.path = path
        self.data = load_data(self.path)
    # Instead of checking for the existence of students, courses, and enrollments
    # in multiple places I wrote some helper functions

    def _find_student(self, student_id):
        for student in self.data["students"]:
            if student["id"] == str(student_id):
                return student
        return None

    def _find_course(self, course_code):
        for course in self.data["courses"]:
            if course["code"] == course_code:
                return course
        return None

    def _find_enrollment(self, student_id, course_code):
        for enrollment in self.data["enrollments"]:
            if (
                enrollment["student_id"] == str(student_id)
                and enrollment["course_code"] == course_code
            ):
                return enrollment
        return None

    def _generate_student_id(self):
        max_id = 0

        for student in self.data["students"]:
            if str(student["id"]).isdigit():
                current_id = int(student["id"])
                if current_id > max_id:
                    max_id = current_id

        return str(max_id + 1)

    def add_student(self, name):
        student_id = self._generate_student_id()
        student = Student(student_id, name)

        self.data["students"].append({
            "id": student.id,
            "name": student.name
        })

        save_data(self.data, self.path)
        return student.id

    def add_course(self, code, title):
        if self._find_course(code):
            raise ValueError(f"Course with code '{code}' already exists")

        course = Course(code, title)

        self.data["courses"].append({
            "code": course.code,
            "title": course.title
        })

        save_data(self.data, self.path)

    def enroll(self, student_id, course_code):
        if not self._find_student(student_id):
            raise ValueError(f"Student with id '{student_id}' does not exist")

        if not self._find_course(course_code):
            raise ValueError(
                f"Course with code '{course_code}' does not exist")

        if self._find_enrollment(student_id, course_code):
            raise ValueError("Student is already enrolled in this course")

        enrollment = Enrollment(str(student_id), course_code, [])

        self.data["enrollments"].append({
            "student_id": enrollment.student_id,
            "course_code": enrollment.course_code,
            "grades": enrollment.grades
        })

        save_data(self.data, self.path)

    def add_grade(self, student_id, course_code, grade):
        if not isinstance(grade, (int, float)):
            raise ValueError("Grade must be numeric")

        if grade < 0 or grade > 100:
            raise ValueError("Grade must be between 0 and 100")

        enrollment = self._find_enrollment(student_id, course_code)
        if not enrollment:
            raise ValueError("Enrollment not found")

        enrollment["grades"].append(grade)
        save_data(self.data, self.path)

    def list_students(self):
        students = []

        for student in self.data["students"]:
            students.append(Student(student["id"], student["name"]))

        return sorted(students, key=lambda s: s.name.lower())

    def list_courses(self):
        courses = []

        for course in self.data["courses"]:
            courses.append(Course(course["code"], course["title"]))

        return sorted(courses, key=lambda c: c.code.lower())

    def list_enrollments(self):
        enrollments = []

        for enrollment in self.data["enrollments"]:
            enrollments.append(
                Enrollment(
                    enrollment["student_id"],
                    enrollment["course_code"],
                    enrollment["grades"]
                )
            )

        return sorted(enrollments, key=lambda e: (e.student_id, e.course_code.lower()))

    def compute_average(self, student_id, course_code):
        enrollment = self._find_enrollment(student_id, course_code)

        if not enrollment:
            raise ValueError("Enrollment not found")

        grades = enrollment["grades"]

        if len(grades) == 0:
            return 0.0

        return sum(grades) / len(grades)

    def compute_gpa(self, student_id):
        student_enrollments = []

        for enrollment in self.data["enrollments"]:
            if enrollment["student_id"] == str(student_id):
                student_enrollments.append(enrollment)

        averages = []

        for enrollment in student_enrollments:
            grades = enrollment["grades"]
            if len(grades) > 0:
                averages.append(sum(grades) / len(grades))

        if len(averages) == 0:
            return 0.0

        return sum(averages) / len(averages)
