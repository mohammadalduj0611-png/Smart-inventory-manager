# ============================================================
# pages/suppliers.py
# Smart Inventory Manager
# Suppliers Management
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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            address TEXT,
            company TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # إصلاح قاعدة البيانات القديمة
    cursor.execute("""
        PRAGMA table_info(suppliers)
    """)

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    if "phone" not in columns:

        cursor.execute("""
            ALTER TABLE suppliers
            ADD COLUMN phone TEXT
        """)

    if "email" not in columns:

        cursor.execute("""
            ALTER TABLE suppliers
            ADD COLUMN email TEXT
        """)

    if "address" not in columns:

        cursor.execute("""
            ALTER TABLE suppliers
            ADD COLUMN address TEXT
        """)

    if "company" not in columns:

        cursor.execute("""
            ALTER TABLE suppliers
            ADD COLUMN company TEXT
        """)

    if "notes" not in columns:

        cursor.execute("""
            ALTER TABLE suppliers
            ADD COLUMN notes TEXT
        """)

    if "created_at" not in columns:

        cursor.execute("""
            ALTER TABLE suppliers
            ADD COLUMN created_at TIMESTAMP
        """)

        cursor.execute("""
            UPDATE suppliers
            SET created_at = CURRENT_TIMESTAMP
            WHERE created_at IS NULL
        """)

    connection.commit()

    connection.close()


# ============================================================
# Supplier Dialog
# ============================================================

class SupplierDialog(QDialog):

    def __init__(
        self,
        parent=None,
        supplier=None
    ):

        super().__init__(parent)

        self.supplier = supplier

        self.setup_ui()

        if supplier:

            self.load_supplier()

        self.update_language()

    # ========================================================
    # UI
    # ========================================================

    def setup_ui(self):

        self.setMinimumWidth(
            540
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

        self.name_input = QLineEdit()
        self.company_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()

        self.notes_input = QTextEdit()

        self.notes_input.setMaximumHeight(
            100
        )

        self.form.addRow(
            self.name_input
        )

        self.form.addRow(
            self.company_input
        )

        self.form.addRow(
            self.phone_input
        )

        self.form.addRow(
            self.email_input
        )

        self.form.addRow(
            self.address_input
        )

        self.form.addRow(
            self.notes_input
        )

        layout.addLayout(
            self.form
        )

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
            "Edit Supplier"
            if self.supplier
            else "Add Supplier"
        )

        self.setWindowTitle(
            title
        )

        self.title_label.setText(
            title
        )

        labels = [
            "Supplier Name:",
            "Company:",
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
    # Load Supplier
    # ========================================================

    def load_supplier(self):

        self.name_input.setText(
            str(
                self.supplier["name"]
                or ""
            )
        )

        self.company_input.setText(
            str(
                self.supplier["company"]
                or ""
            )
        )

        self.phone_input.setText(
            str(
                self.supplier["phone"]
                or ""
            )
        )

        self.email_input.setText(
            str(
                self.supplier["email"]
                or ""
            )
        )

        self.address_input.setText(
            str(
                self.supplier["address"]
                or ""
            )
        )

        self.notes_input.setPlainText(
            str(
                self.supplier["notes"]
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
                "Please enter supplier name."
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

            "company":
                self.company_input
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
# Suppliers Page
# ============================================================

class SuppliersPage(QWidget):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(parent)

        create_database()

        self.setup_ui()

        self.load_suppliers()

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

        header = QHBoxLayout()

        self.title_label = QLabel(
            "🏢 Suppliers"
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
            "➕ Add Supplier"
        )

        self.add_button.clicked.connect(
            self.add_supplier
        )

        header.addWidget(
            self.add_button
        )

        layout.addLayout(
            header
        )

        # Search
        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "🔍 Search suppliers..."
        )

        self.search_input.textChanged.connect(
            self.search_suppliers
        )

        layout.addWidget(
            self.search_input
        )

        # Table
        self.table = QTableWidget()

        self.table.setColumnCount(
            7
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

        # Actions
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
            self.edit_supplier
        )

        self.delete_button.clicked.connect(
            self.delete_supplier
        )

        self.refresh_button.clicked.connect(
            self.load_suppliers
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
    # Load Suppliers
    # ========================================================

    def load_suppliers(self):

        create_database()

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                company,
                phone,
                email,
                address,
                created_at
            FROM suppliers
            ORDER BY id DESC
        """)

        suppliers = cursor.fetchall()

        connection.close()

        self.display_suppliers(
            suppliers
        )

    # ========================================================
    # Display
    # ========================================================

    def display_suppliers(
        self,
        suppliers
    ):

        self.table.setRowCount(
            0
        )

        headers = [
            "ID",
            "Name",
            "Company",
            "Phone",
            "Email",
            "Address",
            "Created At",
        ]

        self.table.setHorizontalHeaderLabels(
            headers
        )

        for supplier in suppliers:

            row = (
                self.table.rowCount()
            )

            self.table.insertRow(
                row
            )

            values = [

                supplier["id"],

                supplier["name"],

                supplier["company"]
                or "",

                supplier["phone"]
                or "",

                supplier["email"]
                or "",

                supplier["address"]
                or "",

                supplier["created_at"]
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

    def search_suppliers(self):

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
                company,
                phone,
                email,
                address,
                created_at
            FROM suppliers
            WHERE name LIKE ?
               OR company LIKE ?
               OR phone LIKE ?
               OR email LIKE ?
               OR address LIKE ?
            ORDER BY id DESC
        """, (

            f"%{text}%",

            f"%{text}%",

            f"%{text}%",

            f"%{text}%",

            f"%{text}%",

        ))

        suppliers = cursor.fetchall()

        connection.close()

        self.display_suppliers(
            suppliers
        )

    # ========================================================
    # Add
    # ========================================================

    def add_supplier(self):

        dialog = SupplierDialog(
            self
        )

        if dialog.exec() != QDialog.Accepted:

            return

        data = dialog.get_data()

        connection = self.get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute("""
                INSERT INTO suppliers (
                    name,
                    company,
                    phone,
                    email,
                    address,
                    notes
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (

                data["name"],

                data["company"],

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
            "Suppliers",
            "Supplier added successfully."
        )

        self.load_suppliers()

    # ========================================================
    # Selected Supplier
    # ========================================================

    def get_selected_supplier_id(self):

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

    def edit_supplier(self):

        supplier_id = (
            self.get_selected_supplier_id()
        )

        if supplier_id is None:

            QMessageBox.information(
                self,
                "Select Supplier",
                "Please select a supplier first."
            )

            return

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM suppliers
            WHERE id = ?
        """, (
            supplier_id,
        ))

        supplier = cursor.fetchone()

        connection.close()

        if not supplier:

            return

        dialog = SupplierDialog(
            self,
            supplier
        )

        if dialog.exec() != QDialog.Accepted:

            return

        data = dialog.get_data()

        connection = self.get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute("""
                UPDATE suppliers
                SET
                    name = ?,
                    company = ?,
                    phone = ?,
                    email = ?,
                    address = ?,
                    notes = ?
                WHERE id = ?
            """, (

                data["name"],

                data["company"],

                data["phone"],

                data["email"],

                data["address"],

                data["notes"],

                supplier_id,

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
            "Suppliers",
            "Supplier updated successfully."
        )

        self.load_suppliers()

    # ========================================================
    # Delete
    # ========================================================

    def delete_supplier(self):

        supplier_id = (
            self.get_selected_supplier_id()
        )

        if supplier_id is None:

            QMessageBox.information(
                self,
                "Select Supplier",
                "Please select a supplier first."
            )

            return

        answer = QMessageBox.question(
            self,
            "Delete Supplier",
            "Are you sure you want to delete this supplier?",
            QMessageBox.Yes |
            QMessageBox.No
        )

        if answer != QMessageBox.Yes:

            return

        connection = self.get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute("""
                DELETE FROM suppliers
                WHERE id = ?
            """, (
                supplier_id,
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
            "Suppliers",
            "Supplier deleted successfully."
        )

        self.load_suppliers()

    # ========================================================
    # Language Refresh
    # ========================================================

    def refresh_language(self):

        self.load_suppliers()