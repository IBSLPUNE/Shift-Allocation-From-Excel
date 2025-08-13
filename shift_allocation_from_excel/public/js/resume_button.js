frappe.ui.form.on("Job Applicant", {
    refresh(frm) {
        frm.add_custom_button(__('Parse Resume'), function () {
            let d = new frappe.ui.Dialog({
                title: 'Upload Resume',
                fields: [
                    {
                        label: 'Resume File',
                        fieldname: 'resume',
                        fieldtype: 'Attach',
                        reqd: 1
                    }
                ],
                primary_action_label: 'Parse & Save',
                primary_action(values) {
                    frappe.call({
                        method: "shift_allocation_from_excel.resume.parse_resume_direct",
                        args: {
                            file_url: values.resume
                        },
                        freeze: true,
                        freeze_message: __("Parsing resume..."),
                        callback(r) {
                            if (r.message && r.message.status === "success") {
                                frm.set_value("applicant_name", r.message.applicant_name);
                                frm.set_value("email_id", r.message.email);
                                frm.set_value("phone_number", r.message.mobile);
                                frm.set_value("resume_attachment", values.resume);

                                frm.save()
                                    .then(() => {
                                        frappe.show_alert({
                                            message: __('Resume parsed and saved successfully.'),
                                            indicator: 'green'
                                        }, 5);
                                    });
                            } else {
                                frappe.msgprint(__('Error: ' + (r.message.message || 'Unknown error')));
                            }
                            d.hide();
                        }
                    });
                }
            });
            d.show();
        });
    }
});

