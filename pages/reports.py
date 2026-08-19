# ============================================================
# pages/reports.py
# Smart Inventory Manager
# Reports & Statistics
# ============================================================

import sqlite3

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QComboBox,
    QMessageBox,
)


DATABASE_FILE = "inventory.db"


# ============================================================
# Reports Page
# ============================================================

class ReportsPage(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setup_ui()

        self.load_report()

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

        # ----------------------------------------------------
        # Header
        # ----------------------------------------------------

        header = QHBoxLayout()

        self.title_label = QLabel(
            "📊 Reports & Statistics"
        )

        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #172033;
            }
        """)

        header.addWidget(
            self.title_label
        )

        header.addStretch()

        self.period_combo = QComboBox()

        self.period_combo.addItems([
            "All Time",
            "Today",
            "This Month",
            "This Year",
        ])

        self.period_combo.currentIndexChanged.connect(
            self.load_report
        )

        header.addWidget(
            self.period_combo
        )

        self.refresh_button = QPushButton(
            "🔄 Refresh"
        )

        self.refresh_button.clicked.connect(
            self.load_report
        )

        header.addWidget(
            self.refresh_button
        )

        layout.addLayout(
            header
        )

        # ----------------------------------------------------
        # Statistics Cards
        # ----------------------------------------------------

        cards = QHBoxLayout()

        self.products_card = self.create_card(
            "📦 Products",
            "0"
        )

        self.stock_card = self.create_card(
            "📦 Stock Quantity",
            "0"
        )

        self.sales_card = self.create_card(
            "💰 Sales",
            "0.00"
        )

        self.purchases_card = self.create_card(
            "🛒 Purchases",
            "0.00"
        )

        self.expenses_card = self.create_card(
            "💸 Expenses",
            "0.00"
        )

        self.profit_card = self.create_card(
            "📈 Profit",
            "0.00"
        )

        cards.addWidget(
            self.products_card
        )

        cards.addWidget(
            self.stock_card
        )

        cards.addWidget(
            self.sales_card
        )

        cards.addWidget(
            self.purchases_card
        )

        cards.addWidget(
            self.expenses_card
        )

        cards.addWidget(
            self.profit_card
        )

        layout.addLayout(
            cards
        )

        # ----------------------------------------------------
        # Low Stock
        # ----------------------------------------------------

        self.low_stock_title = QLabel(
            "⚠ Low Stock Products"
        )

        self.low_stock_title.setStyleSheet("""
            QLabel {
                font-size: 21px;
                font-weight: bold;
                color: #172033;
                margin-top: 15px;
            }
        """)

        layout.addWidget(
            self.low_stock_title
        )

        self.low_stock_table = QTableWidget()

        self.low_stock_table.setColumnCount(
            5
        )

        self.low_stock_table.setHorizontalHeaderLabels([
            "ID",
            "Code",
            "Product",
            "Quantity",
            "Minimum",
        ])

        self.low_stock_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.low_stock_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.low_stock_table.setAlternatingRowColors(
            True
        )

        layout.addWidget(
            self.low_stock_table
        )

        # ----------------------------------------------------
        # Top Products
        # ----------------------------------------------------

        self.top_products_title = QLabel(
            "🏆 Products Overview"
        )

        self.top_products_title.setStyleSheet("""
            QLabel {
                font-size: 21px;
                font-weight: bold;
                color: #172033;
                margin-top: 15px;
            }
        """)

        layout.addWidget(
            self.top_products_title
        )

        self.products_table = QTableWidget()

        self.products_table.setColumnCount(
            5
        )

        self.products_table.setHorizontalHeaderLabels([
            "ID",
            "Code",
            "Product",
            "Purchase Price",
            "Selling Price",
        ])

        self.products_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.products_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.products_table.setAlternatingRowColors(
            True
        )

        layout.addWidget(
            self.products_table
        )

        self.apply_style()

    # ========================================================
    # Card
    # ========================================================

    def create_card(
        self,
        title,
        value
    ):

        widget = QWidget()

        widget.setMinimumHeight(
            100
        )

        widget.setStyleSheet("""
            QWidget {
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
            }

            QLabel {
                border: none;
                background: transparent;
            }
        """)

        card_layout = QVBoxLayout(
            widget
        )

        title_label = QLabel(
            title
        )

        title_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #6b7280;
                font-weight: bold;
            }
        """)

        value_label = QLabel(
            value
        )

        value_label.setStyleSheet("""
            QLabel {
                font-size: 23px;
                color: #172033;
                font-weight: bold;
            }
        """)

        card_layout.addWidget(
            title_label
        )

        card_layout.addWidget(
            value_label
        )

        widget.value_label = value_label

        return widget

    # ========================================================
    # Style
    # ========================================================

    def apply_style(self):

        self.setStyleSheet("""
            QWidget {
                background: #f3f6fa;
            }

            QComboBox {
                background: white;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 9px 12px;
                min-width: 120px;
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
    # Database
    # ========================================================

    def get_connection(self):

        connection = sqlite3.connect(
            DATABASE_FILE
        )

        connection.row_factory = sqlite3.Row

        return connection

    # ========================================================
    # Load Report
    # ========================================================

    def load_report(self):

        connection = self.get_connection()

        cursor = connection.cursor()

        # ----------------------------------------------------
        # Products
        # ----------------------------------------------------

        try:

            cursor.execute("""
                SELECT
                    COUNT(*) AS count,
                    COALESCE(SUM(quantity), 0) AS stock
                FROM products
            """)

            product_stats = cursor.fetchone()

            products_count = (
                product_stats["count"]
            )

            stock_quantity = (
                product_stats["stock"]
            )

        except sqlite3.Error:

            products_count = 0
            stock_quantity = 0

        # ----------------------------------------------------
        # Sales
        # ----------------------------------------------------

        sales_total = 0

        try:

            cursor.execute("""
                SELECT
                    COALESCE(
                        SUM(final_total),
                        0
                    ) AS total
                FROM sales
            """)

            row = cursor.fetchone()

            sales_total = float(
                row["total"] or 0
            )

        except sqlite3.Error:

            sales_total = 0

        # ----------------------------------------------------
        # Purchases
        # ----------------------------------------------------

        purchases_total = 0

        try:

            cursor.execute("""
                SELECT
                    COALESCE(
                        SUM(final_total),
                        0
                    ) AS total
                FROM purchases
            """)

            row = cursor.fetchone()

            purchases_total = float(
                row["total"] or 0
            )

        except sqlite3.Error:

            purchases_total = 0

        # ----------------------------------------------------
        # Expenses
        # ----------------------------------------------------

        expenses_total = 0

        try:

            cursor.execute("""
                SELECT
                    COALESCE(
                        SUM(amount),
                        0
                    ) AS total
                FROM expenses
            """)

            row = cursor.fetchone()

            expenses_total = float(
                row["total"] or 0
            )

        except sqlite3.Error:

            expenses_total = 0

        connection.close()

        # ----------------------------------------------------
        # Profit
        # ----------------------------------------------------

        profit = (
            sales_total
            - purchases_total
            - expenses_total
        )

        self.products_card.value_label.setText(
            str(products_count)
        )

        self.stock_card.value_label.setText(
            str(stock_quantity)
        )

        self.sales_card.value_label.setText(
            f"{sales_total:.2f}"
        )

        self.purchases_card.value_label.setText(
            f"{purchases_total:.2f}"
        )

        self.expenses_card.value_label.setText(
            f"{expenses_total:.2f}"
        )

        self.profit_card.value_label.setText(
            f"{profit:.2f}"
        )

        self.load_low_stock()

        self.load_products_table()

    # ========================================================
    # Low Stock
    # ========================================================

    def load_low_stock(self):

        connection = self.get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute("""
                SELECT
                    id,
                    code,
                    name,
                    quantity,
                    min_quantity
                FROM products
                WHERE quantity <= min_quantity
                ORDER BY quantity ASC
            """)

            products = cursor.fetchall()

        except sqlite3.Error:

            products = []

        connection.close()

        self.low_stock_table.setRowCount(
            0
        )

        for product in products:

            row = (
                self.low_stock_table.rowCount()
            )

            self.low_stock_table.insertRow(
                row
            )

            values = [
                product["id"],
                product["code"],
                product["name"],
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

                self.low_stock_table.setItem(
                    row,
                    column,
                    item
                )

    # ========================================================
    # Products Table
    # ========================================================

    def load_products_table(self):

        connection = self.get_connection()

        cursor = connection.cursor()

        try:

            cursor.execute("""
                SELECT
                    id,
                    code,
                    name,
                    purchase_price,
                    selling_price
                FROM products
                ORDER BY id DESC
                LIMIT 100
            """)

            products = cursor.fetchall()

        except sqlite3.Error:

            products = []

        connection.close()

        self.products_table.setRowCount(
            0
        )

        for product in products:

            row = (
                self.products_table.rowCount()
            )

            self.products_table.insertRow(
                row
            )

            values = [
                product["id"],
                product["code"],
                product["name"],
                f"{float(product['purchase_price'] or 0):.2f}",
                f"{float(product['selling_price'] or 0):.2f}",
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

                self.products_table.setItem(
                    row,
                    column,
                    item
                )

    # ========================================================
    # Language Refresh
    # ========================================================

    def refresh_language(self):

        self.load_report()