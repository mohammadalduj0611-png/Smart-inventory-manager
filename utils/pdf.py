# ============================================================
# utils/pdf.py
# Smart Inventory Manager
# PDF Reports & Invoices
# ============================================================

from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


BASE_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = BASE_DIR / "reports"


def create_pdf(
    title,
    headers,
    rows,
    filename=None
):
    """
    إنشاء ملف PDF عام من جدول بيانات.
    """

    PDF_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if filename is None:
        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        filename = (
            f"report_{timestamp}.pdf"
        )

    output_file = PDF_DIR / filename

    document = SimpleDocTemplate(
        str(output_file),
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]

    title_style.alignment = TA_CENTER

    story = []

    story.append(
        Paragraph(
            title,
            title_style
        )
    )

    story.append(
        Spacer(1, 20)
    )

    table_data = [
        headers
    ]

    for row in rows:

        table_data.append([
            str(
                value
                if value is not None
                else ""
            )
            for value in row
        ])

    table = Table(
        table_data,
        repeatRows=1
    )

    table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#111827")
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [
                    colors.white,
                    colors.HexColor("#f3f4f6")
                ]
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

        ])
    )

    story.append(table)

    document.build(
        story
    )

    return output_file


def create_invoice_pdf(
    invoice_number,
    customer_name,
    items,
    total,
    discount=0,
    final_total=None,
    filename=None
):
    """
    إنشاء فاتورة PDF.
    """

    PDF_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if final_total is None:
        final_total = total - discount

    if filename is None:

        filename = (
            f"invoice_{invoice_number}.pdf"
        )

    output_file = PDF_DIR / filename

    document = SimpleDocTemplate(
        str(output_file),
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]

    title_style.alignment = TA_CENTER

    story = []

    story.append(
        Paragraph(
            "SMART INVENTORY MANAGER",
            title_style
        )
    )

    story.append(
        Spacer(1, 10)
    )

    story.append(
        Paragraph(
            f"Invoice #{invoice_number}",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Customer: {customer_name}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Date: "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M')}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 20)
    )

    table_data = [
        [
            "Product",
            "Quantity",
            "Price",
            "Subtotal",
        ]
    ]

    for item in items:

        if isinstance(item, dict):

            name = item.get(
                "name",
                ""
            )

            quantity = item.get(
                "quantity",
                0
            )

            price = item.get(
                "price",
                0
            )

            subtotal = item.get(
                "subtotal",
                quantity * price
            )

        else:

            name = item[0]
            quantity = item[1]
            price = item[2]

            if len(item) >= 4:
                subtotal = item[3]
            else:
                subtotal = quantity * price

        table_data.append([
            str(name),
            str(quantity),
            f"{float(price):.2f}",
            f"{float(subtotal):.2f}",
        ])

    table = Table(
        table_data,
        repeatRows=1
    )

    table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#111827")
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [
                    colors.white,
                    colors.HexColor("#f3f4f6")
                ]
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

        ])
    )

    story.append(table)

    story.append(
        Spacer(1, 20)
    )

    totals = [
        ["Total", f"{float(total):.2f}"],
        ["Discount", f"{float(discount):.2f}"],
        ["Final Total", f"{float(final_total):.2f}"],
    ]

    totals_table = Table(
        totals,
        colWidths=[150, 100]
    )

    totals_table.setStyle(
        TableStyle([

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "RIGHT"
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                "Helvetica-Bold"
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "BACKGROUND",
                (0, 2),
                (-1, 2),
                colors.HexColor("#dbeafe")
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

        ])
    )

    story.append(
        totals_table
    )

    story.append(
        Spacer(1, 30)
    )

    story.append(
        Paragraph(
            "Thank you for your business!",
            styles["Normal"]
        )
    )

    document.build(
        story
    )

    return output_file


def open_pdf_folder():

    PDF_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    return PDF_DIR


if __name__ == "__main__":

    file = create_pdf(
        "Inventory Report",
        [
            "ID",
            "Product",
            "Quantity"
        ],
        [
            [1, "Keyboard", 10],
            [2, "Mouse", 25],
            [3, "Monitor", 5],
        ]
    )

    print(
        f"PDF created: {file}"
    )