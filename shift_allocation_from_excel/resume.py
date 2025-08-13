import frappe
import os
import docx2txt
import PyPDF2
import re

@frappe.whitelist()
def parse_resume_direct(file_url):
    try:
        if not file_url:
            frappe.throw("Please upload a resume first.")
        file_doc = frappe.get_doc("File", {"file_url": file_url})
        file_path = file_doc.get_full_path()

        resume_text = extract_text_from_file(file_path)

        name = extract_name_from_text(resume_text)
        email = extract_email_from_text(resume_text)
        mobile = extract_mobile_from_text(resume_text)

        return {
            "status": "success",
            "applicant_name": name or "Unknown",
            "email": email or "",
            "mobile": mobile or ""
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Resume Parser Error")
        return {"status": "error", "message": str(e)}


def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif ext == ".docx":
        return docx2txt.process(file_path)
    else:
        frappe.throw("Unsupported file format. Please upload PDF or DOCX.")


def extract_name_from_text(text):
    lines = text.split("\n")
    return lines[0].strip() if lines else None


def extract_email_from_text(text):
    match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    return match.group(0) if match else None


def extract_mobile_from_text(text):
    match = re.search(r"\+?\d[\d\s\-]{8,15}", text)
    if match:
        return match.group(0).strip()
    return None

