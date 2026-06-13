# 🎓 Student Management System

**Course:** IT in Business 
**Language:** Python (Console-based)  

---

## Overview

A console-based Student Management System built entirely in Python during the first semester. This was the first major project — no GUI, no database, just core Python: classes, objects, loops, and input/output. The focus was on understanding Object-Oriented Programming fundamentals and structuring a multi-entity system cleanly.

---

## Features

- **Student Management** — Add and display student records (ID, name, status)
- **Course Management** — Register courses with credit hours
- **Teacher Management** — Store teacher details by department
- **Fee Tracking** — Record fee amounts per student
- **Exam Records** — Log marks per student per course
- **Hostel Management** — Assign rooms and track payment status
- **Attendance Tracking** — Record attendance percentage per student
- **Enrollment** — Link students to courses
- **Interactive Menu** — Loop-driven CLI menu for all modules

---

## Tech Stack

| Component | Detail |
|-----------|--------|
| Language | Python  |
| Interface | Console / CLI |
| Storage | In-memory (runtime only) |
| Libraries | None (pure Python) |

---

## How to Run

```bash
python student_management_system.py
```

Follow the on-screen menu to navigate between modules. Enter data for up to 10 records per category.

---

## Project Structure

```
student_management_system.py
│
├── Classes
│   ├── Student
│   ├── Course
│   ├── Teacher
│   ├── Fee
│   ├── Exams
│   ├── Hostel
│   ├── Attendance
│   └── Enrollment
│
└── Functions
    ├── get_student_input()
    ├── get_course_input()
    ├── get_teacher_input()
    ├── get_fee_input()
    ├── get_exam_input()
    ├── get_hostel_input()
    ├── get_attendance_input()
    └── get_enrollment_input()
```

---

## Concepts Demonstrated

- Object-Oriented Programming (classes, constructors, methods)
- Modular function design
- List-based in-memory data storage
- User input handling and validation
- Control flow with loops and conditionals

---

## Limitations

- Data is not persisted — all records are lost on exit
- No search, edit, or delete functionality
- Fixed input count (10 records per module)
- No input validation beyond basic type casting

> These limitations were intentional for the scope of a Semester 1 project. Later projects address persistence, GUI, and database integration.

---

## Notes

This project was built independently as a Semester 1 final project for the IT in Business course. It represents foundational Python and OOP concepts before any GUI or database exposure.
