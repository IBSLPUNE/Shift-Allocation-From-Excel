frappe.ui.form.on('Shift Allocation Tool', {
    refresh(frm) {
        frm.add_custom_button("Download Template", () => {
            if (!frm.doc.from_date || !frm.doc.to_date) {
                frappe.msgprint(__('Please set Start Date and End Date before downloading the template.'));
                return;
            }

            const startDate = frm.doc.from_date;
            const endDate = frm.doc.to_date;
            const docname = frm.doc.name;

            const url = `/api/method/shift_allocation_from_excel.download.download_shift_template?start_date=${startDate}&end_date=${endDate}&docname=${docname}`;

            window.open(url, "_blank");
        });
    }
});



frappe.ui.form.on('Shift Allocation Tool', {
    refresh: function(frm) {
        frm.add_custom_button(__('Get Employees'), function() {
            frappe.call({
                method: "shift_allocation_from_excel.api.get_employees",
                args: {
                    branch:frm.doc.branch || null,
                    department: frm.doc.department || null,
                    designation: frm.doc.designation || null,
                    employee_grade: frm.doc.employee_grade || null,
                    status: "Active"
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.msgprint(__('Fetched {0} employees', [r.message.length]));

                        frm.clear_table("shift_allocation_employees");
                        r.message.forEach(emp => {
                            let row = frm.add_child("shift_allocation_employees");
                            row.employee = emp.name;
                            row.employee_name = emp.employee_name;
                            row.designation = emp.designation;
                            row.department = emp.department;
                        });
                        frm.refresh_field("shift_allocation_employees");
                    }
                }
            });
        });
    }
});
frappe.ui.form.on('Shift Allocation Tool', {
    refresh: function(frm) {
        const note_id = 'shift-upload-note'; 
        if (!document.getElementById(note_id)) {
            const note = `
                <div id="${note_id}" style="font-weight: bold; color: red; margin-top: 10px;">
                    Note: Only a maximum of 50 employees can be uploaded.
                </div>
            `;

            $(frm.fields_dict['shift'].wrapper)
                .closest('.frappe-control')
                .after(note);
        }
    }
});

