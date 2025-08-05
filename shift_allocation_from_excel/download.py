import frappe
import openpyxl
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter
from frappe.utils import getdate, add_days, now_datetime
import io

@frappe.whitelist()
def download_shift_template(start_date, end_date):
    start_date = getdate(start_date)
    end_date = getdate(end_date)
    total_days = (end_date - start_date).days + 1

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Shift Template"

    headers = ["S. No", "EMPLOYEE ID", "EMPLOYEE NAME"]

    for i in range(total_days):
        current_date = add_days(start_date, i)
        date_str = current_date.strftime("%-d-%b-%Y")
        headers.append(date_str)

    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.font = Font(bold=True)
        ws.column_dimensions[get_column_letter(col_idx)].width = 15

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    frappe.response["filename"] = f"Shift_Template_{start_date}_to_{end_date}_current_{now_datetime()}.xlsx"
    frappe.response["filecontent"] = buffer.read()
    frappe.response["type"] = "binary"





