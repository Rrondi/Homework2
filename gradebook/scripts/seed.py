from gradebook.service import GradebookService


def seed():
    """Populate the gradebook with sample data."""

    service = GradebookService(path="data/gradebook.json")

    # Students
    s1 = service.add_student("Rron")
    s2 = service.add_student("Filan")
    s3 = service.add_student("Gentrit")

    #  Courses
    service.add_course("CS101", "Intro to CS")
    service.add_course("Python Fundamentals",
                       "Learn Python programming from scratch")

    # Enrollments
    service.enroll(s1, "CS101")
    service.enroll(s1, "Python Fundamentals")

    service.enroll(s2, "CS101")
    service.enroll(s3, "Python Fundamentals")

    #  Grades
    service.add_grade(s1, "CS101", 90)
    service.add_grade(s1, "CS101", 85)

    service.add_grade(s1, "Python Fundamentals", 88)

    service.add_grade(s2, "CS101", 75)

    service.add_grade(s3, "Python Fundamentals", 92)
    service.add_grade(s3, "Python Fundamentals", 87)

    print("Sample data created successfully!")


if __name__ == "__main__":
    seed()
