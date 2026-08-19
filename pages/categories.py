# ============================================================
# pages/categories.py
# Smart Inventory Manager
# Categories Management
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
)

from utils.translations import tr


DATABASE_FILE = "inventory.db"


# ============================================================
# Database
# ============================================================

def create_database():

    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# Category Dialog
# ============================================================

class CategoryDialog(QDialog):

    def __init__(self, parent=None, category=None):

        super().__init__(parent)

        self.category = category

        self.setup_ui()

        if category:
            self.load_category()

        self.update_language()

    # ========================================================
    # UI
    # ========================================================

    def setup_ui(self):

        self.setMinimumWidth(450)

        layout = QVBoxLayout(self)

        self.title_label = QLabel()

        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)

        layout.addWidget(self.title_label)

        self.form = QFormLayout()

        self.name_input = QLineEdit()

        self.form.addRow(
            self.name_input
        )

        layout.addLayout(self.form)

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

        layout.addLayout(buttons)

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

            QLineEdit {
                background: white;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 9px;
                font-size: 14px;
            }

            QLineEdit:focus {
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
            tr("edit_category")
            if self.category
            else tr("add_category")
        )

        self.setWindowTitle(title)

        self.title_label.setText(title)

        label = self.form.itemAt(
            0,
            QFormLayout.LabelRole
        )

        if label and label.widget():

            label.widget().setText(
                tr("category_name") + ":"
            )

        self.cancel_button.setText(
            tr("cancel")
        )

        self.save_button.setText(
            tr("save")
        )

    # ========================================================
    # Load Category
    # ========================================================

    def load_category(self):

        self.name_input.setText(
            str(self.category["name"])
        )

    # ========================================================
    # Save
    # ========================================================

    def save(self):

        name = self.name_input.text().strip()

        if not name:

            QMessageBox.warning(
                self,
                tr("missing_data"),
                tr("enter_category_name")
            )

            return

        self.accept()

    # ========================================================
    # Get Data
    # ========================================================

    def get_data(self):

        return {
            "name": self.name_input.text().strip()
        }


# ============================================================
# Categories Page
# ============================================================

class CategoriesPage(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        create_database()

        self.setup_ui()

        self.update_language()

        self.load_categories()

    # ========================================================
    # UI
    # ========================================================

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            30,
            25,
            30,
            30
        )

        # Header
        header = QHBoxLayout()

        self.title_label = QLabel()

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

        self.add_button = QPushButton()

        self.add_button.clicked.connect(
            self.add_category
        )

        header.addWidget(
            self.add_button
        )

        layout.addLayout(header)

        # Search
        self.search_input = QLineEdit()

        self.search_input.textChanged.connect(
            self.search_categories
        )

        layout.addWidget(
            self.search_input
        )

        # Table
        self.table = QTableWidget()

        self.table.setColumnCount(3)

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

        self.edit_button = QPushButton()
        self.delete_button = QPushButton()
        self.refresh_button = QPushButton()

        self.edit_button.clicked.connect(
            self.edit_category
        )

        self.delete_button.clicked.connect(
            self.delete_category
        )

        self.refresh_button.clicked.connect(
            self.load_categories
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

        layout.addLayout(actions)

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
    # Language
    # ========================================================

    def update_language(self):

        self.title_label.setText(
            f"📂 {tr('categories')}"
        )

        self.add_button.setText(
            f"➕ {tr('add_category')}"
        )

        self.search_input.setPlaceholderText(
            f"🔍 {tr('category_search')}"
        )

        self.edit_button.setText(
            f"✏️ {tr('edit')}"
        )

        self.delete_button.setText(
            f"🗑️ {tr('delete')}"
        )

        self.refresh_button.setText(
            f"🔄 {tr('refresh')}"
        )

        headers = [
            tr("id"),
            tr("category_name"),
            tr("created_at"),
        ]

        self.table.setHorizontalHeaderLabels(
            headers
        )

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
    # Load Categories
    # ========================================================

    def load_categories(self):

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                created_at
            FROM categories
            ORDER BY id DESC
        """)

        categories = cursor.fetchall()

        connection.close()

        self.display_categories(
            categories
        )

    # ========================================================
    # Display
    # ========================================================

    def display_categories(self, categories):

        self.table.setRowCount(0)

        for category in categories:

            row = self.table.rowCount()

            self.table.insertRow(row)

            values = [
                category["id"],
                category["name"],
                category["created_at"],
            ]

            for column, value in enumerate(values):

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

    def search_categories(self):

        text = self.search_input.text().strip()

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                created_at
            FROM categories
            WHERE name LIKE ?
            ORDER BY id DESC
        """, (
            f"%{text}%",
        ))

        categories = cursor.fetchall()

        connection.close()

        self.display_categories(
            categories
        )

    # ========================================================
    # Add
    # ========================================================

    def add_category(self):

        dialog = CategoryDialog(self)

        if dialog.exec() != QDialog.Accepted:
            return

        data = dialog.get_data()

        connection = self.get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute("""
                INSERT INTO categories (name)
                VALUES (?)
            """, (
                data["name"],
            ))

            connection.commit()

            QMessageBox.information(
                self,
                tr("categories"),
                tr("category_added")
            )

        except sqlite3.IntegrityError:

            QMessageBox.warning(
                self,
                tr("duplicate_category"),
                tr("duplicate_category_message")
            )

        finally:

            connection.close()

        self.load_categories()

    # ========================================================
    # Selected Category
    # ========================================================

    def get_selected_category_id(self):

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

        return int(
            item.text()
        )

    # ========================================================
    # Edit
    # ========================================================

    def edit_category(self):

        category_id = (
            self.get_selected_category_id()
        )

        if category_id is None:

            QMessageBox.information(
                self,
                tr("select_category"),
                tr("select_category_message")
            )

            return

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM categories
            WHERE id = ?
        """, (
            category_id,
        ))

        category = cursor.fetchone()

        connection.close()

        if not category:
            return

        dialog = CategoryDialog(
            self,
            category
        )

        if dialog.exec() != QDialog.Accepted:
            return

        data = dialog.get_data()

        connection = self.get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute("""
                UPDATE categories
                SET name = ?
                WHERE id = ?
            """, (
                data["name"],
                category_id,
            ))

            connection.commit()

            QMessageBox.information(
                self,
                tr("categories"),
                tr("category_updated")
            )

        except sqlite3.IntegrityError:

            QMessageBox.warning(
                self,
                tr("duplicate_category"),
                tr("duplicate_category_message")
            )

        finally:

            connection.close()

        self.load_categories()

    # ========================================================
    # Delete
    # ========================================================

    def delete_category(self):

        category_id = (
            self.get_selected_category_id()
        )

        if category_id is None:

            QMessageBox.information(
                self,
                tr("select_category"),
                tr("select_category_message")
            )

            return

        answer = QMessageBox.question(
            self,
            tr("delete_category"),
            tr("delete_category_question"),
            QMessageBox.Yes |
            QMessageBox.No
        )

        if answer != QMessageBox.Yes:
            return

        connection = self.get_connection()

        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM categories
            WHERE id = ?
        """, (
            category_id,
        ))

        connection.commit()

        connection.close()

        QMessageBox.information(
            self,
            tr("categories"),
            tr("category_deleted")
        )

        self.load_categories()

    # ========================================================
    # Language Change
    # ========================================================

    def refresh_language(self):

        self.update_language()

        self.load_categories()