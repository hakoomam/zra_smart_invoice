
import frappe
from .api import send_invoice_to_zra

def on_submit_sales_invoice(doc, method):
    try:
        send_invoice_to_zra(doc)
    except Exception as e:
        doc.db_set("zra_status", "Failed")
        frappe.log_error(frappe.get_traceback(), "ZRA Integration Error")

def add_manual_retry_button(doc, method):
    if frappe.form_dict and doc.get("zra_status") in ["Failed", "Pending"]:
        frappe.local.response["doc"].add_custom_button(
            "Send to ZRA",
            lambda: frappe.call({
                "method": "zra_smart_invoice.sales_invoice.retry_send_to_zra",
                "args": {"invoice": doc.name},
                "freeze": True,
            }),
            "Actions"
        )

@frappe.whitelist()
def retry_send_to_zra(invoice):
    doc = frappe.get_doc("Sales Invoice", invoice)
    send_invoice_to_zra(doc)
