
# ============================================================
# main.py
# Smart Inventory Manager
# Main Application
# ============================================================

import sys
import sqlite3

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget,
    QMessageBox,
)

from translations import tr

from pages.dashboard import DashboardPage
from pages.products import ProductsPage
from pages.customers import CustomersPage
from pages.categories import CategoriesPage
from pages.purchases import PurchasesPage
from pages.suppliers import SuppliersPage
from pages.expenses import ExpensesPage
from pages.reports import ReportsPage
from pages.settings import SettingsPage


DATABASE_FILE = "inventory.db"


# ============================================================
# Sales
# ============================================================

try:
    from pages.sales import SalesPage
    SALES_AVAILABLE = True
except ImportError:
    SALES_AVAILABLE = False


# ============================================================
# Database Migration
# ============================================================

def column_exists(cursor, table_name, column_name):

    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    columns = cursor.fetchall()

    for column in columns:

        if column[1] == column_name:
            return True

    return False


def add_column_if_missing(
    cursor,
    table_name,
    column_name,
    column_definition
):

    if not column_exists(
        cursor,
        table_name,
        column_name
    ):

        cursor.execute(
            f"""
            ALTER TABLE {table_name}
            ADD COLUMN {column_name}
            {column_definition}
            """
        )


def initialize_database():

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    cursor = connection.cursor()

    try:

        # ====================================================
        # Products
        # ====================================================

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

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,

                updated_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ====================================================
        # Customers
        # ====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL
            )
        """)

        # ====================================================
        # Suppliers
        # ====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS suppliers (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL
            )
        """)

        # ====================================================
        # Purchases
        # ====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchases (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                product_id INTEGER NOT NULL,

                supplier_id INTEGER,

                quantity INTEGER NOT NULL DEFAULT 0,

                purchase_price REAL NOT NULL DEFAULT 0,

                total REAL NOT NULL DEFAULT 0,

                date TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ====================================================
        # Sales
        # ====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                product_id INTEGER NOT NULL,

                customer_id INTEGER,

                quantity INTEGER NOT NULL DEFAULT 0,

                selling_price REAL NOT NULL DEFAULT 0,

                total REAL NOT NULL DEFAULT 0,

                date TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ====================================================
        # Expenses
        # ====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                title TEXT,

                amount REAL DEFAULT 0,

                description TEXT DEFAULT '',

                date TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ====================================================
        # Fix old Products table
        # ====================================================

        add_column_if_missing(
            cursor,
            "products",
            "purchase_price",
            "REAL DEFAULT 0"
        )

        add_column_if_missing(
            cursor,
            "products",
            "selling_price",
            "REAL DEFAULT 0"
        )

        add_column_if_missing(
            cursor,
            "products",
            "quantity",
            "INTEGER DEFAULT 0"
        )

        add_column_if_missing(
            cursor,
            "products",
            "min_quantity",
            "INTEGER DEFAULT 0"
        )

        add_column_if_missing(
            cursor,
            "products",
            "description",
            "TEXT DEFAULT ''"
        )

        add_column_if_missing(
            cursor,
            "products",
            "created_at",
            "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        )

        add_column_if_missing(
            cursor,
            "products",
            "updated_at",
            "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        )

        # ====================================================
        # Fix old Purchases table
        # ====================================================

        add_column_if_missing(
            cursor,
            "purchases",
            "product_id",
            "INTEGER"
        )

        add_column_if_missing(
            cursor,
            "purchases",
            "supplier_id",
            "INTEGER"
        )

        add_column_if_missing(
            cursor,
            "purchases",
            "quantity",
            "INTEGER DEFAULT 0"
        )

        add_column_if_missing(
            cursor,
            "purchases",
            "purchase_price",
            "REAL DEFAULT 0"
        )

        add_column_if_missing(
            cursor,
            "purchases",
            "total",
            "REAL DEFAULT 0"
        )

        add_column_if_missing(
            cursor,
            "purchases",
            "date",
            "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        )

        # ====================================================
        # Fix old Sales table
        # ====================================================

        add_column_if_missing(
            cursor,
            "sales",
            "product_id",
            "INTEGER"
        )

        add_column_if_missing(
            cursor,
            "sales",
            "customer_id",
            "INTEGER"
        )

        add_column_if_missing(
            cursor,
            "sales",
            "quantity",
            "INTEGER DEFAULT 0"
        )

        add_column_if_missing(
            cursor,
            "sales",
            "selling_price",
            "REAL DEFAULT 0"
        )

        add_column_if_missing(
            cursor,
            "sales",
            "total",
            "REAL DEFAULT 0"
        )

        add_column_if_missing(
            cursor,
            "sales",
            "date",
            "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        )

        connection.commit()

    except sqlite3.Error as error:

        connection.rollback()

        print(
            "Database initialization error:",
            error
        )

        raise

    finally:

        connection.close()


# ============================================================
# Main Window
# ============================================================

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.language = "English"

        self.pages = {}

        self.buttons = {}

        self.setup_ui()

        self.show_page(
            "dashboard"
        )

        self.update_language(
            self.language
        )

    # ========================================================
    # UI
    # ========================================================

    def setup_ui(self):

        central = QWidget()

        self.setCentralWidget(
            central
        )

        main_layout = QHBoxLayout(
            central
        )

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        main_layout.setSpacing(
            0
        )

        # ====================================================
        # Sidebar
        # ====================================================

        self.sidebar = QWidget()

        self.sidebar.setFixedWidth(
            230
        )

        self.sidebar.setObjectName(
            "sidebar"
        )

        sidebar_layout = QVBoxLayout(
            self.sidebar
        )

        sidebar_layout.setContentsMargins(
            15,
            20,
            15,
            20
        )

        sidebar_layout.setSpacing(
            8
        )

        # ====================================================
        # Logo
        # ====================================================

        self.logo = QLabel(
            "📦 Smart Inventory"
        )

        self.logo.setObjectName(
            "logo"
        )

        sidebar_layout.addWidget(
            self.logo
        )

        self.subtitle = QLabel(
            "Inventory Manager"
        )

        self.subtitle.setObjectName(
            "subtitle"
        )

        sidebar_layout.addWidget(
            self.subtitle
        )

        sidebar_layout.addSpacing(
            20
        )

        # ====================================================
        # Navigation
        # ====================================================

        self.add_nav_button(
            sidebar_layout,
            "dashboard",
            "🏠 Dashboard"
        )

        self.add_nav_button(
            sidebar_layout,
            "products",
            "📦 Products"
        )

        self.add_nav_button(
            sidebar_layout,
            "categories",
            "🗂 Categories"
        )

        self.add_nav_button(
            sidebar_layout,
            "customers",
            "👥 Customers"
        )

        self.add_nav_button(
            sidebar_layout,
            "suppliers",
            "🏢 Suppliers"
        )

        self.add_nav_button(
            sidebar_layout,
            "purchases",
            "🛒 Purchases"
        )

        if SALES_AVAILABLE:

            self.add_nav_button(
                sidebar_layout,
                "sales",
                "💰 Sales"
            )

        self.add_nav_button(
            sidebar_layout,
            "expenses",
            "💸 Expenses"
        )

        self.add_nav_button(
            sidebar_layout,
            "reports",
            "📊 Reports"
        )

        self.add_nav_button(
            sidebar_layout,
            "settings",
            "⚙️ Settings"
        )

        sidebar_layout.addStretch()

        # ====================================================
        # Exit
        # ====================================================

        self.exit_button = QPushButton(
            "🚪 Exit"
        )

        self.exit_button.clicked.connect(
            self.close
        )

        self.exit_button.setObjectName(
            "exit_button"
        )

        sidebar_layout.addWidget(
            self.exit_button
        )

        # ====================================================
        # Content
        # ====================================================

        self.content = QWidget()

        self.content.setObjectName(
            "content"
        )

        content_layout = QVBoxLayout(
            self.content
        )

        content_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.stack = QStackedWidget()

        content_layout.addWidget(
            self.stack
        )

        main_layout.addWidget(
            self.sidebar
        )

        main_layout.addWidget(
            self.content
        )

        self.apply_style()

        self.create_pages()

    # ========================================================
    # Navigation Button
    # ========================================================

    def add_nav_button(
        self,
        layout,
        page_name,
        text
    ):

        button = QPushButton(
            text
        )

        button.setCheckable(
            True
        )

        button.setObjectName(
            "nav_button"
        )

        button.clicked.connect(
            lambda checked=False,
            name=page_name:
            self.show_page(name)
        )

        layout.addWidget(
            button
        )

        self.buttons[
            page_name
        ] = button

    # ========================================================
    # Create Pages
    # ========================================================

    def create_pages(self):

        self.add_page(
            "dashboard",
            DashboardPage()
        )

        self.add_page(
            "products",
            ProductsPage()
        )

        self.add_page(
            "categories",
            CategoriesPage()
        )

        self.add_page(
            "customers",
            CustomersPage()
        )

        self.add_page(
            "suppliers",
            SuppliersPage()
        )

        self.add_page(
            "purchases",
            PurchasesPage()
        )

        if SALES_AVAILABLE:

            self.add_page(
                "sales",
                SalesPage()
            )

        self.add_page(
            "expenses",
            ExpensesPage()
        )

        self.add_page(
            "reports",
            ReportsPage()
        )

        self.settings_page = SettingsPage()

        if hasattr(
            self.settings_page,
            "language_changed"
        ):

            self.settings_page.language_changed.connect(
                self.on_language_changed
            )

        self.add_page(
            "settings",
            self.settings_page
        )

    # ========================================================
    # Add Page
    # ========================================================

    def add_page(
        self,
        name,
        page
    ):

        self.pages[
            name
        ] = page

        self.stack.addWidget(
            page
        )

    # ========================================================
    # Show Page
    # ========================================================

    def show_page(
        self,
        name
    ):

        if name not in self.pages:

            QMessageBox.warning(
                self,
                tr(
                    "error",
                    self.language
                ),
                f"Page '{name}' is not available."
            )

            return

        page = self.pages[
            name
        ]

        self.stack.setCurrentWidget(
            page
        )

        for page_name, button in self.buttons.items():

            button.setChecked(
                page_name == name
            )

        self.refresh_all_pages()

    # ========================================================
    # Refresh Pages
    # ========================================================

    def refresh_all_pages(self):

        for page in self.pages.values():

            if hasattr(
                page,
                "refresh_language"
            ):

                try:

                    page.refresh_language()

                except Exception as error:

                    print(
                        "Language refresh error:",
                        error
                    )

    # ========================================================
    # Language Changed
    # ========================================================

    def on_language_changed(
        self,
        language
    ):

        if language not in (
            "English",
            "Arabic"
        ):

            language = "English"

        self.language = language

        self.update_language(
            language
        )

    # ========================================================
    # Update Language
    # ========================================================

    def update_language(
        self,
        language
    ):

        self.language = language

        self.setWindowTitle(
            tr(
                "app_name",
                language
            )
        )

        self.logo.setText(
            "📦 " + tr(
                "app_name",
                language
            )
        )

        self.subtitle.setText(
            "Inventory Manager"
            if language == "English"
            else "إدارة المخزون"
        )

        navigation = {

            "dashboard":
                "🏠 " + tr(
                    "dashboard",
                    language
                ),

            "products":
                "📦 " + tr(
                    "products",
                    language
                ),

            "categories":
                "🗂 " + tr(
                    "categories",
                    language
                ),

            "customers":
                "👥 " + tr(
                    "customers",
                    language
                ),

            "suppliers":
                "🏢 " + tr(
                    "suppliers",
                    language
                ),

            "purchases":
                "🛒 " + tr(
                    "purchases",
                    language
                ),

            "sales":
                "💰 " + tr(
                    "sales",
                    language
                ),

            "expenses":
                "💸 " + tr(
                    "expenses",
                    language
                ),

            "reports":
                "📊 " + tr(
                    "reports",
                    language
                ),

            "settings":
                "⚙️ " + tr(
                    "settings",
                    language
                ),
        }

        for page_name, text in navigation.items():

            if page_name in self.buttons:

                self.buttons[
                    page_name
                ].setText(
                    text
                )

        self.exit_button.setText(
            "🚪 " + tr(
                "exit",
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

        self.refresh_all_pages()

    # ========================================================
    # Style
    # ========================================================

    def apply_style(self):

        self.setStyleSheet("""
            QMainWindow {
                background: #f3f6fa;
            }

            #sidebar {
                background: #111827;
            }

            #logo {
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 5px;
            }

            #subtitle {
                color: #9ca3af;
                font-size: 12px;
                padding-left: 5px;
            }

            QPushButton#nav_button {
                background: transparent;
                color: #d1d5db;
                border: none;
                border-radius: 9px;
                text-align: left;
                padding: 13px 15px;
                font-size: 14px;
            }

            QPushButton#nav_button:hover {
                background: #1f2937;
                color: white;
            }

            QPushButton#nav_button:checked {
                background: #2563eb;
                color: white;
                font-weight: bold;
            }

            QPushButton#exit_button {
                background: #374151;
                color: white;
                border: none;
                border-radius: 9px;
                padding: 12px;
                font-weight: bold;
            }

            QPushButton#exit_button:hover {
                background: #dc2626;
            }

            #content {
                background: #f3f6fa;
            }
        """)


# ============================================================
# Application
# ============================================================

def main():

    # --------------------------------------------------------
    # إصلاح قاعدة البيانات قبل إنشاء أي صفحة
    # --------------------------------------------------------

    initialize_database()

    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        "Smart Inventory Manager"
    )

    window = MainWindow()

    window.show()

    sys.exit(
        app.exec()
    )


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":

    main()