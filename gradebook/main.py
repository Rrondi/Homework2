import argparse
import logging
import os
from gradebook.service import GradebookService


# get project root (directory of main.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# create logs folder at root
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def parse_student_id(value):
    if not value:
        raise ValueError("Student ID cannot be empty")

    if not str(value).isdigit():
        raise ValueError("Student ID must be a number")

    return str(value)


def parse_course_code(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Course code must be a non-empty string")

    return value.strip()


def parse_grade(value):
    try:
        grade = float(value)
    except:
        raise ValueError("Grade must be a number")

    if grade < 0 or grade > 100:
        raise ValueError("Grade must be between 0 and 100")

    return grade


def main():
    service = GradebookService()

    parser = argparse.ArgumentParser(description="Gradebook CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_student_parser = subparsers.add_parser(
        "add-student", help="Add a new student")
    add_student_parser.add_argument(
        "--name", required=True, help="Student name")

    add_course_parser = subparsers.add_parser(
        "add-course", help="Add a new course")
    add_course_parser.add_argument("--code", required=True, help="Course code")
    add_course_parser.add_argument(
        "--title", required=True, help="Course title")

    enroll_parser = subparsers.add_parser(
        "enroll", help="Enroll a student in a course")
    enroll_parser.add_argument(
        "--student-id", required=True, help="Student ID")
    enroll_parser.add_argument("--course", required=True, help="Course code")

    add_grade_parser = subparsers.add_parser(
        "add-grade", help="Add a grade to a student's course")
    add_grade_parser.add_argument(
        "--student-id", required=True, help="Student ID")
    add_grade_parser.add_argument(
        "--course", required=True, help="Course code")
    add_grade_parser.add_argument(
        "--grade", required=True, type=float, help="Grade")

    list_parser = subparsers.add_parser(
        "list", help="List students, courses, or enrollments")
    list_parser.add_argument(
        "entity", choices=["students", "courses", "enrollments"])
    list_parser.add_argument(
        "--sort", choices=["name", "code"], help="Optional sort field")

    avg_parser = subparsers.add_parser(
        "avg", help="Compute average for a student in a course")
    avg_parser.add_argument("--student-id", required=True, help="Student ID")
    avg_parser.add_argument("--course", required=True, help="Course code")

    gpa_parser = subparsers.add_parser("gpa", help="Compute GPA for a student")
    gpa_parser.add_argument("--student-id", required=True, help="Student ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        if args.command == "add-student":
            name = args.name.strip()
            if not name:
                raise ValueError("Student name cannot be empty")

            student_id = service.add_student(name)
            print(f"Student added successfully with ID {student_id}.")

        elif args.command == "add-course":
            code = parse_course_code(args.code)
            title = args.title.strip()

            if not title:
                raise ValueError("Course title cannot be empty")

            service.add_course(code, title)
            print(f"Course '{code} - {title}' added successfully.")

        elif args.command == "enroll":
            student_id = parse_student_id(args.student_id)
            course_code = parse_course_code(args.course)

            service.enroll(student_id, course_code)
            print(
                f"Student {student_id} enrolled in course {course_code} successfully.")

        elif args.command == "add-grade":
            student_id = parse_student_id(args.student_id)
            course_code = parse_course_code(args.course)
            grade = parse_grade(args.grade)

            service.add_grade(student_id, course_code, grade)
            print(
                f"Grade {grade} added for student {student_id} in course {course_code}."
            )

        elif args.command == "list":
            if args.entity == "students":
                students = service.list_students()

                if args.sort == "name":
                    students = sorted(students, key=lambda s: s.name.lower())

                if not students:
                    print("No students found.")
                else:
                    print("Students:")
                    for student in students:
                        print(f"  ID: {student.id}, Name: {student.name}")

            elif args.entity == "courses":
                courses = service.list_courses()

                if args.sort == "code":
                    courses = sorted(courses, key=lambda c: c.code.lower())

                if not courses:
                    print("No courses found.")
                else:
                    print("Courses:")
                    for course in courses:
                        print(f"  Code: {course.code}, Title: {course.title}")

            elif args.entity == "enrollments":
                enrollments = service.list_enrollments()

                if not enrollments:
                    print("No enrollments found.")
                else:
                    print("Enrollments:")
                    for enrollment in enrollments:
                        print(
                            f"  Student ID: {enrollment.student_id}, "
                            f"Course: {enrollment.course_code}, "
                            f"Grades: {enrollment.grades}"
                        )

        elif args.command == "avg":
            student_id = parse_student_id(args.student_id)
            course_code = parse_course_code(args.course)

            average = service.compute_average(student_id, course_code)
            print(
                f"Average for student {student_id} in course {course_code}: "
                f"{average:.2f}"
            )

        elif args.command == "gpa":
            student_id = parse_student_id(args.student_id)

            gpa = service.compute_gpa(student_id)
            print(f"GPA for student {student_id}: {gpa:.2f}")

    except ValueError as e:
        logging.error(f"Validation error: {e}")
        print(f"Error: {e}")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
