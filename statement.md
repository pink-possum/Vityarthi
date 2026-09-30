# Project Statement: Library Management System

## 1. Problem Statement
Small-to-medium institutional libraries frequently rely on manual register books or rigid legacy systems to track catalog records, student registrations, and physical checkouts. This manual workflow introduces significant bottlenecks:
- Slow transaction throughput during peak hours.
- Human error in tracking due dates and calculating overdue fines.
- Frequent discrepancies between physical inventory and paper records.
- Heavy infrastructure overhead when attempting to deploy full-scale enterprise database servers for simple standalone environments.

There is a distinct need for a portable, reliable, and lightweight digital tool that automates book inventory tracking, user management, and borrowing transactions without imposing database server installation overheads.

## 2. Scope of the Project
The Library Management System is a modular Command-Line Interface (CLI) application developed in Python. It provides persistent storage across structured CSV flat files while maintaining logical relational integrity in memory.

### In Scope:
- **Catalog Management:** Adding new book inventory records and real-time substring searches across ISBN, Title, and Author attributes.
- **Member Directory:** Registering student/faculty patrons and generating unique incremental identifiers.
- **Circulation & Transaction Engine:** Issuing books with real-time stock decrementing, 14-day loan term tracking, and automated return processing with daily overdue penalty assessments.
- **Analytical Reporting:** Real-time generation of relational views (Active Loans, Overdue Borrowers, Available Stock).
- **Zero-Dependency Persistence:** Safe I/O handling across `books.csv`, `members.csv`, and `transactions.csv`.

### Out of Scope:
- Multi-user network concurrency/locking across remote clients.
- Graphical User Interface (GUI) or web frontend.
- Automated SMS/Email notification dispatch.
- Payment gateway integration for fine settlement.

## 3. Target Users
- **Librarians / Library Assistants:** Primary operators responsible for checking books in/out, cataloging new acquisitions, and registering students.
- **Administrative Auditors:** Academic staff reviewing overdue reports, active circulation statistics, and inventory asset summaries.

## 4. High-Level Features
- **Dynamic Multi-Field Search:** Real-time keyword filtering allowing patrons or staff to locate books without requiring exact identifier matches.
- **Logical Relational Data Model:** Foreign key validation implemented programmatically, linking `member_id` and `book_id` into loan transaction ledgers.
- **Automated Fine Engine:** Dynamic calculation of late return penalties based on system date arithmetic (at a standard rate of ₹2.00/day).
- **Defensive Error Handling:** Input sanitization preventing program termination on invalid data types, nonexistent IDs, or out-of-stock borrow requests.

## 5. Non-Functional Requirements
- **Maintainability:** Separation of concerns using a 6-module decoupled Python package structure.
- **Portability:** Built strictly with standard Python libraries (`csv`, `datetime`, `os`) plus lightweight terminal formatting (`tabulate`), executing uniformly across Windows, macOS, and Linux.
- **Data Integrity:** Atomic file writes to prevent record truncation during updates.
- **Usability:** High-contrast, tabular terminal presentation for high scanability.