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


import pdfplumber

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        with pdfplumber.open(file_path) as pdf:
            return "\n".join([page.extract_text() or "" for page in pdf.pages])
    elif ext == ".docx":
        return docx2txt.process(file_path)
    else:
        frappe.throw("Unsupported file format. Please upload PDF or DOCX.")



def extract_name_from_text(text):
    match = re.search(r"(Mr|Ms|Mrs)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*", text)
    if match:
        return match.group(0).replace("Mr ", "").replace("Ms ", "").replace("Mrs ", "").strip()
    # fallback: first non-empty line
    for line in text.split("\n"):
        if line.strip() and len(line.split()) <= 4:  # likely a short name
            return line.strip()
    return None



def extract_email_from_text(text):
    match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    return match.group(0) if match else None


def extract_mobile_from_text(text):
    match = re.search(r"\+?\d[\d\s\-]{8,15}", text)
    if match:
        return match.group(0).strip()
    return None

