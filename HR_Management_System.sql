
-- ════════════════════════════════════════════════════════════════════════════
-- HR DEPARTMENT MANAGEMENT SYSTEM — DATABASE SCHEMA
-- With full RBAC (Role-Based Access Control) for 4 Department Users
-- ════════════════════════════════════════════════════════════════════════════

CREATE DATABASE hr_department;


-- ── EMPLOYEE TABLE ────────────────────────────────────────────────────────────
CREATE TABLE employee (
    employee_id       INT PRIMARY KEY,
    first_name        VARCHAR(50) NOT NULL,
    last_name         VARCHAR(50) NOT NULL,
    email             VARCHAR(50) UNIQUE NOT NULL,
    cnic              VARCHAR(50) UNIQUE NOT NULL,
    address           VARCHAR(50) NOT NULL,
    phone_no          VARCHAR(15) NOT NULL,
    birth_date        DATE NOT NULL,
    employment_status VARCHAR(20) NOT NULL,
    job_role          VARCHAR(20) NOT NULL,
    hire_date         DATE NOT NULL,

    CONSTRAINT chk_phone_no
        CHECK (phone_no != ''),

    CONSTRAINT chk_birth_date CHECK (
        (EXTRACT(YEAR FROM current_date) - EXTRACT(YEAR FROM birth_date) > 18)
        OR (
            EXTRACT(YEAR FROM current_date) - EXTRACT(YEAR FROM birth_date) = 18
            AND EXTRACT(MONTH FROM current_date) > EXTRACT(MONTH FROM birth_date)
        )
        OR (
            EXTRACT(YEAR FROM current_date) - EXTRACT(YEAR FROM birth_date) = 18
            AND EXTRACT(MONTH FROM current_date) = EXTRACT(MONTH FROM birth_date)
            AND EXTRACT(DAY FROM current_date) >= EXTRACT(DAY FROM birth_date)
        )
    ),

    CONSTRAINT chk_employment_status
        CHECK (employment_status IN ('full-time','part-time','internship','contract')),

    CONSTRAINT chk_job_role
        CHECK (job_role IN ('manager','hr','developer','designer')),

    CONSTRAINT chk_future_hire
        CHECK (hire_date <= current_date),

    CONSTRAINT chk_hire_after_18
        CHECK (EXTRACT(YEAR FROM hire_date) - EXTRACT(YEAR FROM birth_date) >= 18)
);

-- ── DEPARTMENT TABLE ──────────────────────────────────────────────────────────
CREATE TABLE department (
    dep_id      INT PRIMARY KEY,
    employee_id INT NOT NULL,
    dep_name    VARCHAR(50) NOT NULL,

    CONSTRAINT chk_dep_name
        CHECK (dep_name IN ('it','design','management','hr')),

    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

-- ── SALARY TABLE ──────────────────────────────────────────────────────────────
CREATE TABLE salary (
    payroll_id   INT PRIMARY KEY,
    employee_id  INT NOT NULL,
    amount       DECIMAL(10,2) NOT NULL,
    bonus        DECIMAL(10,2) DEFAULT 0.00,
    deductions   DECIMAL(10,2) DEFAULT 0.00,
    payment_date DATE,

    CONSTRAINT chk_salary_amount CHECK (amount > 0),
    CONSTRAINT chk_bonus         CHECK (bonus >= 0),
    CONSTRAINT chk_deductions    CHECK (deductions >= 0),
    CONSTRAINT chk_payment_date  CHECK (payment_date <= current_date),

    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

-- ── ATTENDANCE TABLE ──────────────────────────────────────────────────────────
-- NOTE: Only HR and Admin roles are permitted to INSERT / UPDATE / DELETE
-- this table.  The application layer enforces this via ATTENDANCE_EDIT_ROLES.
CREATE TABLE attendance_table (
    attendance_id INT PRIMARY KEY,
    employee_id   INT NOT NULL,
    employee_name VARCHAR(50),          -- denormalised convenience column
    status        VARCHAR(15) NOT NULL,
    att_date      DATE NOT NULL,

    CONSTRAINT chk_att_status
        CHECK (status IN ('present','absent','leave')),

    CONSTRAINT chk_att_date
        CHECK (att_date <= current_date),

    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

-- ── APPLICANT TABLE ───────────────────────────────────────────────────────────
CREATE TABLE applicant (
    applicant_id   INT PRIMARY KEY,
    applicant_name VARCHAR(50) NOT NULL,
    a_position     VARCHAR(50) NOT NULL,
    a_status       VARCHAR(10) NOT NULL,

    CONSTRAINT chk_a_position
        CHECK (a_position IN ('manager','hr','developer','designer')),

    CONSTRAINT chk_a_status
        CHECK (a_status IN ('pending','selected','rejected'))
);

-- ── INTERVIEW TABLE ───────────────────────────────────────────────────────────
CREATE TABLE interview_table (
    interview_id INT PRIMARY KEY,
    applicant_id INT NOT NULL,
    i_result     VARCHAR(50) NOT NULL,
    i_date       DATE NOT NULL,

    CONSTRAINT chk_i_result
        CHECK (i_result IN ('pass','fail','pending')),

    CONSTRAINT chk_i_date
        CHECK (i_date <= current_date),

    FOREIGN KEY (applicant_id) REFERENCES applicant(applicant_id)
);

-- ════════════════════════════════════════════════════════════════════════════
-- RBAC TABLES  (users + rolee)
-- ════════════════════════════════════════════════════════════════════════════

-- ── USERS TABLE ───────────────────────────────────────────────────────────────
-- Added: department column — tracks which organisational unit owns this user
CREATE TABLE users (
    user_id       INT PRIMARY KEY,
    user_name     VARCHAR(50) NOT NULL,
    user_password VARCHAR(50) UNIQUE NOT NULL,
    department    VARCHAR(20) DEFAULT 'general',

    CONSTRAINT chk_user_name CHECK (user_name != '')
);

-- ── ROLES TABLE ───────────────────────────────────────────────────────────────
-- Expanded role_name check to include new department roles
CREATE TABLE rolee (
    role_id   INT PRIMARY KEY,
    user_id   INT NOT NULL,
    role_name VARCHAR(50) NOT NULL,

    CONSTRAINT chk_role_name CHECK (
        role_name IN (
            'admin',        -- full system access
            'hr',           -- HR department: all data + attendance edit
            'finance',      -- Finance: salary/payroll read + finance reports
            'operations',   -- Operations: employees, departments, hiring (read)
            'manager',      -- Manager: broad access (no users page)
            'employee',     -- Basic employee: dashboard only
            'developer',    -- Developer: dashboard only
            'designer',     -- Designer: dashboard only
            'senior_manager', -- Future role, same as manager
            'junior',         -- Future role, restricted
            'director'        -- Future role, admin-like
        )
    ),

    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- ════════════════════════════════════════════════════════════════════════════
-- SEED DATA — EMPLOYEES
-- ════════════════════════════════════════════════════════════════════════════
INSERT INTO employee VALUES
(1,  'ali',    'khan',   'ali@gmail.com',   '4210112345671', 'karachi',    '03001234567', '1995-05-10', 'full-time',   'developer', '2018-06-01'),
(2,  'sara',   'ahmed',  'sara@gmail.com',  '3520212345672', 'lahore',     '03011234567', '1998-03-12', 'part-time',   'designer',  '2020-02-15'),
(3,  'usman',  'ali',    'usman@gmail.com', '6110312345673', 'islamabad',  '03021234567', '1997-07-20', 'full-time',   'manager',   '2019-09-10'),
(4,  'amna',   'shah',   'amna@gmail.com',  '4210412345674', 'karachi',    '03031234567', '2000-01-05', 'internship',  'hr',        '2023-01-10'),
(5,  'hamza',  'raza',   'hamza@gmail.com', '3520512345675', 'lahore',     '03041234567', '1996-11-30', 'contract',    'developer', '2021-05-18'),
(6,  'noor',   'fatima', 'noor@gmail.com',  '3310612345676', 'faisalabad', '03051234567', '1999-09-09', 'full-time',   'designer',  '2022-03-01'),
(7,  'bilal',  'hassan', 'bilal@gmail.com', '3610712345677', 'multan',     '03061234567', '1994-04-14', 'full-time',   'manager',   '2017-08-25'),
(8,  'ayesha', 'khan',   'ayesha@gmail.com','4210812345678', 'karachi',    '03071234567', '2001-06-22', 'part-time',   'hr',        '2022-10-11'),
(9,  'zain',   'malik',  'zain@gmail.com',  '3520912345679', 'lahore',     '03081234567', '1993-12-01', 'full-time',   'developer', '2016-04-05'),
(10, 'hira',   'noor',   'hira@gmail.com',  '6111012345670', 'islamabad',  '03091234567', '1998-08-18', 'contract',    'designer',  '2020-12-20');

-- ── DEPARTMENTS ───────────────────────────────────────────────────────────────
INSERT INTO department VALUES
(1,  1,  'it'),
(2,  2,  'design'),
(3,  3,  'management'),
(4,  4,  'hr'),
(5,  5,  'it'),
(6,  6,  'design'),
(7,  7,  'management'),
(8,  8,  'hr'),
(9,  9,  'it'),
(10, 10, 'design');

-- ── SALARY ────────────────────────────────────────────────────────────────────
INSERT INTO salary VALUES
(1,  1,  120000, 5000, 2000, '2024-01-31'),
(2,  2,  80000,  3000, 1000, '2024-01-31'),
(3,  3,  150000, 7000, 3000, '2024-01-31'),
(4,  4,  50000,  2000,  500, '2024-01-31'),
(5,  5,  110000, 4000, 1500, '2024-01-31'),
(6,  6,  90000,  3500, 1000, '2024-01-31'),
(7,  7,  160000, 8000, 4000, '2024-01-31'),
(8,  8,  60000,  2500,  800, '2024-01-31'),
(9,  9,  140000, 6000, 2500, '2024-01-31'),
(10, 10, 95000,  3000, 1200, '2024-01-31');

-- ── ATTENDANCE (sample — normally HR inserts these) ───────────────────────────
-- CSV import (skip if importing via file):
-- COPY attendance_table (attendance_id, employee_id, status, att_date)
-- FROM 'C:/temp/attendance.csv' DELIMITER ',' CSV HEADER;

-- ── APPLICANTS ────────────────────────────────────────────────────────────────
INSERT INTO applicant VALUES
(1,  'ahmad',  'developer', 'pending'),
(2,  'laiba',  'designer',  'selected'),
(3,  'junaid', 'manager',   'rejected'),
(4,  'sana',   'hr',        'selected'),
(5,  'saad',   'developer', 'pending'),
(6,  'maryam', 'designer',  'rejected'),
(7,  'rizwan', 'manager',   'selected'),
(8,  'fatima', 'hr',        'pending'),
(9,  'taha',   'developer', 'selected'),
(10, 'mehak',  'designer',  'pending');

-- ── INTERVIEWS ────────────────────────────────────────────────────────────────
INSERT INTO interview_table VALUES
(1,  1,  'pass',    '2024-03-01'),
(2,  2,  'pass',    '2024-03-02'),
(3,  3,  'fail',    '2024-03-03'),
(4,  4,  'pass',    '2024-03-04'),
(5,  5,  'fail',    '2024-03-05'),
(6,  6,  'fail',    '2024-03-06'),
(7,  7,  'pass',    '2024-03-07'),
(8,  8,  'pass',    '2024-03-08'),
(9,  9,  'pass',    '2024-03-09'),
(10, 10, 'pending', '2024-03-10');

-- ════════════════════════════════════════════════════════════════════════════
-- RBAC SEED DATA — 4 DEPARTMENT USERS + LEGACY USERS
-- ════════════════════════════════════════════════════════════════════════════

-- ── The 4 required department users ──────────────────────────────────────────
INSERT INTO users (user_id, user_name, user_password, department) VALUES
-- Department login accounts
(101, 'admin_user',   'admin123',   'admin'),
(102, 'hr_user',      'hr123',      'hr'),
(103, 'finance_user', 'finance123', 'finance'),
(104, 'ops_user',     'ops123',     'operations'),

-- Legacy individual-level users (kept for backward compatibility)
(1,  'admin1', 'pass123', 'admin'),
(2,  'user2',  'pass234', 'general'),
(3,  'user3',  'pass345', 'general'),
(4,  'user4',  'pass456', 'hr'),
(5,  'user5',  'pass567', 'general'),
(6,  'user6',  'pass678', 'general'),
(7,  'user7',  'pass789', 'general'),
(8,  'user8',  'pass890', 'hr'),
(9,  'user9',  'pass901', 'general'),
(10, 'user10', 'pass012', 'general');

-- ── Role assignments ──────────────────────────────────────────────────────────
INSERT INTO rolee (role_id, user_id, role_name) VALUES
-- 4 department roles
(101, 101, 'admin'),
(102, 102, 'hr'),
(103, 103, 'finance'),
(104, 104, 'operations'),

-- Legacy individual roles
(1,  1,  'admin'),
(2,  2,  'employee'),
(3,  3,  'employee'),
(4,  4,  'hr'),
(5,  5,  'developer'),
(6,  6,  'designer'),
(7,  7,  'manager'),
(8,  8,  'hr'),
(9,  9,  'developer'),
(10, 10, 'designer');

-- ════════════════════════════════════════════════════════════════════════════
-- VERIFICATION QUERIES
-- ════════════════════════════════════════════════════════════════════════════

-- Show all users and their roles (RBAC overview)
---- list of all employees
select * from employee;

---- employees by department
select e.first_name, e.last_name, d.dep_name
from employee e
join department d on e.employee_id = d.employee_id
order by d.dep_name, e.first_name;

---- salary report
select e.employee_id, e.first_name, e.last_name, d.dep_name, s.amount, s.bonus, s.deductions,
       (s.amount + s.bonus - s.deductions) as net_salary,
       s.payment_date
from employee e
join salary s on e.employee_id = s.employee_id
join department d on e.employee_id = d.employee_id
order by s.payment_date desc;

---- list of newly hired employees
select employee_id, first_name, last_name, job_role, hire_date
from employee
order by hire_date desc;

---- department wise employee count
select d.dep_name,
       count(e.employee_id) as employee_count
from department d
join employee e on d.employee_id = e.employee_id
group by d.dep_name
order by employee_count desc;

---- employee payroll report
select e.employee_id, e.first_name, e.last_name, d.dep_name, s.payroll_id, s.amount as basic_salary,
       s.bonus, s.deductions,
       (s.amount + s.bonus - s.deductions) as net_pay,
       s.payment_date
from employee e
join salary s on e.employee_id = s.employee_id
join department d on e.employee_id = d.employee_id
order by s.payment_date desc;

---- list of job applicants
select applicant_id, applicant_name, a_position, a_status
from applicant
order by applicant_name;

---- selected and rejected candidates report
select a.applicant_id, a.applicant_name, a.a_position, a.a_status, i.i_result, i.i_date
from applicant a
join interview_table i on a.applicant_id = i.applicant_id
where a.a_status in ('selected', 'rejected')
order by a.a_status, i.i_date desc;

---- interview schedule report
select i.interview_id, a.applicant_name, a.a_position, i.i_date, i.i_result, a.a_status
from interview_table i
join applicant a on i.applicant_id = a.applicant_id
order by i.i_date desc;



---- ADVANCED REPORTS-----
---top paid employees
SELECT e.first_name, s.amount
FROM employee e
JOIN salary s ON e.employee_id = s.employee_id
ORDER BY s.amount DESC
LIMIT 5;

--- department with highest salaries
SELECT d.dep_name, SUM(s.amount) AS total_salary
FROM salary s
JOIN employee e ON s.employee_id = e.employee_id
JOIN department d ON e.dep_id = d.dept_id
GROUP BY d.dept_name
ORDER BY total_salary DESC
LIMIT 1;

--- Employees with most absences
SELECT e.first_name, COUNT(*) AS absent_days
FROM attendance_table a
JOIN employee e ON a.employee_id = e.employee_id
WHERE a.status = 'absent'
GROUP BY e.first_name
ORDER BY absent_days DESC;

--- Employees earning above average salary
SELECT e.first_name, e.last_name, s.amount
FROM employee e
JOIN salary s ON e.employee_id = s.employee_id
WHERE s.amount > (
    SELECT AVG(amount)
    FROM salary
);

--- Employees with more than 3 absences
SELECT first_name, last_name
FROM employee
WHERE employee_id IN (
    SELECT employee_id
    FROM attendance_table
    WHERE status = 'absent'
    GROUP BY employee_id
    HAVING COUNT(*) > 3
);

--- RBAC 
SELECT u.user_name, r.role_name
FROM users u
JOIN rolee r ON u.user_id = r.user_id;

--- department salary report
SELECT d.dep_name,
       SUM(s.amount + s.bonus - s.deductions) AS total_department_salary
FROM salary s
JOIN employee e ON s.employee_id = e.employee_id
JOIN department d ON e.employee_id = d.employee_id
GROUP BY d.dep_name;

--- hiring summary report
SELECT a_status, COUNT(*) AS total_applicants
FROM applicant
GROUP BY a_status;

-- Show permission summary (conceptual — enforced in Python app layer)
-- Admin      → All pages + all reports
-- HR         → All pages except Users; can edit attendance
-- Finance    → Dashboard + Salary (read-only) + Finance reports only
-- Operations → Dashboard + Employees/Departments/Applicants/Interviews (read) + Ops reports



select * from attendance_table