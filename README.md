# 📚 Gradebook CLI Application

A simple Python CLI application to manage students, courses, enrollments, and grades.

---

## Setup Instructions

### 1. Clone / Download the project

```bash
git clone <your-repo-url>
cd gradebook
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

This project uses only standard Python libraries, so no extra installation is required.

## Seed Sample Data

To populate the application with sample data:

```bash
python -m scripts.seed
```

Or run the script directly:

```bash
python scripts/seed.py
```

This creates or updates:

- `data/gradebook.json`

Seeded data includes:

- 3 students
- 2 courses
- enrollments
- grades

## CLI Usage

Run commands using:

```bash
python main.py <command> [options]
```

### Add a student

```bash
python main.py add-student --name "Rron"
```

Expected output:

```text
Student added successfully with ID 1.
```

### Add a course

```bash
python main.py add-course --code CS101 --title "Intro to CS"
```

Expected output:

```text
Course 'CS101 - Intro to CS' added successfully.
```

### Enroll a student

```bash
python main.py enroll --student-id 1 --course CS101
```

Expected output:

```text
Student 1 enrolled in course CS101 successfully.
```

### Add a grade

```bash
python main.py add-grade --student-id 1 --course CS101 --grade 95
```

Expected output:

```text
Grade 95.0 added for student 1 in course CS101.
```

### List data

Students:

```bash
python main.py list students
```

Courses:

```bash
python main.py list courses
```

Enrollments:

```bash
python main.py list enrollments
```

### Compute average

```bash
python main.py avg --student-id 1 --course CS101
```

Expected output:

```text
Average for student 1 in course CS101: 90.00
```

### Compute GPA

```bash
python main.py gpa --student-id 1
```

Expected output:

```text
GPA for student 1: 88.50
```

## Run Tests

From the project root (`gradebook`):

```bash
python -m unittest discover -s tests
```

## Logging

Logs are stored in:

- `logs/app.log`

They include:

- Data loading/saving
- Validation and runtime errors

## 🧠 Design Decisions and Limitations

### Design Decisions

- Architecture:
  - `models.py` for data models
  - `service.py` for business logic
  - `storage.py` for JSON persistence
- JSON file storage is used for simplicity and portability
- CLI is built with `argparse`
- Validation is handled in both CLI parsing and service/model logic
- Logging is implemented with Python's `logging` module

### Limitations

- No database support (data is stored in a JSON file)
- No concurrency handling for simultaneous writers
- No authentication
- GPA is a simple average-based calculation
- No update/delete commands for students or courses
