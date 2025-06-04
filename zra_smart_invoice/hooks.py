
doc_events = {
    "Sales Invoice": {
        "on_submit": "zra_smart_invoice.sales_invoice.on_submit_sales_invoice",
        "validate": "zra_smart_invoice.sales_invoice.add_manual_retry_button"
    }
}
