# Hotel Management System

A console-based Hotel Management System built in C++ that demonstrates core Object-Oriented Programming concepts including inheritance, polymorphism, operator overloading, file I/O, exception handling, and more.

---

## Features

- Make guest reservations with room type selection
- Process and track payment status
- Add and view hotel managers
- Persist all data to `.txt` files
- View total guest and manager counts

---

## OOP Concepts Demonstrated

| Concept | Where Used |
|---|---|
| Classes & Objects | `Hotel`, `Room`, `Guest`, `Payment`, `Manager`, `Reservation` |
| Inheritance | `StandardRoom`, `DeluxeRoom`, `SuiteRoom` → `Room`; `LobbyManager`, `OperationsManager` → `Manager` |
| Polymorphism | Virtual `display()` and `manager()` functions |
| Abstract Class | `Hotel` with pure virtual `display()` |
| Static Members | `Room::count`, `Guest::count`, `Manager::count` |
| Const Member | `guestID` in `Guest` |
| Aggregation | `Payment` holds a pointer to `Room` |
| Operator Overloading | `operator-` and `operator+` in `Payment` for charges |
| Copy Constructor | Shallow and deep copy in `Guest` |
| Friend Function / Class | `verifyPayment()` and `PaymentStatus` in `Payment` |
| Exception Handling | `try/catch` around reservation and payment saving |
| File I/O | `guests.txt`, `reservations.txt`, `payments.txt`, `managers.txt` |

---

## Room Types & Charges

| Room Type | Charge (PKR) |
|---|---|
| Standard | 500 |
| Deluxe | 1,500 |
| Suite | 3,000 |

---

## How to Run

### Requirements
- C++ compiler (g++ recommended)

### Compile & Run

```bash
g++ hotel.cpp -o hotel
./hotel
```

---

## Menu Options

```
MAIN MENU
1. Make Reservation     → Enter guest details, room number, room type, and payment status
2. Manager Section      → Add a new manager or view the managers list
3. Show Totals          → Display total number of guests and managers from saved files
4. Exit
```

---

## File Output

All data is saved locally in plain text files:

- `guests.txt` — Guest ID, name, payment status, CNIC verification
- `reservations.txt` — Guest name, room number, room type, payment status
- `payments.txt` — Payment date, room type, payment status
- `managers.txt` — Manager name and role (Lobby / Operations)

---

## Project Structure

```
hotel.cpp          → Main source file (all classes and logic)
guests.txt         → Auto-generated on first reservation
reservations.txt   → Auto-generated on first reservation
payments.txt       → Auto-generated on first reservation
managers.txt       → Auto-generated on first manager entry
```

---

## Notes

- Guest names with spaces should be entered without spaces (single-word input via `cin`)
- Payment date is hardcoded as `2025-12-07` for demonstration purposes
- `Hotel` class is abstract and not directly instantiated in the current implementation — designed for extension

---

## Author

Developed as part of an Object-Oriented Programming course project.
