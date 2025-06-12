# 🚆 Java Online Reservation System

A simple console-based Java application that simulates an online train ticket reservation and cancellation system.

## 📌 Features

- 🔐 **Login System** – Only authorized users can access the system.
- 📝 **Reservation System** – Users can book tickets by entering basic details and journey information.
- ❌ **Cancellation System** – Cancel reserved tickets using the PNR number.
- 📁 **File-Based Storage** – Reservation data is stored and managed via a local text file (`reservations.txt`).

---

## 🛠️ Tech Stack

- Java (JDK 8+)
- VS Code (or any Java IDE)
- File I/O (for data persistence)

---

## 🖥️ Modules

### 1. LoginForm.java
Handles authentication with hardcoded credentials.

### 2. ReservationSystem.java
Takes user input (name, age, train details, etc.), generates a PNR, and stores booking data in `reservations.txt`.

### 3. CancellationForm.java
Finds and cancels a reservation using the PNR number after user confirmation.

### 4. Main.java
Main entry point of the application. It shows the menu and routes user actions to the appropriate module.

---

## 📂 Project Structure

## 📂 Project Structure

```bash
OnlineReservationSystem/
│
├── LoginForm.java
├── ReservationSystem.java
├── CancellationForm.java
├── Main.java
├── reservations.txt  # stores reservation records
└── README.md

