# ============================================================
# pages/purchases.py
# Smart Inventory Manager
# Purchases Management
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
    QComboBox,
    QDoubleSpinBox,
    QSpinBox,
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
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            supplier_id INTEGER,
            quantity INTEGER NOT NULL DEFAULT 1,
            purchase_price REAL NOT NULL DEFAULT 0,
            total REAL NOT NULL DEFAULT 0,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products(id),
            FOREIGN KEY(supplier_id) REFERENCES suppliers(id)
        )
    """)

    # ========================================================
    # إصلاح قاعدة البيانات القديمة
    # ========================================================

    cursor.execute("""
        PRAGMA table_info(purchases)
    """)

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    if "product_id" not in columns:

        cursor.execute("""
            ALTER TABLE purchases
            ADD COLUMN product_id INTEGER
        """)

    if "supplier_id" not in columns:

        cursor.execute("""
            ALTER TABLE purchases
            ADD COLUMN supplier_id INTEGER
        """)

    if "quantity" not in columns:

        cursor.execute("""
            ALTER TABLE purchases
            ADD COLUMN quantity INTEGER NOT NULL DEFAULT 1
        """)

    if "purchase_price" not in columns:

        cursor.execute("""
            ALTER TABLE purchases
            ADD COLUMN purchase_price REAL NOT NULL DEFAULT 0
        """)

    if "total" not in columns:

        cursor.execute("""
            ALTER TABLE purchases
            ADD COLUMN total REAL NOT NULL DEFAULT 0
        """)

    if "date" not in columns:

        cursor.execute("""
            ALTER TABLE purchases
            ADD COLUMN date TIMESTAMP
        """)

        cursor.execute("""
            UPDATE purchases
            SET date = CURRENT_TIMESTAMP
            WHERE date IS NULL
        """)

    connection.commit()

    connection.close()


# ============================================================
# Purchase Dialog
# ============================================================

class PurchaseDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(parent)

        self.purchase_data = None

        self.setup_ui()

        self.load_products()

        self.load_suppliers()

        self.calculate_total()

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

        self.title_label = QLabel(
            "➕ Add Purchase"
        )

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

        # Product
        self.product_combo = QComboBox()

        self.form.addRow(
            "Product:",
            self.product_combo
        )

        # Supplier
        self.supplier_combo = QComboBox()

        self.form.addRow(
            "Supplier:",
            self.supplier_combo
        )

        # Quantity
        self.quantity_input = QSpinBox()

        self.quantity_input.setMinimum(
            1
        )

        self.quantity_input.setMaximum(
            1000000
        )

        self.form.addRow(
            "Quantity:",
            self.quantity_input
        )

        # Purchase Price
        self.price_input = QDoubleSpinBox()

        self.price_input.setMinimum(
            0
        )

        self.price_input.setMaximum(
            999999999
        )

        self.price_input.setDecimals(
            2
        )

        self.form.addRow(
            "Purchase Price:",
            self.price_input
        )

        # Total
        self.total_label = QLabel(
            "0.00"
        )

        self.total_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2563eb;
            }
        """)

        self.form.addRow(
            "Total:",
            self.total_label
        )

        layout.addLayout(
            self.form
        )

        # Buttons
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

        self.quantity_input.valueChanged.connect(
            self.calculate_total
        )

        self.price_input.valueChanged.connect(
            self.calculate_total
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

            QComboBox,
            QSpinBox,
            QDoubleSpinBox {

                background: white;

                border: 1px solid #d1d5db;

                border-radius: 8px;

                padding: 9px;

                font-size: 14px;
            }

            QComboBox:focus,
            QSpinBox:focus,
            QDoubleSpinBox:focus {

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
    # Load Products
    # ========================================================

    def load_products(self):

        self.product_combo.clear()

        connection = sqlite3.connect(
            DATABASE_FILE
        )

        cursor = connection.cursor()

        try:

            cursor.execute("""
                SELECT id, name
                FROM products
                ORDER BY name
            """)

            products = cursor.fetchall()

            for product_id, name in products:

                self.product_combo.addItem(
                    str(name),
                    product_id
                )

        except sqlite3.Error:

            pass

        connection.close()

    # ========================================================
    # Load Suppliers
    # ========================================================

    def load_suppliers(self):

        self.supplier_combo.clear()

        self.supplier_combo.addItem(
            "No Supplier",
            None
        )

        connection = sqlite3.connect(
            DATABASE_FILE
        )

        cursor = connection.cursor()

        try:

            cursor.execute("""
                SELECT id, name
                FROM suppliers
                ORDER BY name
            """)

            suppliers = cursor.fetchall()

            for supplier_id, name in suppliers:

                self.supplier_combo.addItem(
                    str(name),
                    supplier_id
                )

        except sqlite3.Error:

            pass

        connection.close()

    # ========================================================
    # Calculate Total
    # ========================================================

    def calculate_total(self):

        quantity = (
            self.quantity_input
            .value()
        )

        price = (
            self.price_input
            .value()
        )

        total = quantity * price

        self.total_label.setText(
            f"{total:,.2f}"
        )

    # ========================================================
    # Save
    # ========================================================

    def save(self):

        product_id = (
            self.product_combo
            .currentData()
        )

        if product_id is None:

            QMessageBox.warning(
                self,
                "Missing Data",
                "Please select a product."
            )

            return

        quantity = (
            self.quantity_input
            .value()
        )

        price = (
            self.price_input
            .value()
        )

        if price <= 0:

            QMessageBox.warning(
                self,
                "Invalid Price",
                "Please enter a purchase price greater than zero."
            )

            return

        total = (
            quantity *
            price
        )

        self.purchase_data = {

            "product_id":
                product_id,

            "supplier_id":
                self.supplier_combo
                .currentData(),

            "quantity":
                quantity,

            "purchase_price":
                price,

            "total":
                total,
        }

        self.accept()

    # ========================================================
    # Get Data
    # ========================================================

    def get_data(self):

        return self.purchase_data


# ============================================================
# Purchases Page
# ============================================================

class PurchasesPage(QWidget):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        create_database()

        self.setup_ui()

        self.load_purchases()

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

        # Header
        header = QHBoxLayout()

        self.title_label = QLabel(
            "🛒 Purchases"
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
            "➕ Add Purchase"
        )

        self.add_button.clicked.connect(
            self.add_purchase
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
            "🔍 Search purchases..."
        )

        self.search_input.textChanged.connect(
            self.search_purchases
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

        self.delete_button = QPushButton(
            "🗑️ Delete"
        )

        self.refresh_button = QPushButton(
            "🔄 Refresh"
        )

        self.delete_button.clicked.connect(
            self.delete_purchase
        )

        self.refresh_button.clicked.connect(
            self.load_purchases
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

        # Total
        self.total_label = QLabel(
            "Total Purchases: 0.00"
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
    # Connection
    # ========================================================

    def get_connection(self):

        connection = sqlite3.connect(
            DATABASE_FILE
        )

        connection.row_factory = sqlite3.Row

        return connection

    # ========================================================
    # Load Purchases
    # ========================================================

    def load_purchases(self):

        create_database()

        connection = self.get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute("""
                SELECT
                    purchases.id,
                    products.name AS product_name,
                    suppliers.name AS supplier_name,
                    purchases.quantity,
                    purchases.purchase_price,
                    purchases.total,
                    purchases.date
                FROM purchases
                LEFT JOIN products
                    ON purchases.product_id = products.id
                LEFT JOIN suppliers
                    ON purchases.supplier_id = suppliers.id
                ORDER BY purchases.id DESC
            """)

            purchases = cursor.fetchall()

        except sqlite3.Error as error:

            connection.close()

            QMessageBox.critical(
                self,
                "Database Error",
                str(error)
            )

            return

        connection.close()

        self.display_purchases(
            purchases
        )

    # ========================================================
    # Display
    # ========================================================

    def display_purchases(
        self,
        purchases
    ):

        self.table.setRowCount(
            0
        )

        headers = [
            "ID",
            "Product",
            "Supplier",
            "Quantity",
            "Purchase Price",
            "Total",
            "Date",
        ]

        self.table.setHorizontalHeaderLabels(
            headers
        )

        total_purchases = 0

        for purchase in purchases:

            row = (
                self.table.rowCount()
            )

            self.table.insertRow(
                row
            )

            purchase_price = float(
                purchase["purchase_price"]
                or 0
            )

            total = float(
                purchase["total"]
                or 0
            )

            total_purchases += total

            values = [

                purchase["id"],

                purchase["product_name"]
                or "",

                purchase["supplier_name"]
                or "",

                purchase["quantity"],

                f"{purchase_price:,.2f}",

                f"{total:,.2f}",

                purchase["date"]
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

        self.total_label.setText(
            f"Total Purchases: {total_purchases:,.2f}"
        )

    # ========================================================
    # Search
    # ========================================================

    def search_purchases(self):

        text = (
            self.search_input
            .text()
            .strip()
        )

        connection = self.get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute("""
                SELECT
                    purchases.id,
                    products.name AS product_name,
                    suppliers.name AS supplier_name,
                    purchases.quantity,
                    purchases.purchase_price,
                    purchases.total,
                    purchases.date
                FROM purchases
                LEFT JOIN products
                    ON purchases.product_id = products.id
                LEFT JOIN suppliers
                    ON purchases.supplier_id = suppliers.id
                WHERE products.name LIKE ?
                   OR suppliers.name LIKE ?
                   OR CAST(purchases.quantity AS TEXT) LIKE ?
                   OR CAST(purchases.purchase_price AS TEXT) LIKE ?
                   OR CAST(purchases.total AS TEXT) LIKE ?
                   OR purchases.date LIKE ?
                ORDER BY purchases.id DESC
            """, (

                f"%{text}%",

                f"%{text}%",

                f"%{text}%",

                f"%{text}%",

                f"%{text}%",

                f"%{text}%",

            ))

            purchases = cursor.fetchall()

        except sqlite3.Error as error:

            connection.close()

            QMessageBox.critical(
                self,
                "Database Error",
                str(error)
            )

            return

        connection.close()

        self.display_purchases(
            purchases
        )

    # ========================================================
    # Add Purchase
    # ========================================================

    def add_purchase(self):

        dialog = PurchaseDialog(
            self
        )

        if (
            dialog.exec()
            != QDialog.Accepted
        ):

            return

        data = dialog.get_data()

        if not data:

            return

        connection = self.get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute("""
                INSERT INTO purchases (
                    product_id,
                    supplier_id,
                    quantity,
                    purchase_price,
                    total
                )
                VALUES (?, ?, ?, ?, ?)
            """, (

                data["product_id"],

                data["supplier_id"],

                data["quantity"],

                data["purchase_price"],

                data["total"],

            ))

            # =================================================
            # تحديث المخزون
            # =================================================

            cursor.execute("""
                UPDATE products
                SET quantity = quantity + ?
                WHERE id = ?
            """, (

                data["quantity"],

                data["product_id"],

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
            "Purchases",
            "Purchase added successfully."
        )

        self.load_purchases()

    # ========================================================
    # Selected Purchase
    # ========================================================

    def get_selected_purchase_id(self):

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
    # Delete Purchase
    # ========================================================

    def delete_purchase(self):

        purchase_id = (
            self.get_selected_purchase_id()
        )

        if purchase_id is None:

            QMessageBox.information(
                self,
                "Select Purchase",
                "Please select a purchase first."
            )

            return

        answer = QMessageBox.question(
            self,
            "Delete Purchase",
            "Are you sure you want to delete this purchase?",
            QMessageBox.Yes |
            QMessageBox.No
        )

        if answer != QMessageBox.Yes:

            return

        connection = self.get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute("""
                SELECT
                    product_id,
                    quantity
                FROM purchases
                WHERE id = ?
            """, (
                purchase_id,
            ))

            purchase = cursor.fetchone()

            if not purchase:

                connection.close()

                return

            cursor.execute("""
                DELETE FROM purchases
                WHERE id = ?
            """, (
                purchase_id,
            ))

            # =================================================
            # إعادة الكمية من المخزون
            # =================================================

            cursor.execute("""
                UPDATE products
                SET quantity = quantity - ?
                WHERE id = ?
            """, (

                purchase["quantity"],

                purchase["product_id"],

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
            "Purchases",
            "Purchase deleted successfully."
        )

        self.load_purchases()

    # ========================================================
    # Language Refresh
    # ========================================================

    def refresh_language(self):

        self.load_purchases()