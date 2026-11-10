# Blood Bank Management System

A Python-based Blood Bank Management System developed using SQLite and Tkinter as part of a Database Management Systems (DBMS) academic project.

## Project Overview

The application manages donation centres, blood donations and processed blood units through a relational database and a graphical user interface.

## Technologies Used

- Python
- SQLite
- Tkinter
- SQL

## Database Structure

The application uses three relational tables:

1. **Centres** – Stores donation centre information and transfusion officer contact emails.
2. **Donations** – Stores donor information, donation dates and centre references.
3. **Blood Units** – Stores processed blood unit types, quantities and donation references.

## Key Features

- Add new blood donation records.
- Automatically create new donation centre profiles when required.
- Reuse existing donation centre records.
- Delete donation centres, donations and individual blood units.
- Cascading deletion using foreign-key constraints.
- Display combined records using SQL JOIN operations.
- View individual database tables.
- Input validation and automatic database refresh.
- Graphical dashboard using Tkinter.

## How to Run

**Requirements:** Python 3 with Tkinter support.

1. Download or clone this repository.
2. Open the project folder.
3. Run the following command:

```bash
python3 blood_bank_app.py
```

4. The application automatically initializes the SQLite database and inserts sample records if the database is completely empty.
5. The Blood Bank Management System dashboard will open.

## Database

The application uses SQLite. The database file is automatically created in the same directory as the Python script.

## Academic Project

Developed as a Database Management Systems (DBMS) project.
