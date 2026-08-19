# ============================================================
# pages/expenses.py
# Smart Inventory Manager
# Expenses Management
# ============================================================

import os
import sqlite3

from PySide6.QtCore import Qt, QDate
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
    QDoubleSpinBox,
    QTextEdit,
    QDateEdit,
    QComboBox,
)


# ============================================================
# Database Path
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATABASE_FILE = os.path.join(
    BASE_DIR,
    "inventory.db"
)


# ============================================================
# Database
# ============================================================

def get_connection():

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    connection.row_factory = sqlite3.Row

    return connection


def create_database():

    connection = get_connection()

    cursor = connection.cursor()

    # Create expenses table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT,
            amount REAL NOT NULL DEFAULT 0,
            expense_date TEXT NOT NULL,
            payment_method TEXT DEFAULT 'Cash',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # --------------------------------------------------------
    # Check existing columns
    # --------------------------------------------------------

    cursor.execute(
        "PRAGMA table_info(expenses)"
    )

    columns = [
        row["name"]
        for row in cursor.fetchall()
    ]

    # --------------------------------------------------------
    # Add missing columns
    # --------------------------------------------------------

    if "category" not in columns:

        cursor.execute("""
            ALTER TABLE expenses
            ADD COLUMN category TEXT
        """)

    if "amount" not in columns:

        cursor.execute("""
            ALTER TABLE expenses
            ADD COLUMN amount REAL NOT NULL DEFAULT 0
        """)

    if "expense_date" not in columns:

        cursor.execute("""
            ALTER TABLE expenses
            ADD COLUMN expense_date TEXT
        """)

    if "payment_method" not in columns:

        cursor.execute("""
            ALTER TABLE expenses
            ADD COLUMN payment_method TEXT DEFAULT 'Cash'
        """)

    if "notes" not in columns:

        cursor.execute("""
            ALTER TABLE expenses
            ADD COLUMN notes TEXT
        """)

    if "created_at" not in columns:

        cursor.execute("""
            ALTER TABLE expenses
            ADD COLUMN created_at TIMESTAMP
        """)

    connection.commit()

    connection.close()


# ============================================================
# Expense Dialog
# ============================================================

class ExpenseDialog(QDialog):

    def __init__(
        self,
        parent=None,
        expense=None
    ):

        super().__init__(parent)

        self.expense = expense

        self.setup_ui()

        if expense:

            self.load_expense()

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

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        self.title_input = QLineEdit()

        self.form.addRow(
            "Expense Title:",
            self.title_input
        )

        # ----------------------------------------------------
        # Category
        # ----------------------------------------------------

        self.category_input = QComboBox()

        self.category_input.setEditable(
            True
        )

        self.category_input.addItems([
            "Rent",
            "Electricity",
            "Water",
            "Internet",
            "Transport",
            "Salary",
            "Maintenance",
            "Marketing",
            "Other",
        ])

        self.form.addRow(
            "Category:",
            self.category_input
        )

        # ----------------------------------------------------
        # Amount
        # ----------------------------------------------------

        self.amount_input = QDoubleSpinBox()

        self.amount_input.setRange(
            0,
            999999999
        )

        self.amount_input.setDecimals(
            2
        )

        self.amount_input.setSingleStep(
            1
        )

        self.form.addRow(
            "Amount:",
            self.amount_input
        )

        # ----------------------------------------------------
        # Date
        # ----------------------------------------------------

        self.date_input = QDateEdit()

        self.date_input.setCalendarPopup(
            True
        )

        self.date_input.setDate(
            QDate.currentDate()
        )

        self.form.addRow(
            "Date:",
            self.date_input
        )

        # ----------------------------------------------------
        # Payment
        # ----------------------------------------------------

        self.payment_input = QComboBox()

        self.payment_input.addItems([
            "Cash",
            "Card",
            "Bank Transfer",
            "Other",
        ])

        self.form.addRow(
            "Payment Method:",
            self.payment_input
        )

        # ----------------------------------------------------
        # Notes
        # ----------------------------------------------------

        self.notes_input = QTextEdit()

        self.notes_input.setMaximumHeight(
            100
        )

        self.form.addRow(
            "Notes:",
            self.notes_input
        )

        layout.addLayout(
            self.form
        )

        # ----------------------------------------------------
        # Buttons
        # ----------------------------------------------------

        buttons = QHBoxLayout()

        buttons.addStretch()

        self.cancel_button = QPushButton(
            "Cancel"
        )

        self.save_button = QPushButton(
            "Save"
        )

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
            QComboBox,
            QDoubleSpinBox,
            QDateEdit,
            QTextEdit {
                background: white;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }

            QLineEdit:focus,
            QComboBox:focus,
            QDoubleSpinBox:focus,
            QDateEdit:focus,
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
            "Edit Expense"
            if self.expense
            else "Add Expense"
        )

        self.setWindowTitle(
            title
        )

        self.title_label.setText(
            title
        )

        self.cancel_button.setText(
            "Cancel"
        )

        self.save_button.setText(
            "Save"
        )

    # ========================================================
    # Load Expense
    # ========================================================

    def load_expense(self):

        self.title_input.setText(
            str(
                self.expense["title"]
                or ""
            )
        )

        category = str(
            self.expense["category"]
            or ""
        )

        index = (
            self.category_input
            .findText(category)
        )

        if index >= 0:

            self.category_input.setCurrentIndex(
                index
            )

        else:

            self.category_input.setCurrentText(
                category
            )

        self.amount_input.setValue(
            float(
                self.expense["amount"]
                or 0
            )
        )

        date_value = QDate.fromString(
            str(
                self.expense["expense_date"]
                or ""
            ),
            "yyyy-MM-dd"
        )

        if date_value.isValid():

            self.date_input.setDate(
                date_value
            )

        payment = str(
            self.expense["payment_method"]
            or "Cash"
        )

        payment_index = (
            self.payment_input
            .findText(payment)
        )

        if payment_index >= 0:

            self.payment_input.setCurrentIndex(
                payment_index
            )

        self.notes_input.setPlainText(
            str(
                self.expense["notes"]
                or ""
            )
        )

    # ========================================================
    # Save
    # ========================================================

    def save(self):

        title = (
            self.title_input
            .text()
            .strip()
        )

        if not title:

            QMessageBox.warning(
                self,
                "Missing Data",
                "Please enter expense title."
            )

            return

        if self.amount_input.value() <= 0:

            QMessageBox.warning(
                self,
                "Invalid Amount",
                "Please enter an amount greater than zero."
            )

            return

        self.accept()

    # ========================================================
    # Get Data
    # ========================================================

    def get_data(self):

        return {

            "title":
                self.title_input
                .text()
                .strip(),

            "category":
                self.category_input
                .currentText()
                .strip(),

            "amount":
                self.amount_input
                .value(),

            "expense_date":
                self.date_input
                .date()
                .toString(
                    "yyyy-MM-dd"
                ),

            "payment_method":
                self.payment_input
                .currentText(),

            "notes":
                self.notes_input
                .toPlainText()
                .strip(),
        }


# ============================================================
# Expenses Page
# ============================================================

class ExpensesPage(QWidget):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        # Make sure database/table/columns exist
        create_database()

        self.setup_ui()

        self.load_expenses()

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

        layout.setSpacing(
            15
        )

        # ----------------------------------------------------
        # Header
        # ----------------------------------------------------

        header = QHBoxLayout()

        self.title_label = QLabel(
            "💸 Expenses"
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
            "➕ Add Expense"
        )

        self.add_button.clicked.connect(
            self.add_expense
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
            "🔍 Search expenses..."
        )

        self.search_input.textChanged.connect(
            self.search_expenses
        )

        layout.addWidget(
            self.search_input
        )

        # ----------------------------------------------------
        # Table
        # ----------------------------------------------------

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
            self.edit_expense
        )

        self.delete_button.clicked.connect(
            self.delete_expense
        )

        self.refresh_button.clicked.connect(
            self.load_expenses
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

        # ----------------------------------------------------
        # Total
        # ----------------------------------------------------

        self.total_label = QLabel(
            "Total Expenses: 0.00"
        )

        self.total_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #172033;
                padding-top: 10px;
            }
        """)

        layout.addWidget(
            self.total_label
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
    # Load Expenses
    # ========================================================

    def load_expenses(self):

        try:

            # Ensure database is ready
            create_database()

            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    id,
                    title,
                    category,
                    amount,
                    expense_date,
                    payment_method,
                    notes
                FROM expenses
                ORDER BY expense_date DESC, id DESC
            """)

            expenses = cursor.fetchall()

            connection.close()

            self.display_expenses(
                expenses
            )

        except sqlite3.Error as error:

            print(
                "Expenses database error:",
                error
            )

            QMessageBox.critical(
                self,
                "Database Error",
                f"Could not load expenses.\n\n{error}"
            )

    # ========================================================
    # Display
    # ========================================================

    def display_expenses(
        self,
        expenses
    ):

        self.table.setRowCount(
            0
        )

        headers = [
            "ID",
            "Title",
            "Category",
            "Amount",
            "Date",
            "Payment",
            "Notes",
        ]

        self.table.setHorizontalHeaderLabels(
            headers
        )

        total = 0

        for expense in expenses:

            row = self.table.rowCount()

            self.table.insertRow(
                row
            )

            amount = float(
                expense["amount"]
                or 0
            )

            total += amount

            values = [
                expense["id"],
                expense["title"],
                expense["category"] or "",
                f"{amount:.2f}",
                expense["expense_date"] or "",
                expense["payment_method"] or "",
                expense["notes"] or "",
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

        self.total_label.setText(
            f"Total Expenses: {total:.2f}"
        )

    # ========================================================
    # Search
    # ========================================================

    def search_expenses(self):

        text = (
            self.search_input
            .text()
            .strip()
        )

        try:

            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    id,
                    title,
                    category,
                    amount,
                    expense_date,
                    payment_method,
                    notes
                FROM expenses
                WHERE title LIKE ?
                   OR category LIKE ?
                   OR payment_method LIKE ?
                   OR notes LIKE ?
                ORDER BY expense_date DESC, id DESC
            """, (
                f"%{text}%",
                f"%{text}%",
                f"%{text}%",
                f"%{text}%",
            ))

            expenses = cursor.fetchall()

            connection.close()

            self.display_expenses(
                expenses
            )

        except sqlite3.Error as error:

            print(
                "Expense search error:",
                error
            )

    # ========================================================
    # Add Expense
    # ========================================================

    def add_expense(self):

        dialog = ExpenseDialog(
            self
        )

        if (
            dialog.exec()
            != QDialog.Accepted
        ):

            return

        data = dialog.get_data()

        try:

            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO expenses (
                    title,
                    category,
                    amount,
                    expense_date,
                    payment_method,
                    notes
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data["title"],
                data["category"],
                data["amount"],
                data["expense_date"],
                data["payment_method"],
                data["notes"],
            ))

            connection.commit()

            connection.close()

            QMessageBox.information(
                self,
                "Expenses",
                "Expense added successfully."
            )

            self.load_expenses()

        except sqlite3.Error as error:

            QMessageBox.critical(
                self,
                "Database Error",
                f"Could not add expense.\n\n{error}"
            )

    # ========================================================
    # Selected Expense
    # ========================================================

    def get_selected_expense_id(self):

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
    # Edit Expense
    # ========================================================

    def edit_expense(self):

        expense_id = (
            self.get_selected_expense_id()
        )

        if expense_id is None:

            QMessageBox.information(
                self,
                "Select Expense",
                "Please select an expense first."
            )

            return

        try:

            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute("""
                SELECT *
                FROM expenses
                WHERE id = ?
            """, (
                expense_id,
            ))

            expense = cursor.fetchone()

            connection.close()

        except sqlite3.Error as error:

            QMessageBox.critical(
                self,
                "Database Error",
                f"Could not read expense.\n\n{error}"
            )

            return

        if not expense:

            return

        dialog = ExpenseDialog(
            self,
            expense
        )

        if (
            dialog.exec()
            != QDialog.Accepted
        ):

            return

        data = dialog.get_data()

        try:

            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute("""
                UPDATE expenses
                SET
                    title = ?,
                    category = ?,
                    amount = ?,
                    expense_date = ?,
                    payment_method = ?,
                    notes = ?
                WHERE id = ?
            """, (
                data["title"],
                data["category"],
                data["amount"],
                data["expense_date"],
                data["payment_method"],
                data["notes"],
                expense_id,
            ))

            connection.commit()

            connection.close()

            QMessageBox.information(
                self,
                "Expenses",
                "Expense updated successfully."
            )

            self.load_expenses()

        except sqlite3.Error as error:

            QMessageBox.critical(
                self,
                "Database Error",
                f"Could not update expense.\n\n{error}"
            )

    # ========================================================
    # Delete Expense
    # ========================================================

    def delete_expense(self):

        expense_id = (
            self.get_selected_expense_id()
        )

        if expense_id is None:

            QMessageBox.information(
                self,
                "Select Expense",
                "Please select an expense first."
            )

            return

        answer = QMessageBox.question(
            self,
            "Delete Expense",
            "Are you sure you want to delete this expense?",
            QMessageBox.Yes |
            QMessageBox.No
        )

        if answer != QMessageBox.Yes:

            return

        try:

            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM expenses
                WHERE id = ?
            """, (
                expense_id,
            ))

            connection.commit()

            connection.close()

            QMessageBox.information(
                self,
                "Expenses",
                "Expense deleted successfully."
            )

            self.load_expenses()

        except sqlite3.Error as error:

            QMessageBox.critical(
                self,
                "Database Error",
                f"Could not delete expense.\n\n{error}"
            )

    # ========================================================
    # Language Refresh
    # ========================================================

    def refresh_language(self):

        self.load_expenses()