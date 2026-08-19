# ============================================================
# utils/translations.py
# Smart Inventory Manager
# Arabic / English Translation System
# ============================================================

import json
import os


SETTINGS_FILE = "settings.json"


# ============================================================
# Translations
# ============================================================

TRANSLATIONS = {

    # --------------------------------------------------------
    # Application
    # --------------------------------------------------------

    "app_name": {
        "English": "Smart Inventory Manager",
        "Arabic": "مدير المخزون الذكي",
    },

    # --------------------------------------------------------
    # Navigation
    # --------------------------------------------------------

    "dashboard": {
        "English": "Dashboard",
        "Arabic": "لوحة التحكم",
    },

    "products": {
        "English": "Products",
        "Arabic": "المنتجات",
    },

    "categories": {
        "English": "Categories",
        "Arabic": "التصنيفات",
    },

    "customers": {
        "English": "Customers",
        "Arabic": "العملاء",
    },

    "suppliers": {
        "English": "Suppliers",
        "Arabic": "الموردون",
    },

    "purchases": {
        "English": "Purchases",
        "Arabic": "المشتريات",
    },

    "sales": {
        "English": "Sales",
        "Arabic": "المبيعات",
    },

    "expenses": {
        "English": "Expenses",
        "Arabic": "المصروفات",
    },

    "reports": {
        "English": "Reports",
        "Arabic": "التقارير",
    },

    "settings": {
        "English": "Settings",
        "Arabic": "الإعدادات",
    },

    "exit": {
        "English": "Exit",
        "Arabic": "خروج",
    },

    # --------------------------------------------------------
    # Common
    # --------------------------------------------------------

    "add": {
        "English": "Add",
        "Arabic": "إضافة",
    },

    "edit": {
        "English": "Edit",
        "Arabic": "تعديل",
    },

    "delete": {
        "English": "Delete",
        "Arabic": "حذف",
    },

    "save": {
        "English": "Save",
        "Arabic": "حفظ",
    },

    "cancel": {
        "English": "Cancel",
        "Arabic": "إلغاء",
    },

    "update": {
        "English": "Update",
        "Arabic": "تحديث",
    },

    "refresh": {
        "English": "Refresh",
        "Arabic": "تحديث",
    },

    "search": {
        "English": "Search",
        "Arabic": "بحث",
    },

    "close": {
        "English": "Close",
        "Arabic": "إغلاق",
    },

    "yes": {
        "English": "Yes",
        "Arabic": "نعم",
    },

    "no": {
        "English": "No",
        "Arabic": "لا",
    },

    "confirm": {
        "English": "Confirm",
        "Arabic": "تأكيد",
    },

    "warning": {
        "English": "Warning",
        "Arabic": "تحذير",
    },

    "error": {
        "English": "Error",
        "Arabic": "خطأ",
    },

    "success": {
        "English": "Success",
        "Arabic": "نجاح",
    },

    "information": {
        "English": "Information",
        "Arabic": "معلومات",
    },

    # --------------------------------------------------------
    # Dashboard
    # --------------------------------------------------------

    "dashboard_title": {
        "English": "Dashboard",
        "Arabic": "لوحة التحكم",
    },

    "welcome": {
        "English": "Welcome to Smart Inventory Manager",
        "Arabic": "مرحبًا بك في مدير المخزون الذكي",
    },

    "dashboard_welcome": {
        "English": "Manage your products, customers, suppliers and inventory easily.",
        "Arabic": "قم بإدارة منتجاتك وعملائك ومورديك ومخزونك بسهولة.",
    },

    "quick_actions": {
        "English": "Quick Actions",
        "Arabic": "إجراءات سريعة",
    },

    "total_products": {
        "English": "Total Products",
        "Arabic": "إجمالي المنتجات",
    },

    "total_customers": {
        "English": "Total Customers",
        "Arabic": "إجمالي العملاء",
    },

    "total_suppliers": {
        "English": "Total Suppliers",
        "Arabic": "إجمالي الموردين",
    },

    "total_sales": {
        "English": "Total Sales",
        "Arabic": "إجمالي المبيعات",
    },

    "total_purchases": {
        "English": "Total Purchases",
        "Arabic": "إجمالي المشتريات",
    },

    "low_stock": {
        "English": "Low Stock",
        "Arabic": "مخزون منخفض",
    },

    # --------------------------------------------------------
    # Products
    # --------------------------------------------------------

    "product": {
        "English": "Product",
        "Arabic": "المنتج",
    },

    "product_code": {
        "English": "Product Code",
        "Arabic": "رمز المنتج",
    },

    "product_name": {
        "English": "Product Name",
        "Arabic": "اسم المنتج",
    },

    "products_title": {
        "English": "Products",
        "Arabic": "المنتجات",
    },

    "add_product": {
        "English": "Add Product",
        "Arabic": "إضافة منتج",
    },

    "edit_product": {
        "English": "Edit Product",
        "Arabic": "تعديل المنتج",
    },

    "purchase_price": {
        "English": "Purchase Price",
        "Arabic": "سعر الشراء",
    },

    "selling_price": {
        "English": "Selling Price",
        "Arabic": "سعر البيع",
    },

    "quantity": {
        "English": "Quantity",
        "Arabic": "الكمية",
    },

    "minimum_stock": {
        "English": "Minimum Stock",
        "Arabic": "الحد الأدنى للمخزون",
    },

    "description": {
        "English": "Description",
        "Arabic": "الوصف",
    },

    "product_search": {
        "English": "Search products...",
        "Arabic": "ابحث عن المنتجات...",
    },

    "search_products": {
        "English": "Search products...",
        "Arabic": "ابحث عن المنتجات...",
    },

    "low_stock_status": {
        "English": "Low Stock",
        "Arabic": "مخزون منخفض",
    },

    "in_stock": {
        "English": "In Stock",
        "Arabic": "متوفر",
    },

    "product_added": {
        "English": "Product added successfully.",
        "Arabic": "تمت إضافة المنتج بنجاح.",
    },

    "product_updated": {
        "English": "Product updated successfully.",
        "Arabic": "تم تحديث المنتج بنجاح.",
    },

    "product_deleted": {
        "English": "Product deleted successfully.",
        "Arabic": "تم حذف المنتج بنجاح.",
    },

    "duplicate_code": {
        "English": "Duplicate Product Code",
        "Arabic": "رمز المنتج مكرر",
    },

    "duplicate_code_message": {
        "English": "This product code already exists.",
        "Arabic": "رمز المنتج هذا موجود مسبقًا.",
    },

    "select_product": {
        "English": "Select Product",
        "Arabic": "اختيار المنتج",
    },

    "select_product_message": {
        "English": "Please select a product first.",
        "Arabic": "يرجى اختيار منتج أولًا.",
    },

    "delete_product": {
        "English": "Delete Product",
        "Arabic": "حذف المنتج",
    },

    "delete_product_question": {
        "English": "Are you sure you want to delete this product?",
        "Arabic": "هل أنت متأكد أنك تريد حذف هذا المنتج؟",
    },

    "missing_data": {
        "English": "Missing Data",
        "Arabic": "بيانات ناقصة",
    },

    "enter_product_code": {
        "English": "Please enter the product code.",
        "Arabic": "يرجى إدخال رمز المنتج.",
    },

    "enter_product_name": {
        "English": "Please enter the product name.",
        "Arabic": "يرجى إدخال اسم المنتج.",
    },

    # --------------------------------------------------------
    # Customers
    # --------------------------------------------------------

    "add_customer": {
        "English": "Add Customer",
        "Arabic": "إضافة عميل",
    },

    "edit_customer": {
        "English": "Edit Customer",
        "Arabic": "تعديل العميل",
    },

    "customer_name": {
        "English": "Customer Name",
        "Arabic": "اسم العميل",
    },

    "phone": {
        "English": "Phone",
        "Arabic": "الهاتف",
    },

    "email": {
        "English": "Email",
        "Arabic": "البريد الإلكتروني",
    },

    "address": {
        "English": "Address",
        "Arabic": "العنوان",
    },

    "notes": {
        "English": "Notes",
        "Arabic": "ملاحظات",
    },

    "search_customers": {
        "English": "Search customers...",
        "Arabic": "ابحث عن العملاء...",
    },

    "customer_added": {
        "English": "Customer added successfully.",
        "Arabic": "تمت إضافة العميل بنجاح.",
    },

    "customer_updated": {
        "English": "Customer updated successfully.",
        "Arabic": "تم تحديث العميل بنجاح.",
    },

    "customer_deleted": {
        "English": "Customer deleted successfully.",
        "Arabic": "تم حذف العميل بنجاح.",
    },

    "select_customer": {
        "English": "Select Customer",
        "Arabic": "اختيار العميل",
    },

    "delete_customer_question": {
        "English": "Are you sure you want to delete this customer?",
        "Arabic": "هل أنت متأكد أنك تريد حذف هذا العميل؟",
    },

    "missing_customer_name": {
        "English": "Please enter customer name.",
        "Arabic": "يرجى إدخال اسم العميل.",
    },

    # --------------------------------------------------------
    # Suppliers
    # --------------------------------------------------------

    "add_supplier": {
        "English": "Add Supplier",
        "Arabic": "إضافة مورد",
    },

    "edit_supplier": {
        "English": "Edit Supplier",
        "Arabic": "تعديل المورد",
    },

    "supplier_name": {
        "English": "Supplier Name",
        "Arabic": "اسم المورد",
    },

    "company": {
        "English": "Company",
        "Arabic": "الشركة",
    },

    "search_suppliers": {
        "English": "Search suppliers...",
        "Arabic": "ابحث عن الموردين...",
    },

    "supplier_added": {
        "English": "Supplier added successfully.",
        "Arabic": "تمت إضافة المورد بنجاح.",
    },

    "supplier_updated": {
        "English": "Supplier updated successfully.",
        "Arabic": "تم تحديث المورد بنجاح.",
    },

    "supplier_deleted": {
        "English": "Supplier deleted successfully.",
        "Arabic": "تم حذف المورد بنجاح.",
    },

    "select_supplier": {
        "English": "Select Supplier",
        "Arabic": "اختيار المورد",
    },

    "delete_supplier_question": {
        "English": "Are you sure you want to delete this supplier?",
        "Arabic": "هل أنت متأكد أنك تريد حذف هذا المورد؟",
    },

    "missing_supplier_name": {
        "English": "Please enter supplier name.",
        "Arabic": "يرجى إدخال اسم المورد.",
    },

    # --------------------------------------------------------
    # Categories
    # --------------------------------------------------------

    "categories_title": {
        "English": "Categories",
        "Arabic": "التصنيفات",
    },

    "add_category": {
        "English": "Add Category",
        "Arabic": "إضافة تصنيف",
    },

    "edit_category": {
        "English": "Edit Category",
        "Arabic": "تعديل التصنيف",
    },

    "category_name": {
        "English": "Category Name",
        "Arabic": "اسم التصنيف",
    },

    "category_search": {
        "English": "Search categories...",
        "Arabic": "ابحث عن التصنيفات...",
    },

    "search_categories": {
        "English": "Search categories...",
        "Arabic": "ابحث عن التصنيفات...",
    },

    "category_added": {
        "English": "Category added successfully.",
        "Arabic": "تمت إضافة التصنيف بنجاح.",
    },

    "category_updated": {
        "English": "Category updated successfully.",
        "Arabic": "تم تحديث التصنيف بنجاح.",
    },

    "category_deleted": {
        "English": "Category deleted successfully.",
        "Arabic": "تم حذف التصنيف بنجاح.",
    },

    "duplicate_category": {
        "English": "Duplicate Category",
        "Arabic": "تصنيف مكرر",
    },

    "duplicate_category_message": {
        "English": "This category already exists.",
        "Arabic": "هذا التصنيف موجود مسبقًا.",
    },

    "select_category": {
        "English": "Select Category",
        "Arabic": "اختيار التصنيف",
    },

    "select_category_message": {
        "English": "Please select a category first.",
        "Arabic": "يرجى اختيار تصنيف أولًا.",
    },

    "delete_category": {
        "English": "Delete Category",
        "Arabic": "حذف التصنيف",
    },

    "delete_category_question": {
        "English": "Are you sure you want to delete this category?",
        "Arabic": "هل أنت متأكد أنك تريد حذف هذا التصنيف؟",
    },

    "enter_category_name": {
        "English": "Please enter category name.",
        "Arabic": "يرجى إدخال اسم التصنيف.",
    },

    # --------------------------------------------------------
    # Purchases
    # --------------------------------------------------------

    "purchases_title": {
        "English": "Purchases",
        "Arabic": "المشتريات",
    },

    "add_purchase": {
        "English": "Add Purchase",
        "Arabic": "إضافة عملية شراء",
    },

    # --------------------------------------------------------
    # Sales
    # --------------------------------------------------------

    "sales_title": {
        "English": "Sales",
        "Arabic": "المبيعات",
    },

    "add_sale": {
        "English": "Add Sale",
        "Arabic": "إضافة عملية بيع",
    },

    # --------------------------------------------------------
    # Expenses
    # --------------------------------------------------------

    "expenses_title": {
        "English": "Expenses",
        "Arabic": "المصروفات",
    },

    "add_expense": {
        "English": "Add Expense",
        "Arabic": "إضافة مصروف",
    },

    # --------------------------------------------------------
    # Reports
    # --------------------------------------------------------

    "reports_title": {
        "English": "Reports",
        "Arabic": "التقارير",
    },

    "generate_report": {
        "English": "Generate Report",
        "Arabic": "إنشاء تقرير",
    },

    # --------------------------------------------------------
    # Settings
    # --------------------------------------------------------

    "settings_title": {
        "English": "Settings",
        "Arabic": "الإعدادات",
    },

    "settings_subtitle": {
        "English": "Customize application settings",
        "Arabic": "تخصيص إعدادات التطبيق",
    },

    "language": {
        "English": "Language",
        "Arabic": "اللغة",
    },

    "language_description": {
        "English": "Choose the language you want to use in the application.",
        "Arabic": "اختر اللغة التي تريد استخدامها في التطبيق.",
    },

    "application_language": {
        "English": "Application Language:",
        "Arabic": "لغة التطبيق:",
    },

    "save_settings": {
        "English": "Save Settings",
        "Arabic": "حفظ الإعدادات",
    },

    # --------------------------------------------------------
    # Table
    # --------------------------------------------------------

    "id": {
        "English": "ID",
        "Arabic": "الرقم",
    },

    "name": {
        "English": "Name",
        "Arabic": "الاسم",
    },

    "created_at": {
        "English": "Created At",
        "Arabic": "تاريخ الإنشاء",
    },

    "actions": {
        "English": "Actions",
        "Arabic": "الإجراءات",
    },

    "date": {
        "English": "Date",
        "Arabic": "التاريخ",
    },

    "total": {
        "English": "Total",
        "Arabic": "الإجمالي",
    },
}


# ============================================================
# Get Current Language
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
# Translation Function
# ============================================================

def tr(
    key,
    language=None
):

    if language is None:
        language = get_language()

    translation = TRANSLATIONS.get(key)

    if not translation:
        return key

    return translation.get(
        language,
        translation.get(
            "English",
            key
        )
    )


# ============================================================
# Available Languages
# ============================================================

LANGUAGES = {

    "English": "English",

    "Arabic": "العربية",

}