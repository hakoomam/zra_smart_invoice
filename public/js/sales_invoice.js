
frappe.ui.form.on('Sales Invoice', {
    refresh(frm) {
        if (frm.doc.zra_status === "Failed" || frm.doc.zra_status === "Pending") {
            frm.add_custom_button("Send to ZRA", function() {
                frappe.call({
                    method: "zra_smart_invoice.sales_invoice.retry_send_to_zra",
                    args: {invoice: frm.doc.name},
                    freeze: true,
                    callback: function(r) {
                        frm.reload_doc();
                    }
                });
            });
        }
    }
});
