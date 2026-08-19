# ============================================================
# pages/sales.py
# Smart Inventory Manager
# Sales Management
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

def get_database_connection():

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    connection.row_factory = sqlite3.Row

    return connection


def create_database():

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    cursor = connection.cursor()

    # --------------------------------------------------------
    # Create sales table if it does not exist
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            customer_id INTEGER,
            quantity INTEGER NOT NULL DEFAULT 1,
            selling_price REAL NOT NULL DEFAULT 0,
            total REAL NOT NULL DEFAULT 0,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # --------------------------------------------------------
    # Check existing columns
    # --------------------------------------------------------

    cursor.execute("""
        PRAGMA table_info(sales)
    """)

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    # --------------------------------------------------------
    # Add missing columns automatically
    # --------------------------------------------------------

    if "product_id" not in columns:

        cursor.execute("""
            ALTER TABLE sales
            ADD COLUMN product_id INTEGER
        """)

    if "customer_id" not in columns:

        cursor.execute("""
            ALTER TABLE sales
            ADD COLUMN customer_id INTEGER
        """)

    if "quantity" not in columns:

        cursor.execute("""
            ALTER TABLE sales
            ADD COLUMN quantity INTEGER NOT NULL DEFAULT 1
        """)

    if "selling_price" not in columns:

        cursor.execute("""
            ALTER TABLE sales
            ADD COLUMN selling_price REAL NOT NULL DEFAULT 0
        """)

    if "total" not in columns:

        cursor.execute("""
            ALTER TABLE sales
            ADD COLUMN total REAL NOT NULL DEFAULT 0
        """)

    if "date" not in columns:

        cursor.execute("""
            ALTER TABLE sales
            ADD COLUMN date TIMESTAMP
        """)

        cursor.execute("""
            UPDATE sales
            SET date = CURRENT_TIMESTAMP
            WHERE date IS NULL
        """)

    connection.commit()

    connection.close()


# ============================================================
# Sale Dialog
# ============================================================

class SaleDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(parent)

        self.sale_data = None

        self.setup_ui()

        self.load_products()

        self.load_customers()

        self.product_combo.currentIndexChanged.connect(
            self.update_product_price
        )

        self.quantity_input.valueChanged.connect(
            self.calculate_total
        )

        self.price_input.valueChanged.connect(
            self.calculate_total
        )

        self.update_product_price()

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
            "➕ Add Sale"
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

        # Customer
        self.customer_combo = QComboBox()

        self.form.addRow(
            "Customer:",
            self.customer_combo
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

        # Selling Price
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
            "Selling Price:",
            self.price_input
        )

        # Total
        self.total_label = QLabel(
            "0.00"
        )

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
                SELECT
                    id,
                    name,
                    selling_price,
                    quantity
                FROM products
                ORDER BY name
            """)

            products = cursor.fetchall()

            for (
                product_id,
                name,
                selling_price,
                quantity
            ) in products:

                self.product_combo.addItem(
                    name,
                    {
                        "id": product_id,
                        "price": selling_price or 0,
                        "stock": quantity or 0,
                    }
                )

        except sqlite3.Error as error:

            QMessageBox.warning(
                self,
                "Database Error",
                str(error)
            )

        connection.close()

    # ========================================================
    # Load Customers
    # ========================================================

    def load_customers(self):

        self.customer_combo.clear()

        self.customer_combo.addItem(
            "No Customer",
            None
        )

        connection = sqlite3.connect(
            DATABASE_FILE
        )

        cursor = connection.cursor()

        try:

            cursor.execute("""
                SELECT
                    id,
                    name
                FROM customers
                ORDER BY name
            """)

            customers = cursor.fetchall()

            for customer_id, name in customers:

                self.customer_combo.addItem(
                    name,
                    customer_id
                )

        except sqlite3.Error as error:

            QMessageBox.warning(
                self,
                "Database Error",
                str(error)
            )

        connection.close()

    # ========================================================
    # Product Price
    # ========================================================

    def update_product_price(self):

        data = (
            self.product_combo
            .currentData()
        )

        if not data:

            self.price_input.setValue(
                0
            )

            self.quantity_input.setMaximum(
                1000000
            )

            self.calculate_total()

            return

        price = data.get(
            "price",
            0
        )

        stock = int(
            data.get(
                "stock",
                0
            )
        )

        self.price_input.setValue(
            float(price or 0)
        )

        self.quantity_input.setMaximum(
            max(
                1,
                stock
            )
        )

        self.calculate_total()

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

        data = (
            self.product_combo
            .currentData()
        )

        if not data:

            QMessageBox.warning(
                self,
                "Missing Data",
                "Please select a product."
            )

            return

        product_id = data["id"]

        stock = int(
            data.get(
                "stock",
                0
            )
        )

        quantity = (
            self.quantity_input
            .value()
        )

        if stock <= 0:

            QMessageBox.warning(
                self,
                "Out of Stock",
                "This product is out of stock."
            )

            return

        if quantity > stock:

            QMessageBox.warning(
                self,
                "Insufficient Stock",
                f"Available stock: {stock}"
            )

            return

        price = (
            self.price_input
            .value()
        )

        if price <= 0:

            QMessageBox.warning(
                self,
                "Invalid Price",
                "Please enter a selling price greater than zero."
            )

            return

        total = quantity * price

        self.sale_data = {

            "product_id":
                product_id,

            "customer_id":
                self.customer_combo
                .currentData(),

            "quantity":
                quantity,

            "selling_price":
                price,

            "total":
                total,

        }

        self.accept()

    # ========================================================
    # Get Data
    # ========================================================

    def get_data(self):

        return self.sale_data


# ============================================================
# Sales Page
# ============================================================

class SalesPage(QWidget):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        create_database()

        self.setup_ui()

        self.load_sales()

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
            "💰 Sales"
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
            "➕ Add Sale"
        )

        self.add_button.clicked.connect(
            self.add_sale
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
            "🔍 Search sales..."
        )

        self.search_input.textChanged.connect(
            self.search_sales
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
            self.delete_sale
        )

        self.refresh_button.clicked.connect(
            self.load_sales
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
    # Connection
    # ========================================================

    def get_connection(self):

        return get_database_connection()

    # ========================================================
    # Load Sales
    # ========================================================

    def load_sales(self):

        connection = self.get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute("""
                SELECT
                    sales.id,
                    products.name AS product_name,
                    customers.name AS customer_name,
                    sales.quantity,
                    sales.selling_price,
                    sales.total,
                    sales.date
                FROM sales
                LEFT JOIN products
                    ON sales.product_id = products.id
                LEFT JOIN customers
                    ON sales.customer_id = customers.id
                ORDER BY sales.id DESC
            """)

            sales = cursor.fetchall()

        except sqlite3.Error as error:

            connection.close()

            QMessageBox.critical(
                self,
                "Database Error",
                str(error)
            )

            return

        connection.close()

        self.display_sales(
            sales
        )

    # ========================================================
    # Display
    # ========================================================

    def display_sales(
        self,
        sales
    ):

        self.table.setRowCount(
            0
        )

        headers = [
            "ID",
            "Product",
            "Customer",
            "Quantity",
            "Selling Price",
            "Total",
            "Date",
        ]

        self.table.setHorizontalHeaderLabels(
            headers
        )

        for sale in sales:

            row = (
                self.table.rowCount()
            )

            self.table.insertRow(
                row
            )

            selling_price = float(
                sale["selling_price"] or 0
            )

            total = float(
                sale["total"] or 0
            )

            values = [

                sale["id"],

                sale["product_name"]
                or "",

                sale["customer_name"]
                or "",

                sale["quantity"]
                or 0,

                f"{selling_price:,.2f}",

                f"{total:,.2f}",

                sale["date"]
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

    def search_sales(self):

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
                    sales.id,
                    products.name AS product_name,
                    customers.name AS customer_name,
                    sales.quantity,
                    sales.selling_price,
                    sales.total,
                    sales.date
                FROM sales
                LEFT JOIN products
                    ON sales.product_id = products.id
                LEFT JOIN customers
                    ON sales.customer_id = customers.id
                WHERE products.name LIKE ?
                   OR customers.name LIKE ?
                ORDER BY sales.id DESC
            """, (

                f"%{text}%",

                f"%{text}%",

            ))

            sales = cursor.fetchall()

        except sqlite3.Error as error:

            connection.close()

            QMessageBox.critical(
                self,
                "Database Error",
                str(error)
            )

            return

        connection.close()

        self.display_sales(
            sales
        )

    # ========================================================
    # Add Sale
    # ========================================================

    def add_sale(self):

        dialog = SaleDialog(
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
                SELECT quantity
                FROM products
                WHERE id = ?
            """, (
                data["product_id"],
            ))

            product = cursor.fetchone()

            if not product:

                connection.close()

                QMessageBox.warning(
                    self,
                    "Error",
                    "Product not found."
                )

                return

            available_stock = int(
                product["quantity"] or 0
            )

            if available_stock < data["quantity"]:

                connection.close()

                QMessageBox.warning(
                    self,
                    "Insufficient Stock",
                    f"Available stock: {available_stock}"
                )

                return

            cursor.execute("""
                INSERT INTO sales (
                    product_id,
                    customer_id,
                    quantity,
                    selling_price,
                    total
                )
                VALUES (?, ?, ?, ?, ?)
            """, (

                data["product_id"],

                data["customer_id"],

                data["quantity"],

                data["selling_price"],

                data["total"],

            ))

            cursor.execute("""
                UPDATE products
                SET quantity = quantity - ?
                WHERE id = ?
            """, (

                data["quantity"],

                data["product_id"],

            ))

            connection.commit()

        except sqlite3.Error as error:

            connection.rollback()

            connection.close()

            QMessageBox.critical(
                self,
                "Database Error",
                str(error)
            )

            return

        connection.close()

        QMessageBox.information(
            self,
            "Sales",
            "Sale added successfully."
        )

        self.load_sales()

    # ========================================================
    # Selected Sale
    # ========================================================

    def get_selected_sale_id(self):

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
    # Delete Sale
    # ========================================================

    def delete_sale(self):

        sale_id = (
            self.get_selected_sale_id()
        )

        if sale_id is None:

            QMessageBox.information(
                self,
                "Select Sale",
                "Please select a sale first."
            )

            return

        answer = QMessageBox.question(
            self,
            "Delete Sale",
            "Are you sure you want to delete this sale?",
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
                FROM sales
                WHERE id = ?
            """, (
                sale_id,
            ))

            sale = cursor.fetchone()

            if not sale:

                connection.close()

                return

            cursor.execute("""
                DELETE FROM sales
                WHERE id = ?
            """, (
                sale_id,
            ))

            cursor.execute("""
                UPDATE products
                SET quantity = quantity + ?
                WHERE id = ?
            """, (

                sale["quantity"],

                sale["product_id"],

            ))

            connection.commit()

        except sqlite3.Error as error:

            connection.rollback()

            connection.close()

            QMessageBox.critical(
                self,
                "Database Error",
                str(error)
            )

            return

        connection.close()

        QMessageBox.information(
            self,
            "Sales",
            "Sale deleted successfully."
        )

        self.load_sales()

    # ========================================================
    # Language Refresh
    # ========================================================

    def refresh_language(self):

        self.load_sales()