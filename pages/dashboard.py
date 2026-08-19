# ============================================================
# pages/dashboard.py
# Smart Inventory Manager
# Dashboard
# ============================================================

import json
import os
import sqlite3

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QFrame,
)

from translations import tr


DATABASE_FILE = "inventory.db"
SETTINGS_FILE = "settings.json"


# ============================================================
# Settings
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

def get_connection():

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# Safe Count
# ============================================================

def safe_count(
    cursor,
    table_name
):

    try:

        cursor.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        )

        return cursor.fetchone()[0]

    except sqlite3.Error:

        return 0


# ============================================================
# Stat Card
# ============================================================

class StatCard(QFrame):

    def __init__(
        self,
        title,
        value,
        icon,
        parent=None
    ):

        super().__init__(parent)

        self.setObjectName(
            "stat_card"
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            20,
            18,
            20,
            18
        )

        self.icon_label = QLabel(
            icon
        )

        self.icon_label.setAlignment(
            Qt.AlignCenter
        )

        self.icon_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                background: transparent;
                border: none;
            }
        """)

        layout.addWidget(
            self.icon_label
        )

        self.value_label = QLabel(
            str(value)
        )

        self.value_label.setAlignment(
            Qt.AlignCenter
        )

        self.value_label.setStyleSheet("""
            QLabel {
                font-size: 30px;
                font-weight: bold;
                color: #172033;
                background: transparent;
                border: none;
            }
        """)

        layout.addWidget(
            self.value_label
        )

        self.title_label = QLabel(
            title
        )

        self.title_label.setAlignment(
            Qt.AlignCenter
        )

        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #64748b;
                font-weight: bold;
                background: transparent;
                border: none;
            }
        """)

        layout.addWidget(
            self.title_label
        )

    # ========================================================
    # Update Value
    # ========================================================

    def set_value(
        self,
        value
    ):

        self.value_label.setText(
            str(value)
        )

    # ========================================================
    # Update Title
    # ========================================================

    def set_title(
        self,
        title
    ):

        self.title_label.setText(
            title
        )


# ============================================================
# Dashboard Page
# ============================================================

class DashboardPage(QWidget):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(parent)

        self.language = get_language()

        self.setup_ui()

        self.update_language()

        self.load_statistics()

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
            20
        )

        # ====================================================
        # Header
        # ====================================================

        header = QHBoxLayout()

        self.title_label = QLabel()

        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #172033;
                background: transparent;
            }
        """)

        header.addWidget(
            self.title_label
        )

        header.addStretch()

        self.refresh_button = QPushButton()

        self.refresh_button.clicked.connect(
            self.load_statistics
        )

        header.addWidget(
            self.refresh_button
        )

        layout.addLayout(
            header
        )

        # ====================================================
        # Welcome
        # ====================================================

        self.welcome_frame = QFrame()

        self.welcome_frame.setObjectName(
            "welcome_frame"
        )

        welcome_layout = QVBoxLayout(
            self.welcome_frame
        )

        welcome_layout.setContentsMargins(
            25,
            20,
            25,
            20
        )

        self.welcome_title = QLabel()

        self.welcome_title.setStyleSheet("""
            QLabel {
                font-size: 21px;
                font-weight: bold;
                color: white;
                background: transparent;
            }
        """)

        welcome_layout.addWidget(
            self.welcome_title
        )

        self.welcome_text = QLabel()

        self.welcome_text.setWordWrap(
            True
        )

        self.welcome_text.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #dbeafe;
                background: transparent;
            }
        """)

        welcome_layout.addWidget(
            self.welcome_text
        )

        layout.addWidget(
            self.welcome_frame
        )

        # ====================================================
        # Statistics
        # ====================================================

        cards_layout = QGridLayout()

        cards_layout.setSpacing(
            18
        )

        self.products_card = StatCard(
            "",
            0,
            "📦"
        )

        self.categories_card = StatCard(
            "",
            0,
            "📂"
        )

        self.customers_card = StatCard(
            "",
            0,
            "👥"
        )

        self.suppliers_card = StatCard(
            "",
            0,
            "🚚"
        )

        self.low_stock_card = StatCard(
            "",
            0,
            "⚠️"
        )

        self.sales_card = StatCard(
            "",
            0,
            "💰"
        )

        cards_layout.addWidget(
            self.products_card,
            0,
            0
        )

        cards_layout.addWidget(
            self.categories_card,
            0,
            1
        )

        cards_layout.addWidget(
            self.customers_card,
            0,
            2
        )

        cards_layout.addWidget(
            self.suppliers_card,
            1,
            0
        )

        cards_layout.addWidget(
            self.low_stock_card,
            1,
            1
        )

        cards_layout.addWidget(
            self.sales_card,
            1,
            2
        )

        layout.addLayout(
            cards_layout
        )

        # ====================================================
        # Quick Actions
        # ====================================================

        self.actions_frame = QFrame()

        actions_layout = QVBoxLayout(
            self.actions_frame
        )

        actions_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        self.actions_title = QLabel()

        self.actions_title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #172033;
                background: transparent;
            }
        """)

        actions_layout.addWidget(
            self.actions_title
        )

        buttons_layout = QHBoxLayout()

        self.products_button = QPushButton()
        self.categories_button = QPushButton()
        self.customers_button = QPushButton()
        self.suppliers_button = QPushButton()

        buttons_layout.addWidget(
            self.products_button
        )

        buttons_layout.addWidget(
            self.categories_button
        )

        buttons_layout.addWidget(
            self.customers_button
        )

        buttons_layout.addWidget(
            self.suppliers_button
        )

        actions_layout.addLayout(
            buttons_layout
        )

        layout.addWidget(
            self.actions_frame
        )

        layout.addStretch()

        self.apply_style()

    # ========================================================
    # Style
    # ========================================================

    def apply_style(self):

        self.setStyleSheet("""
            QWidget {
                background: #f3f6fa;
            }

            QFrame#stat_card {
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 14px;
            }

            QFrame#stat_card:hover {
                border: 1px solid #2563eb;
            }

            QFrame#welcome_frame {
                background: #2563eb;
                border-radius: 14px;
            }

            QFrame#actions_frame {
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 14px;
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

            QPushButton:pressed {
                background: #1e40af;
            }
        """)

    # ========================================================
    # Language
    # ========================================================

    def update_language(self):

        self.language = get_language()

        language = self.language

        self.title_label.setText(
            "📊 " + tr(
                "dashboard",
                language
            )
        )

        self.refresh_button.setText(
            "🔄 " + tr(
                "refresh",
                language
            )
        )

        self.welcome_title.setText(
            tr(
                "welcome",
                language
            )
        )

        self.welcome_text.setText(
            tr(
                "dashboard_welcome",
                language
            )
        )

        self.products_card.set_title(
            tr(
                "products",
                language
            )
        )

        self.categories_card.set_title(
            tr(
                "categories",
                language
            )
        )

        self.customers_card.set_title(
            tr(
                "customers",
                language
            )
        )

        self.suppliers_card.set_title(
            tr(
                "suppliers",
                language
            )
        )

        self.low_stock_card.set_title(
            tr(
                "low_stock",
                language
            )
        )

        self.sales_card.set_title(
            tr(
                "sales",
                language
            )
        )

        self.actions_title.setText(
            tr(
                "quick_actions",
                language
            )
        )

        self.products_button.setText(
            "📦 " + tr(
                "products",
                language
            )
        )

        self.categories_button.setText(
            "📂 " + tr(
                "categories",
                language
            )
        )

        self.customers_button.setText(
            "👥 " + tr(
                "customers",
                language
            )
        )

        self.suppliers_button.setText(
            "🚚 " + tr(
                "suppliers",
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
    # Statistics
    # ========================================================

    def load_statistics(self):

        connection = None

        try:

            connection = get_connection()

            cursor = connection.cursor()

            # ------------------------------------------------
            # Products
            # ------------------------------------------------

            products_count = safe_count(
                cursor,
                "products"
            )

            # ------------------------------------------------
            # Categories
            # ------------------------------------------------

            categories_count = safe_count(
                cursor,
                "categories"
            )

            # ------------------------------------------------
            # Customers
            # ------------------------------------------------

            customers_count = safe_count(
                cursor,
                "customers"
            )

            # ------------------------------------------------
            # Suppliers
            # ------------------------------------------------

            suppliers_count = safe_count(
                cursor,
                "suppliers"
            )

            # ------------------------------------------------
            # Low Stock
            # ------------------------------------------------

            try:

                cursor.execute("""
                    SELECT COUNT(*)
                    FROM products
                    WHERE quantity <= min_quantity
                """)

                low_stock_count = (
                    cursor.fetchone()[0]
                )

            except sqlite3.Error:

                low_stock_count = 0

            # ------------------------------------------------
            # Sales
            # ------------------------------------------------

            sales_count = safe_count(
                cursor,
                "sales"
            )

            # ------------------------------------------------
            # Update Cards
            # ------------------------------------------------

            self.products_card.set_value(
                products_count
            )

            self.categories_card.set_value(
                categories_count
            )

            self.customers_card.set_value(
                customers_count
            )

            self.suppliers_card.set_value(
                suppliers_count
            )

            self.low_stock_card.set_value(
                low_stock_count
            )

            self.sales_card.set_value(
                sales_count
            )

        except sqlite3.Error as error:

            print(
                "Dashboard database error:",
                error
            )

            self.products_card.set_value(0)
            self.categories_card.set_value(0)
            self.customers_card.set_value(0)
            self.suppliers_card.set_value(0)
            self.low_stock_card.set_value(0)
            self.sales_card.set_value(0)

        finally:

            if connection:

                connection.close()

    # ========================================================
    # Language Change
    # ========================================================

    def refresh_language(self):

        self.language = get_language()

        self.update_language()

        self.load_statistics()

