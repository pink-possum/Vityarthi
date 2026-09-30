# Library Management System

  

A modular, zero-configuration Command-Line Interface (CLI) Library Management System built with Python. Designed for portable deployment, it implements persistent relational data storage using flat CSV files without requiring external database engine installation.

  

---

  

## Features

  

- **Catalog Management:** Register new titles and perform case-insensitive substring searches across ISBN, Title, and Author fields.

- **Member Directory:** Enroll student and faculty members with automatic incremental ID assignment.

- **Circulation Lifecycle:**

- Issue books with automatic stock validation and 14-day due date computation.

- Return books with real-time inventory restoration.

- Automatic overdue fine calculation (₹2.00/day past due).

- **Tabular Reporting:** Live generation of formatted tables for:

- Complete Available Inventory

- Currently Active Loans

- Overdue Loans

- **Defensive Input Handling:** Built-in validation guarding against invalid menu choices, missing identifiers, and empty catalog searches.

  

---

  

## Architecture & Module Breakdown

  

The system adopts a 3-tier modular package structure:

  

```text

library_management_system/

├── config.py # Global constants, file paths, fine rate settings

├── db_init.py # Generic CSV read, atomic write, and auto-ID utilities

├── library_operations.py # Catalog ingestion and search query filtering

├── members.py # Patron registration and profile lookup

├── transactions.py # Circulation state machine, date math, fine logic, reports

├── main.py # Interactive CLI loop and presentation routing

├── requirements.txt # Project runtime dependencies

├── statement.md # Formal project scope and requirements specification

└── README.md # Setup guide and technical documentation

```

## Technologies Used

* **Language:** Python 3.8+
* **Standard Library:** `csv`, `datetime`, `os`
* **Third-Party Dependencies:** `tabulate` (terminal table formatting)
* **Version Control:** Git & GitHub

---

## Setup & Installation

Follow these steps to set up and run the application in an isolated environment:

### 1. Clone the Repository
```bash
git clone https://github.com/pink-possum/Vityarthi.git
cd Vityarthi
```
### 2. Create a Virtual Environment

```bash
# On macOS / Linux:
python3 -m venv venv

# On Windows:
python -m venv venv
```
### 3. Activate the Virtual Environment
```bash
# On macOS / Linux:
source venv/bin/activate

# On Windows (Command Prompt):
venv\Scripts\activate

# On Windows (PowerShell):
venv\Scripts\Activate.ps1
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```
### 5. Launch the Application
```bash
# On macOS / Linux:
python3 main.py

# On Windows:
python main.py
```
### 6. Deactivate Environment (When Finished)
```bash
deactivate
```

## Manual Testing Instructions

Verify boundary handling and relational updates with the following test procedures:

### 1. Boundary Test (Out of Stock Handling)
* **Action:** Attempt to issue a title where `available_copies` is `0`.
* **Expected Result:** The system denies the transaction, outputs a warning banner, and prevents appending to `transactions.csv`.

### 2. Negative Test (Input Validation)
* **Action:** Provide non-numeric characters when prompted for `Member ID` or `Book ID`.
* **Expected Result:** Caught by internal exception handling; displays an `Invalid Input` prompt without unhandled traceback crashes.

### 3. Integration Test (State Transition & Fines)
* **Action:** Run Option 5 to return Transaction ID `4` (due on September 24, 2026).
* **Expected Result:** System applies dynamic fine math based on the current date, registers the return timestamp, and immediately increments the corresponding book's `available_copies` by 1.

## Visual Workflows & CLI Interface

### 1. Main Navigation & Search
Interactive CLI dashboard displaying keyword-filtered catalog results.

### 2. Circulation Processing
Loan validation checking real-time stock thresholds and writing the transaction.

### 3. Return & Overdue Assessment
Automated penalty calculation and stock replenishment upon book check-in.