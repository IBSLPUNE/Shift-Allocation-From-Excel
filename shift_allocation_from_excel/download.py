import frappe
import openpyxl
from openpyxl.utils import get_column_letter
from frappe.utils import now_datetime
import io

@frappe.whitelist()
def download_shift_template():
    # Create workbook and worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Shift Template"

    # Header row
    headers = ["Employee ID", "Date", "Shift"]
    ws.append(headers)

    # Optional sample row
    #ws.append(["EMP-0001", "2025-08-05", "A"])  # A = Shift Type

    # Adjust column widths
    for idx, header in enumerate(headers, 1):
        ws.column_dimensions[get_column_letter(idx)].width = 20

    # Save workbook to memory
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    # Set binary response
    frappe.response["filename"] = f"Shift_Template_{now_datetime().date()}.xlsx"
    frappe.response["filecontent"] = buffer.read()
    frappe.response["type"] = "binary"

