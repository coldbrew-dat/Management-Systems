# 🚕 Cab Management System

**Course:** Programming in Business  
**Semester:** 2 / 3  
**Language:** Python  
**Libraries:** Tkinter, NumPy, Pandas, Matplotlib  
**Type:** Final Project

---

## Overview

A desktop Cab and Parcel Delivery Management System with a full Tkinter GUI. Built as the final project for the Programming in Business course, this system handles three types of users — **Customers**, **Drivers**, and an **Admin** — each with their own login portal and set of features. Data is persisted through flat `.txt` files.

This was a major step up from the Semester 1 console project: GUI windows, file I/O, fare calculation logic, and data visualization using Matplotlib.

---

## Features

### 👤 User (Customer)
- Register and log in with a username and password
- Book a **ride** — choose cab type and distance, get fare calculated automatically
- Book a **parcel delivery** — calculated by weight and distance
- View full **booking history**
- Confirm or cancel a ride before it's finalized

### 🚗 Driver
- Register and log in
- View all pending bookings
- **Accept a ride** and mark it as completed
- Toggle availability status (available / busy)

### 🛠️ Admin
- Secure login (credentials: `admin` / `123`)
- View all registered users and drivers
- View all bookings system-wide
- Generate a **Revenue Report** with:
  - Total revenue and booking counts
  - Bar chart — Booking type count
  - Line chart — Fare trend
  - Pie chart — Ride vs. Parcel share

---

## Tech Stack

| Component | Detail |
|-----------|--------|
| Language | Python 3 |
| GUI | Tkinter |
| Data Storage | Flat `.txt` files (CSV format) |
| Calculations | NumPy |
| Data Analysis | Pandas |
| Visualization | Matplotlib |

---

## File Structure

```
cab_management_system.py
users.txt          ← Registered users
drivers.txt        ← Registered drivers + availability status
bookings.txt       ← All booking records
```

---

## Fare Calculation Logic

**Rides:**
```
Base Fare: Rs 100
Rate: Rs 30/km  →  Bike, Auto
Rate: Rs 50/km  →  Mini Car, Car A/C
Total = Base Fare + (Rate × Distance)
```

**Parcels:**
```
Base Delivery: Rs 150
Total = 150 + (Weight × 20) + (Distance × 25)
```

---

## How to Run

```bash
pip install numpy pandas matplotlib
python cab_management_system.py
```

The main window will launch with options to register/login as a User, Driver, or Admin.

---

## Screenshots / Flow

```
Main Menu
├── Register User / Login User → Book Ride / Book Parcel / View History
├── Register Driver / Login Driver → View Bookings / Toggle Availability
└── Admin Login → View Users / Drivers / Bookings / Revenue Report
```

---

## Concepts Demonstrated

- Tkinter GUI with multiple nested windows (`Toplevel`)
- File I/O for persistent data storage
- Role-based access (User / Driver / Admin)
- Fare calculation with NumPy arrays
- Data analysis with Pandas DataFrames
- Multi-chart visualization with Matplotlib
- Input validation and error handling

---

## Notes

This project was built as the final project for the Programming in Business course. An earlier version of the project used `simpledialog` for all inputs (also included in this repo as commented-out code). The final version upgrades to proper form-based `Toplevel` windows for a better user experience.

AI assistance was used in parts of the development process and is transparently acknowledged.
