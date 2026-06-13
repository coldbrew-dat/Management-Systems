# Class Definitions
class Student:
    def __init__(self, student_id, name, status):
        self.student_id = student_id
        self.name = name
        self.status = status

    def results(self):
        print("Student ID: " + str(self.student_id) + "\nName: " + self.name + "\nStatus: " + str(self.status))

class Course:
    def __init__(self, course_id, course_name, credit_hours):
        self.course_id = course_id
        self.course_name = course_name
        self.credit_hours = credit_hours

    def results(self):
        print("Course ID: " + str(self.course_id) + "\nCourse Name: " + self.course_name + "\nCredit Hours: " + str(self.credit_hours))

class Teacher:
    def __init__(self, teacher_id, name, department):
        self.teacher_id = teacher_id
        self.name = name
        self.department = department

    def results(self):
        print("Teacher ID: " + str(self.teacher_id) + "\nTeacher Name: " + self.name + "\nDepartment: " + self.department)

class Fee:
    def __init__(self, student_id, amount):
        self.student_id = student_id
        self.amount = amount

    def results(self):
        print("Student ID: " + str(self.student_id) + "\nAmount: " + str(self.amount))

class Exams:
    def __init__(self, student_id, course_id, marks):
        self.student_id = student_id
        self.course_id = course_id
        self.marks = marks

    def results(self):
        print("Student ID: " + str(self.student_id) + "\nCourse ID: " + str(self.course_id) + "\nMarks: " + str(self.marks))

class Hostel:
    def __init__(self, student_id, room_number, pay_status):
        self.student_id = student_id
        self.room_number = room_number
        self.pay_status = pay_status

    def results(self):
        print("Student ID: " + str(self.student_id) + "\nRoom Number: " + str(self.room_number) + "\nPayment Status: " + str(self.pay_status))

class Attendance:
    def __init__(self, student_id, attendance_percent):
        self.student_id = student_id
        self.attendance_percent = attendance_percent

    def results(self):
        print("Student ID: " + str(self.student_id) + "\nAttendance: " + str(self.attendance_percent) + "%")

class Enrollment:
    def __init__(self, student_id, course_id):
        self.student_id = student_id
        self.course_id = course_id

    def results(self):
        print("Student ID: " + str(self.student_id) + "\nCourse ID: " + str(self.course_id))



# Function to get student input
def get_student_input():
    students = []
    count = 0
    for count in range(10):  # Asking for 10 students
        print("\nEnter details for Student: ")
        student_id = int(input("Enter Student ID: "))
        name = input("Enter Student Name: ")
        age = int(input("Enter Student Age: "))
        students.append(Student(student_id, name, age))
        count = count + 1
    return students

# Function to get course input
def get_course_input():
    courses = []
    count = 0
    for count in range(10):  # Asking for 5 courses
        print("\nEnter details for Course: ")
        course_id = int(input("Enter Course ID: "))
        course_name = input("Enter Course Name: ")
        credit_hours = input("Enter Credit Hours: ")
        courses.append(Course(course_id, course_name, credit_hours))
        count = count + 1
    return courses

# Function to get teacher input
def get_teacher_input():
    teachers = []
    count = 0
    for count in range(10):  # Asking for 3 teachers
        print("\nEnter details for Teacher: ")
        teacher_id = int(input("Enter Teacher ID: "))
        name = input("Enter Teacher Name: ")
        department = input("Enter Department: ")
        teachers.append(Teacher(teacher_id, name, department))
        count = count + 1
    return teachers

# Function to get fee input
def get_fee_input():
    fees = []
    count = 0
    for count in range(10):  # Asking for 10 fee records
        print("\nEnter Fee details for Student: ")
        student_id = int(input("Enter Student ID: "))
        amount_due = float(input("Enter Amount Due: "))
        fees.append(Fee(student_id, amount_due))
        count = count + 1
    return fees

# Function to get exam input
def get_exam_input():
    exams = []
    count = 0
    for count in range(10):  # Asking for 10 exam records
        print("\nEnter Exam details for Student: ")
        student_id = int(input("Enter Student ID: "))
        course_id = input("Enter Course ID: ")
        marks = int(input("Enter Marks: "))
        exams.append(Exams(student_id, course_id, marks))
        count = count + 1
    return exams

# Function to get hostel input
def get_hostel_input():
    hostels = []
    count = 0
    for count in range(10):  # Asking for 10 hostel records
        print("\nEnter Hostel details for Student: ")
        student_id = int(input("Enter Student ID: "))
        room_number = int(input("Enter Room Number: "))
        pay_status = input("Enter Pay Status: ")
        hostels.append(Hostel(student_id, room_number, pay_status))
        count = count + 1
    return hostels

# Function to get attendance input
def get_attendance_input():
    attendance = []
    count = 0
    for count in range(10):  # Asking for 10 attendance records
        print("\nEnter Attendance details for Student: ")
        student_id = int(input("Enter Student ID: "))
        attendance_percent = float(input("Enter Attendance Percentage: "))
        attendance.append(Attendance(student_id, attendance_percent))
        count = count + 1
    return attendance

# Function to get enrollment input
def get_enrollment_input():
    enrollments = []
    count = 0
    for count in range(10):  # Asking for 10 enrollment records
        print("\nEnter Enrollment details for Student: ")
        student_id = int(input("Enter Student ID: "))
        course_id = int(input("Enter Course ID: "))
        enrollments.append(Enrollment(student_id, course_id))
        count = count + 1
    return enrollments

# Main Program Loop
while True:
    print("\nWelcome to the Student Management System!")
    print("1. Enter Student Data")
    print("2. Enter Course Data")
    print("3. Enter Teacher Data")
    print("4. Enter Fee Data")
    print("5. Enter Exam Data")
    print("6. Enter Hostel Data")
    print("7. Enter Attendance Data")
    print("8. Enter Enrollment Data")
    print("9. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        students = get_student_input()
        for student in students:
            student.results()
    elif choice == 2:
        courses = get_course_input()
        for course in courses:
            course.results()
    elif choice == 3:
        teachers = get_teacher_input()
        for teacher in teachers:
            teacher.results()
    elif choice == 4:
        fees = get_fee_input()
        for fee in fees:
            fee.results()
    elif choice == 5:
        exams = get_exam_input()
        for exam in exams:
            exam.results()
    elif choice == 6:
        hostels = get_hostel_input()
        for hostel in hostels:
            hostel.results()
    elif choice == 7:
        attendances = get_attendance_input()
        for attendance in attendances:
            attendance.results()
    elif choice == 8:
        enrollments = get_enrollment_input()
        for enrollment in enrollments:
            enrollment.results()
    elif choice == 9:
        print("Exiting the system.")
    else:
        print("Invalid choice! Please try again.")

