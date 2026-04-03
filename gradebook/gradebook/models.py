class Student:
    def __init__(self, id, name):
        if not id:
            raise ValueError("Id cannot be empty")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Student name must be a string and not be empty")

        self.id = id
        self.name = name.strip()

    def __str__(self):
        return f"Student(id={self.id}, name='{self.name}')"


class Course:
    def __init__(self, code, title):
        if not isinstance(code, str) or not code.strip():
            raise ValueError("Course code must be a non-empty string")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Course title must be a non-empty string")

        self.code = code.strip()
        self.title = title.strip()

    def __str__(self):
        return f"Course(code='{self.code}', title='{self.title}')"


class Enrollment:
    # grades is None because a student might not have a grade
    def __init__(self, student_id, course_code, grades=None):
        if not student_id:
            raise ValueError("Student ID cannot be empty")
        if not isinstance(course_code, str) or not course_code.strip():
            raise ValueError("Course code must be a non-empty string")

        if not isinstance(grades, list):
            raise ValueError("Grades must be a list")

        if grades == None:
            grades = []

        if not isinstance(grades, list):
            raise ValueError("Grades must be a list")

        for g in grades:
            if g < 0 or g > 100:
                raise ValueError("Grades must be between 0 and 100")

        self.student_id = student_id
        self.course_code = course_code.strip()
        self.grades = grades

    def __str__(self):
        return (
            f"Enrollment(student_id={self.student_id}, "
            f"course_code='{self.course_code}', grades={self.grades})"
        )
