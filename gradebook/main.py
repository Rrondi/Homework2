import argparse
from gradebook.service import GradebookService


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
            student_id = service.add_student(args.name)
            print(f"Student added successfully with ID {student_id}.")

        elif args.command == "add-course":
            service.add_course(args.code, args.title)
            print(f"Course '{args.code} - {args.title}' added successfully.")

        elif args.command == "enroll":
            service.enroll(args.student_id, args.course)
            print(
                f"Student {args.student_id} enrolled in course {args.course} successfully.")

        elif args.command == "add-grade":
            service.add_grade(args.student_id, args.course, args.grade)
            print(
                f"Grade {args.grade} added for student {args.student_id} in course {args.course}."
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
            average = service.compute_average(args.student_id, args.course)
            print(
                f"Average for student {args.student_id} in course {args.course}: "
                f"{average:.2f}"
            )

        elif args.command == "gpa":
            gpa = service.compute_gpa(args.student_id)
            print(f"GPA for student {args.student_id}: {gpa:.2f}")

    except ValueError as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
