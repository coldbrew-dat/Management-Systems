# HR Management System

**Course:** Database Management / SQL  
**Semester:** 4  
**Language:** Python  
**Database:** PostgreSQL  
**Libraries:** Tkinter, psycopg2  
**Type:** Final Project

---

## Overview

A full-stack desktop HR Management System built with Python (Tkinter) as the frontend and PostgreSQL as the backend database. This was the most technically complex project across all four semesters — featuring a **Role-Based Access Control (RBAC)** system, a dark-themed modern GUI, and a complete set of HR modules covering employees, departments, payroll, attendance, applicants, interviews, and reports.

Four distinct department portals (Admin, HR, Finance, Operations) each have different levels of access, enforced at both the UI and query level.

---

## Features

### Role-Based Access Control (RBAC)
| Role | Portal Access |
|------|--------------|
| Admin | Full access — all modules + user management |
| HR | Employees, Departments, Salary (view), Attendance, Applicants, Interviews, Reports |
| Finance | Salary (read-only), Reports (finance reports only) |
| Operations | Employees (view), Departments (view), Applicants, Interviews, Reports |

### Modules

| Module | Description |
|--------|-------------|
| Dashboard | Role-specific KPI cards + live data tables |
| Employees | Full CRUD — hire date, job role, status, contact info |
| Departments | Assign employees to departments |
| Salary / Payroll | Track base salary, bonuses, deductions, net pay |
| Attendance | Mark present / absent / leave; edit restricted to HR & Admin |
| Applicants | Track job applicants and their application status |
| Interviews | Log interview results and dates per applicant |
| Reports | Pre-built SQL reports filtered by role |
| Users & Roles | Admin-only — add/remove system users and assign roles |

### Reports (Role-Filtered)
- Salary Report — All Employees
- Department Wise Salary Total
- Employees Earning Above Average Salary
- Employees With Most / More Than 3 Absences
- Monthly Attendance Summary
- Hiring Summary — Applicants
- Interview Results Report
- Selected Candidates Only
- Department Wise Employee Count
- Newly Hired Employees
- User Roles — RBAC (Admin only)
- Full Employee Payroll Report (Admin only)

---

## Tech Stack

| Component | Detail |
|-----------|--------|
| Language | Python 3 |
| GUI Framework | Tkinter + ttk |
| Database | PostgreSQL |
| DB Connector | psycopg2 |
| Design | Dark theme — custom color palette |

---

## Database Schema

```
Tables:
├── users          (user_id, user_name, user_password, department)
├── rolee          (role_id, user_id, role_name)
├── employee       (employee_id, first_name, last_name, email, cnic, address, phone_no, birth_date, employment_status, job_role, hire_date)
├── department     (dep_id, employee_id, dep_name)
├── salary         (payroll_id, employee_id, amount, bonus, deductions, payment_date)
├── attendance_table (attendance_id, employee_id, employee_name, status, att_date)
├── applicant      (applicant_id, applicant_name, a_position, a_status)
└── interview_table (interview_id, applicant_id, i_result, i_date)
```

---

## Default Login Accounts

| Department | Username | Password |
|------------|----------|----------|
| Admin | `admin_user` | `admin123` |
| HR | `hr_user` | `hr123` |
| Finance | `finance_user` | `finance123` |
| Operations | `ops_user` | `ops123` |

---

## Setup & Installation

### 1. Prerequisites
```bash
pip install psycopg2-binary
```

### 2. PostgreSQL Setup
- Create a database named `HR_Management_System`
- Update the connection details in `get_connection()` if needed:
```python
def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="HR_Management_System",
        user="postgres",
        password="your_password"
    )
```

### 3. Run the Application
```bash
python hr_management_system.py
```

The app will auto-run a DB setup script on first launch to create required columns and insert default users.

---

## Project Structure

```
hr_management_system.py
│
├── LoginWindow          ← Secure login with RBAC
├── HRApp                ← Main app shell + sidebar navigation
│
├── Pages
│   ├── Dashboard        ← Role-specific KPI cards
│   ├── EmployeesPage    ← Full CRUD
│   ├── DepartmentsPage  ← Department assignment
│   ├── SalaryPage       ← Payroll management
│   ├── AttendancePage   ← Attendance with edit restrictions
│   ├── ApplicantsPage   ← Applicant tracking
│   ├── InterviewsPage   ← Interview logging
│   ├── ReportsPage      ← Role-filtered SQL reports
│   └── UsersPage        ← Admin-only RBAC management
│
└── Helpers
    ├── Table            ← Reusable styled Treeview
    ├── make_entry()     ← Labeled entry field
    ├── make_combo()     ← Labeled dropdown
    └── action_btn()     ← Styled action button
```

---

## Concepts Demonstrated

- Full-stack desktop app with Python + PostgreSQL
- Role-Based Access Control (RBAC) — UI and database level
- Complex SQL queries with JOINs, aggregations, subqueries
- Reusable Tkinter component architecture
- Dynamic dashboard with live DB queries
- Dark-themed professional GUI design
- Auto schema migration on startup

---

## Notes

This was the Semester 4 final project for the Database Management / SQL course. The entire backend runs on PostgreSQL with `psycopg2` as the connector. The RBAC system was designed to reflect real-world enterprise access control — each role sees only what it needs to. AI assistance was used during development and is transparently acknowledged.
