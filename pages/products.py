
# ============================================================
# pages/products.py
# Smart Inventory Manager
# Products Management
# ============================================================

import json
import os
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
    QSpinBox,
    QDoubleSpinBox,
    QTextEdit,
)

from translations import tr


DATABASE_FILE = "inventory.db"
SETTINGS_FILE = "settings.json"


# ============================================================
# Language
# ============================================================

def get_language():

    if not os.path.exists(SETTINGS_FILE):
        return "English"

    try:

        with open(
            SETTINGS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            settings = json.load(file)

            language = settings.get(
                "language",
                "English"
            )

            if language not in (
                "English",
                "Arabic"
            ):

                return "English"

            return language

    except (
        json.JSONDecodeError,
        OSError
    ):

        return "English"


# ============================================================
# Database
# ============================================================

def create_database():

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            code TEXT NOT NULL UNIQUE,

            name TEXT NOT NULL,

            purchase_price REAL DEFAULT 0,

            selling_price REAL DEFAULT 0,

            quantity INTEGER DEFAULT 0,

            min_quantity INTEGER DEFAULT 0,

            description TEXT DEFAULT '',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    connection.commit()

    connection.close()


# ============================================================
# Product Dialog
# ============================================================

class ProductDialog(QDialog):

    def __init__(
        self,
        parent=None,
        product=None
    ):

        super().__init__(parent)

        self.product = product

        self.language = get_language()

        self.setup_ui()

        if product:
            self.load_product()

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
                margin-bottom: 10px;
            }
        """)

        layout.addWidget(
            self.title_label
        )

        self.form = QFormLayout()

        # ----------------------------------------------------
        # Code
        # ----------------------------------------------------

        self.code_input = QLineEdit()

        self.code_label = QLabel()

        self.form.addRow(
            self.code_label,
            self.code_input
        )

        # ----------------------------------------------------
        # Name
        # ----------------------------------------------------

        self.name_input = QLineEdit()

        self.name_label = QLabel()

        self.form.addRow(
            self.name_label,
            self.name_input
        )

        # ----------------------------------------------------
        # Purchase Price
        # ----------------------------------------------------

        self.purchase_price_input = QDoubleSpinBox()

        self.purchase_price_input.setRange(
            0,
            999999999
        )

        self.purchase_price_input.setDecimals(
            2
        )

        self.purchase_price_label = QLabel()

        self.form.addRow(
            self.purchase_price_label,
            self.purchase_price_input
        )

        # ----------------------------------------------------
        # Selling Price
        # ----------------------------------------------------

        self.selling_price_input = QDoubleSpinBox()

        self.selling_price_input.setRange(
            0,
            999999999
        )

        self.selling_price_input.setDecimals(
            2
        )

        self.selling_price_label = QLabel()

        self.form.addRow(
            self.selling_price_label,
            self.selling_price_input
        )

        # ----------------------------------------------------
        # Quantity
        # ----------------------------------------------------

        self.quantity_input = QSpinBox()

        self.quantity_input.setRange(
            0,
            999999999
        )

        self.quantity_label = QLabel()

        self.form.addRow(
            self.quantity_label,
            self.quantity_input
        )

        # ----------------------------------------------------
        # Minimum Quantity
        # ----------------------------------------------------

        self.min_quantity_input = QSpinBox()

        self.min_quantity_input.setRange(
            0,
            999999999
        )

        self.min_quantity_label = QLabel()

        self.form.addRow(
            self.min_quantity_label,
            self.min_quantity_input
        )

        # ----------------------------------------------------
        # Description
        # ----------------------------------------------------

        self.description_input = QTextEdit()

        self.description_input.setMaximumHeight(
            100
        )

        self.description_label = QLabel()

        self.form.addRow(
            self.description_label,
            self.description_input
        )

        layout.addLayout(
            self.form
        )

        # ----------------------------------------------------
        # Buttons
        # ----------------------------------------------------

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
            QSpinBox,
            QDoubleSpinBox,
            QTextEdit {

                background: white;

                border: 1px solid #d1d5db;

                border-radius: 8px;

                padding: 8px;

                font-size: 14px;
            }

            QLineEdit:focus,
            QSpinBox:focus,
            QDoubleSpinBox:focus,
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

        self.language = get_language()

        language = self.language

        if self.product:

            title = tr(
                "edit_product",
                language
            )

        else:

            title = tr(
                "add_product",
                language
            )

        self.setWindowTitle(
            title
        )

        self.title_label.setText(
            title
        )

        self.code_label.setText(
            tr(
                "product_code",
                language
            ) + ":"
        )

        self.name_label.setText(
            tr(
                "product_name",
                language
            ) + ":"
        )

        self.purchase_price_label.setText(
            tr(
                "purchase_price",
                language
            ) + ":"
        )

        self.selling_price_label.setText(
            tr(
                "selling_price",
                language
            ) + ":"
        )

        self.quantity_label.setText(
            tr(
                "quantity",
                language
            ) + ":"
        )

        self.min_quantity_label.setText(
            tr(
                "minimum_stock",
                language
            ) + ":"
        )

        self.description_label.setText(
            tr(
                "description",
                language
            ) + ":"
        )

        self.cancel_button.setText(
            tr(
                "cancel",
                language
            )
        )

        self.save_button.setText(
            tr(
                "save",
                language
            )
        )

        if language == "Arabic":

            self.setLayoutDirection(
                Qt.RightToLeft
            )

        else:

            self.setLayoutDirection(
                Qt.LeftToRight
            )

    # ========================================================
    # Load Product
    # ========================================================

    def load_product(self):

        self.code_input.setText(
            str(
                self.product["code"]
            )
        )

        self.name_input.setText(
            str(
                self.product["name"]
            )
        )

        self.purchase_price_input.setValue(
            float(
                self.product["purchase_price"]
            )
        )

        self.selling_price_input.setValue(
            float(
                self.product["selling_price"]
            )
        )

        self.quantity_input.setValue(
            int(
                self.product["quantity"]
            )
        )

        self.min_quantity_input.setValue(
            int(
                self.product["min_quantity"]
            )
        )

        self.description_input.setPlainText(
            self.product["description"] or ""
        )

    # ========================================================
    # Save
    # ========================================================

    def save(self):

        code = self.code_input.text().strip()

        name = self.name_input.text().strip()

        language = get_language()

        if not code:

            QMessageBox.warning(
                self,
                tr(
                    "missing_data",
                    language
                ),
                tr(
                    "enter_product_code",
                    language
                )
            )

            return

        if not name:

            QMessageBox.warning(
                self,
                tr(
                    "missing_data",
                    language
                ),
                tr(
                    "enter_product_name",
                    language
                )
            )

            return

        self.accept()

    # ========================================================
    # Get Data
    # ========================================================

    def get_data(self):

        return {

            "code":
                self.code_input.text().strip(),

            "name":
                self.name_input.text().strip(),

            "purchase_price":
                self.purchase_price_input.value(),

            "selling_price":
                self.selling_price_input.value(),

            "quantity":
                self.quantity_input.value(),

            "min_quantity":
                self.min_quantity_input.value(),

            "description":
                self.description_input
                .toPlainText()
                .strip(),
        }


# ============================================================
# Products Page
# ============================================================

class ProductsPage(QWidget):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(parent)

        create_database()

        self.language = get_language()

        self.setup_ui()

        self.update_language()

        self.load_products()

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
            self.add_product
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

        self.search_input.textChanged.connect(
            self.search_products
        )

        layout.addWidget(
            self.search_input
        )

        # ----------------------------------------------------
        # Table
        # ----------------------------------------------------

        self.table = QTableWidget()

        self.table.setColumnCount(
            8
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

        self.edit_button = QPushButton()

        self.delete_button = QPushButton()

        self.refresh_button = QPushButton()

        self.edit_button.clicked.connect(
            self.edit_product
        )

        self.delete_button.clicked.connect(
            self.delete_product
        )

        self.refresh_button.clicked.connect(
            self.load_products
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
    # Language
    # ========================================================

    def update_language(self):

        self.language = get_language()

        language = self.language

        self.title_label.setText(
            "📦 " + tr(
                "products",
                language
            )
        )

        self.add_button.setText(
            "➕ " + tr(
                "add_product",
                language
            )
        )

        self.search_input.setPlaceholderText(
            "🔍 " + tr(
                "product_search",
                language
            )
        )

        self.edit_button.setText(
            "✏️ " + tr(
                "edit",
                language
            )
        )

        self.delete_button.setText(
            "🗑️ " + tr(
                "delete",
                language
            )
        )

        self.refresh_button.setText(
            "🔄 " + tr(
                "refresh",
                language
            )
        )

        headers = [

            tr(
                "id",
                language
            ),

            tr(
                "product_code",
                language
            ),

            tr(
                "product_name",
                language
            ),

            tr(
                "purchase_price",
                language
            ),

            tr(
                "selling_price",
                language
            ),

            tr(
                "quantity",
                language
            ),

            tr(
                "minimum_stock",
                language
            ),

            tr(
                "status",
                language
            ),
        ]

        self.table.setHorizontalHeaderLabels(
            headers
        )

        if language == "Arabic":

            self.setLayoutDirection(
                Qt.RightToLeft
            )

        else:

            self.setLayoutDirection(
                Qt.LeftToRight
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
    # Load
    # ========================================================

    def load_products(self):

        connection = None

        try:

            connection = self.get_connection()

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    id,
                    code,
                    name,
                    purchase_price,
                    selling_price,
                    quantity,
                    min_quantity
                FROM products
                ORDER BY id DESC
            """)

            products = cursor.fetchall()

            self.display_products(
                products
            )

        except sqlite3.Error as error:

            print(
                "Products database error:",
                error
            )

        finally:

            if connection:

                connection.close()

    # ========================================================
    # Display
    # ========================================================

    def display_products(
        self,
        products
    ):

        self.table.setRowCount(
            0
        )

        language = get_language()

        for product in products:

            row = self.table.rowCount()

            self.table.insertRow(
                row
            )

            values = [

                product["id"],

                product["code"],

                product["name"],

                f"{product['purchase_price']:.2f}",

                f"{product['selling_price']:.2f}",

                product["quantity"],

                product["min_quantity"],
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

            if (
                product["quantity"]
                <= product["min_quantity"]
            ):

                status = (
                    "⚠ " +
                    tr(
                        "low_stock_status",
                        language
                    )
                )

            else:

                status = (
                    "✓ " +
                    tr(
                        "in_stock",
                        language
                    )
                )

            status_item = QTableWidgetItem(
                status
            )

            status_item.setTextAlignment(
                Qt.AlignCenter
            )

            self.table.setItem(
                row,
                7,
                status_item
            )

    # ========================================================
    # Search
    # ========================================================

    def search_products(self):

        text = self.search_input.text().strip()

        connection = None

        try:

            connection = self.get_connection()

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    id,
                    code,
                    name,
                    purchase_price,
                    selling_price,
                    quantity,
                    min_quantity
                FROM products
                WHERE code LIKE ?
                   OR name LIKE ?
                ORDER BY id DESC
            """, (
                f"%{text}%",
                f"%{text}%"
            ))

            products = cursor.fetchall()

            self.display_products(
                products
            )

        except sqlite3.Error as error:

            print(
                "Products search error:",
                error
            )

        finally:

            if connection:

                connection.close()

    # ========================================================
    # Add
    # ========================================================

    def add_product(self):

        dialog = ProductDialog(
            self
        )

        if dialog.exec() != QDialog.Accepted:

            return

        data = dialog.get_data()

        connection = None

        try:

            connection = self.get_connection()

            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO products (
                    code,
                    name,
                    purchase_price,
                    selling_price,
                    quantity,
                    min_quantity,
                    description
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (

                data["code"],

                data["name"],

                data["purchase_price"],

                data["selling_price"],

                data["quantity"],

                data["min_quantity"],

                data["description"],
            ))

            connection.commit()

            language = get_language()

            QMessageBox.information(
                self,
                tr(
                    "products",
                    language
                ),
                tr(
                    "product_added",
                    language
                )
            )

        except sqlite3.IntegrityError:

            language = get_language()

            QMessageBox.warning(
                self,
                tr(
                    "duplicate_code",
                    language
                ),
                tr(
                    "duplicate_code_message",
                    language
                )
            )

        finally:

            if connection:

                connection.close()

        self.load_products()

    # ========================================================
    # Selected Product
    # ========================================================

    def get_selected_product_id(self):

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

    def edit_product(self):

        product_id = (
            self.get_selected_product_id()
        )

        language = get_language()

        if product_id is None:

            QMessageBox.information(
                self,
                tr(
                    "select_product",
                    language
                ),
                tr(
                    "select_product_message",
                    language
                )
            )

            return

        connection = None

        try:

            connection = self.get_connection()

            cursor = connection.cursor()

            cursor.execute("""
                SELECT *
                FROM products
                WHERE id = ?
            """, (
                product_id,
            ))

            product = cursor.fetchone()

        finally:

            if connection:

                connection.close()

        if not product:

            return

        dialog = ProductDialog(
            self,
            product
        )

        if dialog.exec() != QDialog.Accepted:

            return

        data = dialog.get_data()

        connection = None

        try:

            connection = self.get_connection()

            cursor = connection.cursor()

            cursor.execute("""
                UPDATE products
                SET
                    code = ?,
                    name = ?,
                    purchase_price = ?,
                    selling_price = ?,
                    quantity = ?,
                    min_quantity = ?,
                    description = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (

                data["code"],

                data["name"],

                data["purchase_price"],

                data["selling_price"],

                data["quantity"],

                data["min_quantity"],

                data["description"],

                product_id,
            ))

            connection.commit()

            QMessageBox.information(
                self,
                tr(
                    "products",
                    language
                ),
                tr(
                    "product_updated",
                    language
                )
            )

        except sqlite3.IntegrityError:

            QMessageBox.warning(
                self,
                tr(
                    "duplicate_code",
                    language
                ),
                tr(
                    "duplicate_code_message",
                    language
                )
            )

        finally:

            if connection:

                connection.close()

        self.load_products()

    # ========================================================
    # Delete
    # ========================================================

    def delete_product(self):

        product_id = (
            self.get_selected_product_id()
        )

        language = get_language()

        if product_id is None:

            QMessageBox.information(
                self,
                tr(
                    "select_product",
                    language
                ),
                tr(
                    "select_product_message",
                    language
                )
            )

            return

        answer = QMessageBox.question(
            self,
            tr(
                "delete_product",
                language
            ),
            tr(
                "delete_product_question",
                language
            ),
            QMessageBox.Yes |
            QMessageBox.No
        )

        if answer != QMessageBox.Yes:

            return

        connection = None

        try:

            connection = self.get_connection()

            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM products
                WHERE id = ?
            """, (
                product_id,
            ))

            connection.commit()

        except sqlite3.Error as error:

            print(
                "Delete product error:",
                error
            )

            return

        finally:

            if connection:

                connection.close()

        QMessageBox.information(
            self,
            tr(
                "products",
                language
            ),
            tr(
                "product_deleted",
                language
            )
        )

        self.load_products()

    # ========================================================
    # Language Change
    # ========================================================

    def refresh_language(self):

        self.language = get_language()

        self.update_language()

        self.load_products()
