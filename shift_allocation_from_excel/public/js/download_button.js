frappe.ui.form.on('Shift Allocation Tool', {
    refresh(frm) {
        frm.add_custom_button("Download Template", () => {
            window.open(
                "/api/method/gps.download.download_shift_template",
                "_blank"
            );
        });
    }
});
