import frappe
import openpyxl
from frappe.utils import getdate, add_days
from collections import defaultdict

def process_shift_excel(doc, method):
    if not doc.shift:
        frappe.throw("Please attach the Excel file in the 'shift' field.")

    try:
        file_doc = frappe.get_doc("File", {"file_url": doc.shift})
        file_path = file_doc.get_full_path()
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "❌ Failed to retrieve Excel file")
        frappe.throw("Could not retrieve or read the attached file.")

    try:
        wb = openpyxl.load_workbook(file_path)
        ws = wb.active
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "❌ Failed to open Excel workbook")
        frappe.throw("Failed to read Excel file.")

    all_rows = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row or not row[0] or not row[1] or not row[2]:
            continue
        employee = str(row[0]).strip()
        shift = str(row[2]).strip().upper()
        date = getdate(row[1])
        all_rows.append((employee, date, shift))

    # Sort by employee and date
    all_rows.sort()

    current_emp = None
    current_shift = None
    start_date = None
    last_date = None

    for entry in all_rows:
        emp, date, shift = entry

        if shift == "W/O":
            try:
                add_holiday(emp, date.strftime("%Y-%m-%d"))
            except Exception as e:
                frappe.log_error(frappe.get_traceback(), f"❌ Failed to add holiday for {emp} on {date}")
                raise
            continue

        if (emp == current_emp and shift == current_shift and
                date == add_days(last_date, 1)):
            # Extend current shift block
            last_date = date
        else:
            # Submit previous block if exists
            if current_emp and current_shift:
                try:
                    create_shift_assignment(current_emp, current_shift,
                                            start_date.strftime("%Y-%m-%d"),
                                            last_date.strftime("%Y-%m-%d"))
                except Exception as e:
                    frappe.log_error(frappe.get_traceback(),
                                     f"❌ Failed to create shift assignment for {current_emp}")
                    raise
            # Start new block
            current_emp = emp
            current_shift = shift
            start_date = last_date = date

    # Final group
    if current_emp and current_shift:
        try:
            create_shift_assignment(current_emp, current_shift,
                                    start_date.strftime("%Y-%m-%d"),
                                    last_date.strftime("%Y-%m-%d"))
        except Exception as e:
            frappe.log_error(frappe.get_traceback(),
                             f"❌ Failed to create final shift assignment for {current_emp}")
            raise

    frappe.msgprint("✅ Grouped Shift Assignments & Holidays created.")

def create_shift_assignment(employee, shift_type, start_date, end_date):
    doc = frappe.new_doc("Shift Assignment")
    doc.update({
        "employee": employee,
        "shift_type": shift_type,
        "start_date": start_date,
        "end_date": end_date
    })
    doc.insert(ignore_permissions=True)
    doc.submit()

def add_holiday(employee_id, date_str):
    try:
        employee = frappe.get_doc("Employee", employee_id)
        if not employee.holiday_list:
            frappe.throw(f"No holiday list assigned for employee {employee_id}")

        holiday_list = frappe.get_doc("Holiday List", employee.holiday_list)

        # Skip if already present
        if any(h.holiday_date.strftime("%Y-%m-%d") == date_str for h in holiday_list.holidays):
            return

        # Get weekday name
        day_name = getdate(date_str).strftime("%A")

        holiday_list.append("holidays", {
            "holiday_date": date_str,
            "weekly_off": 1,
            "description": f"{day_name} Weekly Off from Excel"
        })

        holiday_list.save()

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"❌ Error in add_holiday for {employee_id} on {date_str}")
        raise


