frappe.ui.form.on('Shift Allocation Tool', {
    refresh(frm) {
        frm.add_custom_button("Download Template", () => {
            if (!frm.doc.from_date || !frm.doc.to_date) {
                frappe.msgprint(__('Please set Start Date and End Date before downloading the template.'));
                return;
            }

            const startDate = frm.doc.from_date;
            const endDate = frm.doc.to_date;

            const url = `/api/method/shift_allocation_from_excel.download.download_shift_template?start_date=${startDate}&end_date=${endDate}`;

            window.open(url, "_blank");
        });
    }
});

