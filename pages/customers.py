# ============================================================
# pages/customers.py
# Smart Inventory Manager
# Customers Management
# ============================================================

import sqlite3

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QDialog,
    QFormLayout,
    QTextEdit,
)


DATABASE_FILE = "inventory.db"


# ============================================================
# Database
# ============================================================

def create_database():

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    cursor = connection.cursor()

    # إنشاء الجدول إذا لم يكن موجودًا
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            address TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # --------------------------------------------------------
    # إصلاح قاعدة البيانات القديمة
    # --------------------------------------------------------

    cursor.execute("""
        PRAGMA table_info(customers)
    """)

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    if "phone" not in columns:

        cursor.execute("""
            ALTER TABLE customers
            ADD COLUMN phone TEXT
        """)

    if "email" not in columns:

        cursor.execute("""
            ALTER TABLE customers
            ADD COLUMN email TEXT
        """)

    if "address" not in columns:

        cursor.execute("""
            ALTER TABLE customers
            ADD COLUMN address TEXT
        """)

    if "notes" not in columns:

        cursor.execute("""
            ALTER TABLE customers
            ADD COLUMN notes TEXT
        """)

    if "created_at" not in columns:

        cursor.execute("""
            ALTER TABLE customers
            ADD COLUMN created_at TIMESTAMP
        """)

        cursor.execute("""
            UPDATE customers
            SET created_at = CURRENT_TIMESTAMP
            WHERE created_at IS NULL
        """)

    connection.commit()

    connection.close()


# ============================================================
# Customer Dialog
# ============================================================

class CustomerDialog(QDialog):

    def __init__(
        self,
        parent=None,
        customer=None
    ):

        super().__init__(parent)

        self.customer = customer

        self.setup_ui()

        if customer:

            self.load_customer()

        self.update_language()

    # ========================================================
    # UI
    # ========================================================

    def setup_ui(self):

        self.setMinimumWidth(
            520
        )

        layout = QVBoxLayout(
            self
        )

        self.title_label = QLabel()

        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #172033;
                margin-bottom: 10px;
            }
        """)

        layout.addWidget(
            self.title_label
        )

        self.form = QFormLayout()

        # Name
        self.name_input = QLineEdit()

        self.form.addRow(
            self.name_input
        )

        # Phone
        self.phone_input = QLineEdit()

        self.form.addRow(
            self.phone_input
        )

        # Email
        self.email_input = QLineEdit()

        self.form.addRow(
            self.email_input
        )

        # Address
        self.address_input = QLineEdit()

        self.form.addRow(
            self.address_input
        )

        # Notes
        self.notes_input = QTextEdit()

        self.notes_input.setMaximumHeight(
            100
        )

        self.form.addRow(
            self.notes_input
        )

        layout.addLayout(
            self.form
        )

        # Buttons
        buttons = QHBoxLayout()

        buttons.addStretch()

        self.cancel_button = QPushButton()

        self.save_button = QPushButton()

        self.cancel_button.clicked.connect(
            self.reject
        )

        self.save_button.clicked.connect(
            self.save
        )

        buttons.addWidget(
            self.cancel_button
        )

        buttons.addWidget(
            self.save_button
        )

        layout.addLayout(
            buttons
        )

        self.apply_style()

    # ========================================================
    # Style
    # ========================================================

    def apply_style(self):

        self.setStyleSheet("""
            QDialog {
                background: #f8fafc;
            }

            QLabel {
                color: #172033;
            }

            QLineEdit,
            QTextEdit {

                background: white;

                border: 1px solid #d1d5db;

                border-radius: 8px;

                padding: 9px;

                font-size: 14px;
            }

            QLineEdit:focus,
            QTextEdit:focus {

                border: 2px solid #2563eb;
            }

            QPushButton {

                background: #2563eb;

                color: white;

                border: none;

                border-radius: 8px;

                padding: 10px 18px;

                font-weight: bold;
            }

            QPushButton:hover {

                background: #1d4ed8;
            }
        """)

    # ========================================================
    # Language
    # ========================================================

    def update_language(self):

        title = (
            "Edit Customer"
            if self.customer
            else "Add Customer"
        )

        self.setWindowTitle(
            title
        )

        self.title_label.setText(
            title
        )

        labels = [
            "Customer Name:",
            "Phone:",
            "Email:",
            "Address:",
            "Notes:",
        ]

        for index, text in enumerate(
            labels
        ):

            item = self.form.itemAt(
                index,
                QFormLayout.LabelRole
            )

            if item and item.widget():

                item.widget().setText(
                    text
                )

        self.cancel_button.setText(
            "Cancel"
        )

        self.save_button.setText(
            "Save"
        )

    # ========================================================
    # Load Customer
    # ========================================================

    def load_customer(self):

        self.name_input.setText(
            str(
                self.customer["name"]
                or ""
            )
        )

        self.phone_input.setText(
            str(
                self.customer["phone"]
                or ""
            )
        )

        self.email_input.setText(
            str(
                self.customer["email"]
                or ""
            )
        )

        self.address_input.setText(
            str(
                self.customer["address"]
                or ""
            )
        )

        self.notes_input.setPlainText(
            str(
                self.customer["notes"]
                or ""
            )
        )

    # ========================================================
    # Save
    # ========================================================

    def save(self):

        name = (
            self.name_input
            .text()
            .strip()
        )

        if not name:

            QMessageBox.warning(
                self,
                "Missing Data",
                "Please enter customer name."
            )

            return

        self.accept()

    # ========================================================
    # Get Data
    # ========================================================

    def get_data(self):

        return {

            "name":
                self.name_input
                .text()
                .strip(),

            "phone":
                self.phone_input
                .text()
                .strip(),

            "email":
                self.email_input
                .text()
                .strip(),

            "address":
                self.address_input
                .text()
                .strip(),

            "notes":
                self.notes_input
                .toPlainText()
                .strip(),

        }


# ============================================================
# Customers Page
# ============================================================

class CustomersPage(QWidget):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(parent)

        create_database()

        self.setup_ui()

        self.load_customers()

    # ========================================================
    # UI
    # ========================================================

    def setup_ui(self):

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            30,
            25,
            30,
            30
        )

        # ----------------------------------------------------
        # Header
        # ----------------------------------------------------

        header = QHBoxLayout()

        self.title_label = QLabel(
            "👥 Customers"
        )

        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 26px;
                font-weight: bold;
                color: #172033;
            }
        """)

        header.addWidget(
            self.title_label
        )

        header.addStretch()

        self.add_button = QPushButton(
            "➕ Add Customer"
        )

        self.add_button.clicked.connect(
            self.add_customer
        )

        header.addWidget(
            self.add_button
        )

        layout.addLayout(
            header
        )

        # ----------------------------------------------------
        # Search
        # ----------------------------------------------------

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "🔍 Search customers..."
        )

        self.search_input.textChanged.connect(
            self.search_customers
        )

        layout.addWidget(
            self.search_input
        )

        # ----------------------------------------------------
        # Table
        # ----------------------------------------------------

        self.table = QTableWidget()

        self.table.setColumnCount(
            6
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.setAlternatingRowColors(
            True
        )

        layout.addWidget(
            self.table
        )

        # ----------------------------------------------------
        # Actions
        # ----------------------------------------------------

        actions = QHBoxLayout()

        self.edit_button = QPushButton(
            "✏️ Edit"
        )

        self.delete_button = QPushButton(
            "🗑️ Delete"
        )

        self.refresh_button = QPushButton(
            "🔄 Refresh"
        )

        self.edit_button.clicked.connect(
            self.edit_customer
        )

        self.delete_button.clicked.connect(
            self.delete_customer
        )

        self.refresh_button.clicked.connect(
            self.load_customers
        )

        actions.addWidget(
            self.edit_button
        )

        actions.addWidget(
            self.delete_button
        )

        actions.addStretch()

        actions.addWidget(
            self.refresh_button
        )

        layout.addLayout(
            actions
        )

        self.apply_style()

    # ========================================================
    # Style
    # ========================================================

    def apply_style(self):

        self.setStyleSheet("""
            QWidget {
                background: #f3f6fa;
            }

            QLineEdit {

                background: white;

                border: 1px solid #d1d5db;

                border-radius: 9px;

                padding: 11px;

                font-size: 14px;
            }

            QLineEdit:focus {

                border: 2px solid #2563eb;
            }

            QTableWidget {

                background: white;

                border: 1px solid #e5e7eb;

                border-radius: 12px;

                gridline-color: #e5e7eb;

                alternate-background-color: #f8fafc;
            }

            QTableWidget::item {

                padding: 8px;
            }

            QTableWidget::item:selected {

                background: #dbeafe;

                color: #172033;
            }

            QHeaderView::section {

                background: #111827;

                color: white;

                padding: 10px;

                border: none;

                font-weight: bold;
            }

            QPushButton {

                background: #2563eb;

                color: white;

                border: none;

                border-radius: 8px;

                padding: 10px 16px;

                font-weight: bold;
            }

            QPushButton:hover {

                background: #1d4ed8;
            }
        """)

    # ========================================================
    # Database Connection
    # ========================================================

    def get_connection(self):

        connection = sqlite3.connect(
            DATABASE_FILE
        )

        connection.row_factory = sqlite3.Row

        return connection

    # ========================================================
    # Load
    # ========================================================

    def load_customers(self):

        # التأكد من وجود الأعمدة دائمًا
        create_database()

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                phone,
                email,
                address,
                created_at
            FROM customers
            ORDER BY id DESC
        """)

        customers = cursor.fetchall()

        connection.close()

        self.display_customers(
            customers
        )

    # ========================================================
    # Display
    # ========================================================

    def display_customers(
        self,
        customers
    ):

        self.table.setRowCount(
            0
        )

        headers = [
            "ID",
            "Name",
            "Phone",
            "Email",
            "Address",
            "Created At",
        ]

        self.table.setHorizontalHeaderLabels(
            headers
        )

        for customer in customers:

            row = (
                self.table.rowCount()
            )

            self.table.insertRow(
                row
            )

            values = [

                customer["id"],

                customer["name"],

                customer["phone"]
                or "",

                customer["email"]
                or "",

                customer["address"]
                or "",

                customer["created_at"]
                or "",
            ]

            for column, value in enumerate(
                values
            ):

                item = QTableWidgetItem(
                    str(value)
                )

                item.setTextAlignment(
                    Qt.AlignCenter
                )

                self.table.setItem(
                    row,
                    column,
                    item
                )

    # ========================================================
    # Search
    # ========================================================

    def search_customers(self):

        text = (
            self.search_input
            .text()
            .strip()
        )

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                phone,
                email,
                address,
                created_at
            FROM customers
            WHERE name LIKE ?
               OR phone LIKE ?
               OR email LIKE ?
               OR address LIKE ?
            ORDER BY id DESC
        """, (

            f"%{text}%",

            f"%{text}%",

            f"%{text}%",

            f"%{text}%",

        ))

        customers = cursor.fetchall()

        connection.close()

        self.display_customers(
            customers
        )

    # ========================================================
    # Add
    # ========================================================

    def add_customer(self):

        dialog = CustomerDialog(
            self
        )

        if dialog.exec() != QDialog.Accepted:

            return

        data = dialog.get_data()

        connection = self.get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute("""
                INSERT INTO customers (
                    name,
                    phone,
                    email,
                    address,
                    notes
                )
                VALUES (?, ?, ?, ?, ?)
            """, (

                data["name"],

                data["phone"],

                data["email"],

                data["address"],

                data["notes"],

            ))

            connection.commit()

        except sqlite3.Error as error:

            connection.rollback()

            QMessageBox.critical(
                self,
                "Database Error",
                str(error)
            )

            connection.close()

            return

        connection.close()

        QMessageBox.information(
            self,
            "Customers",
            "Customer added successfully."
        )

        self.load_customers()

    # ========================================================
    # Selected Customer
    # ========================================================

    def get_selected_customer_id(self):

        selected = (
            self.table
            .selectionModel()
            .selectedRows()
        )

        if not selected:

            return None

        row = selected[0].row()

        item = self.table.item(
            row,
            0
        )

        if not item:

            return None

        try:

            return int(
                item.text()
            )

        except ValueError:

            return None

    # ========================================================
    # Edit
    # ========================================================

    def edit_customer(self):

        customer_id = (
            self.get_selected_customer_id()
        )

        if customer_id is None:

            QMessageBox.information(
                self,
                "Select Customer",
                "Please select a customer first."
            )

            return

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM customers
            WHERE id = ?
        """, (
            customer_id,
        ))

        customer = cursor.fetchone()

        connection.close()

        if not customer:

            return

        dialog = CustomerDialog(
            self,
            customer
        )

        if dialog.exec() != QDialog.Accepted:

            return

        data = dialog.get_data()

        connection = self.get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute("""
                UPDATE customers
                SET
                    name = ?,
                    phone = ?,
                    email = ?,
                    address = ?,
                    notes = ?
                WHERE id = ?
            """, (

                data["name"],

                data["phone"],

                data["email"],

                data["address"],

                data["notes"],

                customer_id,

            ))

            connection.commit()

        except sqlite3.Error as error:

            connection.rollback()

            QMessageBox.critical(
                self,
                "Database Error",
                str(error)
            )

            connection.close()

            return

        connection.close()

        QMessageBox.information(
            self,
            "Customers",
            "Customer updated successfully."
        )

        self.load_customers()

    # ========================================================
    # Delete
    # ========================================================

    def delete_customer(self):

        customer_id = (
            self.get_selected_customer_id()
        )

        if customer_id is None:

            QMessageBox.information(
                self,
                "Select Customer",
                "Please select a customer first."
            )

            return

        answer = QMessageBox.question(
            self,
            "Delete Customer",
            "Are you sure you want to delete this customer?",
            QMessageBox.Yes |
            QMessageBox.No
        )

        if answer != QMessageBox.Yes:

            return

        connection = self.get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute("""
                DELETE FROM customers
                WHERE id = ?
            """, (
                customer_id,
            ))

            connection.commit()

        except sqlite3.IntegrityError:

            connection.rollback()

            QMessageBox.warning(
                self,
                "Delete Error",
                "This customer cannot be deleted."
            )

            connection.close()

            return

        except sqlite3.Error as error:

            connection.rollback()

            QMessageBox.critical(
                self,
                "Database Error",
                str(error)
            )

            connection.close()

            return

        connection.close()

        QMessageBox.information(
            self,
            "Customers",
            "Customer deleted successfully."
        )

        self.load_customers()

    # ========================================================
    # Language Refresh
    # ========================================================

    def refresh_language(self):

        self.load_customers()