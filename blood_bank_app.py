
import sqlite3
from pathlib import Path
from datetime import date
import tkinter as tk
from tkinter import ttk, messagebox

# ==========================================
# BLOOD BANK MANAGEMENT SYSTEM
# Database Initialization
# ==========================================

DB_NAME = Path(__file__).with_name("blood_bank.db")


def connect_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():

    conn = connect_db()
    cursor = conn.cursor()

    # 1. Create Centres Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS centres (
            centre_id INTEGER PRIMARY KEY AUTOINCREMENT,
            centre_name TEXT NOT NULL UNIQUE,
            contact_email TEXT NOT NULL
        )
    """)

    # 2. Create Donations Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donations (
            donation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            centre_id INTEGER NOT NULL,
            donor_name TEXT NOT NULL,
            donation_date TEXT NOT NULL,

            FOREIGN KEY (centre_id)
            REFERENCES centres(centre_id)
            ON DELETE CASCADE
        )
    """)

    # 3. Create Blood Units Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blood_units (
            unit_id INTEGER PRIMARY KEY AUTOINCREMENT,
            donation_id INTEGER NOT NULL,
            unit_type TEXT NOT NULL,
            quantity REAL NOT NULL CHECK(quantity >= 0),

            FOREIGN KEY (donation_id)
            REFERENCES donations(donation_id)
            ON DELETE CASCADE
        )
    """)

    # ==========================================
    # SAMPLE DATA INITIALIZATION
    # ==========================================

    cursor.execute("SELECT COUNT(*) FROM centres")
    centres_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM donations")
    donations_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM blood_units")
    units_count = cursor.fetchone()[0]

    # Seed only when all three tables are empty
    if centres_count == 0 and donations_count == 0 and units_count == 0:

        sample_centres = [
            ("City Blood Centre", "cityblood@example.com"),
            ("LifeCare Donation Unit", "lifecare@example.com"),
            ("Hope Blood Bank", "hope@example.com")
        ]

        cursor.executemany("""
            INSERT INTO centres (centre_name, contact_email)
            VALUES (?, ?)
        """, sample_centres)

        sample_donations = [
            (1, "Aarti Deshmukh", "2026-11-01"),
            (1, "Joseph Mathew", "2026-11-02"),
            (2, "Rahul Sharma", "2026-11-03"),
            (3, "Priya Nair", "2026-11-04")
        ]

        cursor.executemany("""
            INSERT INTO donations
            (centre_id, donor_name, donation_date)
            VALUES (?, ?, ?)
        """, sample_donations)

        sample_units = [
            (1, "Whole Blood (ml)", 450),
            (1, "Packed RBC (ml)", 250),
            (2, "Platelets (units)", 1),
            (3, "Whole Blood (ml)", 450),
            (4, "Packed RBC (ml)", 300)
        ]

        cursor.executemany("""
            INSERT INTO blood_units
            (donation_id, unit_type, quantity)
            VALUES (?, ?, ?)
        """, sample_units)

        print("Sample records inserted successfully.")

    else:
        print("Existing database records detected. Seeding skipped.")

    conn.commit()
    conn.close()

    print("Database initialized successfully!")
    print("Database location:", DB_NAME)


# ==========================================
# RUN DATABASE INITIALIZATION
# ==========================================


# ==========================================
# BLOOD BANK MANAGEMENT SYSTEM
# GRAPHICAL USER INTERFACE
# ==========================================

def create_dashboard():

    root = tk.Tk()
    root.title("Blood Bank Management System")
    root.geometry("1150x780")
    root.minsize(950, 650)
    root.configure(bg="#F5F5F5")

    # --------------------------------------
    # STYLING
    # --------------------------------------

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Treeview",
        rowheight=28,
        font=("Arial", 10)
    )

    style.configure(
        "Treeview.Heading",
        font=("Arial", 10, "bold"),
        background="#8B0000",
        foreground="white"
    )

    style.configure(
        "TNotebook.Tab",
        font=("Arial", 10, "bold"),
        padding=[15, 8]
    )

    # --------------------------------------
    # HEADER
    # --------------------------------------

    header = tk.Frame(root, bg="#8B0000", height=100)
    header.pack(fill="x")

    tk.Label(
        header,
        text="BLOOD BANK MANAGEMENT SYSTEM",
        font=("Arial", 23, "bold"),
        bg="#8B0000",
        fg="white"
    ).pack(pady=(20, 5))

    tk.Label(
        header,
        text="Donation Centre & Blood Unit Tracking Dashboard",
        font=("Arial", 11),
        bg="#8B0000",
        fg="white"
    ).pack()

    # --------------------------------------
    # MAIN CONTAINER
    # --------------------------------------

    main = tk.Frame(root, bg="#F5F5F5")
    main.pack(fill="both", expand=True, padx=20, pady=15)

    # --------------------------------------
    # INSERT PANEL
    # --------------------------------------

    insert_frame = tk.LabelFrame(
        main,
        text="  ADD NEW BLOOD DONATION  ",
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#8B0000",
        padx=18,
        pady=14
    )
    insert_frame.pack(fill="x", pady=(0, 15))

    # Input variables
    centre_var = tk.StringVar()
    email_var = tk.StringVar()
    donor_var = tk.StringVar()
    unit_var = tk.StringVar()
    quantity_var = tk.StringVar()

    # Two-column form layout. Each field has a visible label above it.
    insert_frame.columnconfigure(0, weight=1)
    insert_frame.columnconfigure(1, weight=1)

    def create_input_field(parent, label_text, variable, row, column, width=38):
        field_frame = tk.Frame(parent, bg="white")
        field_frame.grid(
            row=row, column=column, sticky="ew",
            padx=12, pady=8
        )
        field_frame.columnconfigure(0, weight=1)

        tk.Label(
            field_frame,
            text=label_text,
            bg="white",
            fg="#333333",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        entry = ttk.Entry(
            field_frame,
            textvariable=variable,
            width=width
        )
        entry.grid(row=1, column=0, sticky="ew", ipady=4)
        return entry

    create_input_field(
        insert_frame, "Donation Centre Name", centre_var, 0, 0
    )
    create_input_field(
        insert_frame, "Transfusion Officer Contact Email", email_var, 0, 1
    )
    create_input_field(
        insert_frame, "Donor Full Name", donor_var, 1, 0
    )

    # Unit type selector
    unit_frame = tk.Frame(insert_frame, bg="white")
    unit_frame.grid(row=1, column=1, sticky="ew", padx=12, pady=8)
    unit_frame.columnconfigure(0, weight=1)

    tk.Label(
        unit_frame,
        text="Blood Unit Type",
        bg="white",
        fg="#333333",
        font=("Arial", 10, "bold")
    ).grid(row=0, column=0, sticky="w", pady=(0, 5))

    unit_dropdown = ttk.Combobox(
        unit_frame,
        textvariable=unit_var,
        values=[
            "Whole Blood (ml)",
            "Packed RBC (ml)",
            "Platelets (units)"
        ],
        state="readonly",
        width=35
    )
    unit_dropdown.grid(row=1, column=0, sticky="ew", ipady=3)

    # Quantity field
    create_input_field(
        insert_frame, "Quantity Value", quantity_var, 2, 0
    )

    # --------------------------------------
    # REFRESH DATABASE TABLES
    # --------------------------------------

    def refresh_tables():

        conn = connect_db()
        cursor = conn.cursor()

        # Combined JOIN view

        join_query = """
            SELECT
                d.donation_id,
                c.centre_name,
                d.donor_name,
                d.donation_date,
                b.unit_type,
                b.quantity
            FROM donations d
            JOIN centres c
                ON d.centre_id = c.centre_id
            JOIN blood_units b
                ON d.donation_id = b.donation_id
            ORDER BY d.donation_id
        """

        joined_records = cursor.execute(join_query).fetchall()

        # Individual table views

        centres = cursor.execute(
            "SELECT * FROM centres"
        ).fetchall()

        donations = cursor.execute(
            "SELECT * FROM donations"
        ).fetchall()

        units = cursor.execute(
            "SELECT * FROM blood_units"
        ).fetchall()

        conn.close()

        datasets = [
            (join_tree, joined_records),
            (centre_tree, centres),
            (donation_tree, donations),
            (unit_tree, units)
        ]

        for tree, records in datasets:

            tree.delete(*tree.get_children())

            for record in records:
                tree.insert("", "end", values=record)

        status_label.config(
            text=f"Centres: {len(centres)}   |   "
                 f"Donations: {len(donations)}   |   "
                 f"Blood Units: {len(units)}"
        )
        refresh_delete_options()


# ==========================================
# DELETE PANEL FUNCTIONS
# ==========================================

    def refresh_delete_options():

        conn = connect_db()
        cursor = conn.cursor()

        centres = cursor.execute("""
            SELECT centre_id, centre_name
            FROM centres
            ORDER BY centre_id
        """).fetchall()

        donations = cursor.execute("""
            SELECT donation_id, donor_name
            FROM donations
            ORDER BY donation_id
        """).fetchall()

        units = cursor.execute("""
            SELECT unit_id, unit_type
            FROM blood_units
            ORDER BY unit_id
        """).fetchall()

        conn.close()

        # Prepare dropdown values

        centre_options = [
            f"{row[0]} - {row[1]}" for row in centres
        ]

        donation_options = [
            f"{row[0]} - {row[1]}" for row in donations
        ]

        unit_options = [
            f"{row[0]} - {row[1]}" for row in units
        ]

        # Update dropdowns and remove invalid selections

        dropdown_data = [
            (centre_delete_combo, centre_delete_var, centre_options),
            (donation_delete_combo, donation_delete_var, donation_options),
            (unit_delete_combo, unit_delete_var, unit_options)
        ]

        for combo, variable, options in dropdown_data:

            combo["values"] = options

            if variable.get() not in options:
                variable.set(options[0] if options else "")


    def delete_record(table_name, selection):

        if not selection:
            messagebox.showwarning(
                "No Selection",
                "Please select a record to delete."
            )
            return

        record_id = int(selection.split(" - ", 1)[0])

        # Confirm deletion

        if not messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete this {table_name} record?"
        ):
            return

        conn = connect_db()
        cursor = conn.cursor()

        try:

            if table_name == "centres":

                cursor.execute(
                    "DELETE FROM centres WHERE centre_id = ?",
                    (record_id,)
                )

            elif table_name == "donations":

                cursor.execute(
                    "DELETE FROM donations WHERE donation_id = ?",
                    (record_id,)
                )

            elif table_name == "blood_units":

                cursor.execute(
                    "DELETE FROM blood_units WHERE unit_id = ?",
                    (record_id,)
                )

            conn.commit()

            messagebox.showinfo(
                "Success",
                f"{table_name.replace('_', ' ').title()} deleted successfully!"
            )

            # Refresh all database views and dropdowns

            refresh_tables()

        except sqlite3.Error as error:

            conn.rollback()

            messagebox.showerror(
                "Database Error",
                str(error)
            )

        finally:
            conn.close()


    def delete_centre():
        delete_record("centres", centre_delete_var.get())


    def delete_donation():
        delete_record("donations", donation_delete_var.get())


    def delete_unit():
        delete_record("blood_units", unit_delete_var.get())


    # --------------------------------------
    # ADD RECORD FUNCTION
    # --------------------------------------

    def add_record():

        centre = centre_var.get().strip()
        email = email_var.get().strip()
        donor = donor_var.get().strip()
        unit = unit_var.get().strip()
        quantity = quantity_var.get().strip()

        # Blank field validation

        if not all([centre, email, donor, unit, quantity]):

            messagebox.showwarning(
                "Missing Information",
                "Please fill in all fields."
            )
            return

        # Quantity validation

        try:
            quantity_value = float(quantity)

            if quantity_value < 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Quantity",
                "Enter a valid non-negative numeric quantity."
            )
            return

        conn = connect_db()
        cursor = conn.cursor()

        try:

            # Check whether centre already exists

            cursor.execute(
                "SELECT centre_id FROM centres WHERE centre_name = ?",
                (centre,)
            )

            existing_centre = cursor.fetchone()

            if existing_centre:

                centre_id = existing_centre[0]

            else:

                cursor.execute("""
                    INSERT INTO centres
                    (centre_name, contact_email)
                    VALUES (?, ?)
                """, (centre, email))

                centre_id = cursor.lastrowid

            # Insert donation

            cursor.execute("""
                INSERT INTO donations
                (centre_id, donor_name, donation_date)
                VALUES (?, ?, ?)
            """, (centre_id, donor, date.today().isoformat()))

            donation_id = cursor.lastrowid

            # Insert blood unit

            cursor.execute("""
                INSERT INTO blood_units
                (donation_id, unit_type, quantity)
                VALUES (?, ?, ?)
            """, (donation_id, unit, quantity_value))

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Blood donation record added successfully!"
            )

            # Clear input fields

            centre_var.set("")
            email_var.set("")
            donor_var.set("")
            unit_var.set("")
            quantity_var.set("")

            # Refresh all four views

            refresh_tables()

        except sqlite3.Error as error:

            conn.rollback()

            messagebox.showerror(
                "Database Error",
                str(error)
            )

        finally:
            conn.close()

    # --------------------------------------
    # ADD RECORD BUTTON
    # --------------------------------------

    add_button_frame = tk.Frame(insert_frame, bg="white")
    add_button_frame.grid(
        row=3, column=0, columnspan=2, sticky="ew", padx=12, pady=(8, 2)
    )

    add_button = tk.Button(
        add_button_frame,
        text="+  ADD BLOOD DONATION",
        command=add_record,
        bg="#8B0000",
        fg="white",
        activebackground="#650000",
        activeforeground="white",
        font=("Arial", 10, "bold"),
        relief="flat",
        padx=22,
        pady=10,
        cursor="hand2"
    )
    add_button.pack(anchor="w")


# ==========================================
# DELETE PANEL INTERFACE
# ==========================================

    delete_frame = tk.LabelFrame(
        main,
        text="  DELETE DATABASE RECORDS  ",
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#8B0000",
        padx=15,
        pady=12
    )

    delete_frame.pack(fill="x", pady=(0, 15))

    centre_delete_var = tk.StringVar()
    donation_delete_var = tk.StringVar()
    unit_delete_var = tk.StringVar()

    # Centre deletion

    tk.Label(
        delete_frame,
        text="Donation Centre",
        bg="white",
        font=("Arial", 10, "bold")
    ).grid(row=0, column=0, padx=10, pady=8)

    centre_delete_combo = ttk.Combobox(
        delete_frame,
        textvariable=centre_delete_var,
        state="readonly",
        width=25
    )

    centre_delete_combo.grid(row=0, column=1, padx=10)

    ttk.Button(
        delete_frame,
        text="Delete Centre",
        command=delete_centre
    ).grid(row=0, column=2, padx=10)

    # Donation deletion

    tk.Label(
        delete_frame,
        text="Blood Donation",
        bg="white",
        font=("Arial", 10, "bold")
    ).grid(row=1, column=0, padx=10, pady=8)

    donation_delete_combo = ttk.Combobox(
        delete_frame,
        textvariable=donation_delete_var,
        state="readonly",
        width=25
    )

    donation_delete_combo.grid(row=1, column=1, padx=10)

    ttk.Button(
        delete_frame,
        text="Delete Donation",
        command=delete_donation
    ).grid(row=1, column=2, padx=10)

    # Blood unit deletion

    tk.Label(
        delete_frame,
        text="Blood Unit",
        bg="white",
        font=("Arial", 10, "bold")
    ).grid(row=2, column=0, padx=10, pady=8)

    unit_delete_combo = ttk.Combobox(
        delete_frame,
        textvariable=unit_delete_var,
        state="readonly",
        width=25
    )

    unit_delete_combo.grid(row=2, column=1, padx=10)

    ttk.Button(
        delete_frame,
        text="Delete Blood Unit",
        command=delete_unit
    ).grid(row=2, column=2, padx=10)

    # Load dropdown options

    refresh_delete_options()


    # --------------------------------------
    # TABBED DATABASE DISPLAY
    # --------------------------------------

    display_frame = tk.LabelFrame(
        main,
        text="  DATABASE RECORDS  ",
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#002A8B",
        padx=10,
        pady=10
    )

    display_frame.pack(fill="both", expand=True)

    notebook = ttk.Notebook(display_frame)
    notebook.pack(fill="both", expand=True)

    def create_table_tab(title, columns, headings):

        frame = ttk.Frame(notebook)

        notebook.add(frame, text=title)

        tree = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        for column, heading in zip(columns, headings):

            tree.heading(column, text=heading)

            tree.column(
                column,
                width=150,
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=tree.yview
        )

        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        return tree

    # Tab 1: Combined JOIN

    join_tree = create_table_tab(
        "All Records",
        ("id", "centre", "donor", "date", "unit", "quantity"),
        (
            "Donation ID",
            "Centre Name",
            "Donor Name",
            "Donation Date",
            "Unit Type",
            "Quantity"
        )
    )

    # Tab 2: Centres

    centre_tree = create_table_tab(
        "Centres",
        ("id", "name", "email"),
        ("Centre ID", "Centre Name", "Contact Email")
    )

    # Tab 3: Donations

    donation_tree = create_table_tab(
        "Donations",
        ("id", "centre_id", "donor", "date"),
        ("Donation ID", "Centre ID", "Donor Name", "Date")
    )

    # Tab 4: Blood Units

    unit_tree = create_table_tab(
        "Blood Units",
        ("id", "donation_id", "type", "quantity"),
        ("Unit ID", "Donation ID", "Unit Type", "Quantity")
    )

    # --------------------------------------
    # STATUS BAR
    # --------------------------------------

    status_label = tk.Label(
        root,
        text="Loading database...",
        bg="#8B0000",
        fg="white",
        font=("Arial", 10, "bold"),
        anchor="w",
        padx=15,
        pady=8
    )

    status_label.pack(fill="x", side="bottom")

    # Initial database display

    refresh_tables()

    root.mainloop()


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    initialize_database()
    create_dashboard()

