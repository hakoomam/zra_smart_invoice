
import requests
import frappe

def get_zra_token():
    auth_url = frappe.conf.get("zra_auth_url")
    client_id = frappe.conf.get("zra_client_id")
    client_secret = frappe.conf.get("zra_client_secret")
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    resp = requests.post(auth_url, data=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()["access_token"]

def send_invoice_to_zra(doc):
    token = get_zra_token()
    zra_invoice_url = frappe.conf.get("zra_invoice_url")
    zra_payload = {
        "invoice_number": doc.name,
        "date": str(doc.posting_date),
        "customer_name": doc.customer_name,
        "customer_tax_id": doc.tax_id or "",
        "total_amount": float(doc.grand_total),
        "vat_amount": float(doc.total_taxes_and_charges),
        "items": [
            {
                "description": d.item_name,
                "qty": float(d.qty),
                "rate": float(d.rate),
                "amount": float(d.amount),
            }
            for d in doc.items
        ],
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(zra_invoice_url, json=zra_payload, headers=headers, timeout=20)
    status = "Failed"
    result = response.text
    if response.status_code == 200 and response.json().get("data"):
        zra_data = response.json()["data"]
        doc.db_set("zra_uid", zra_data.get("uid"))
        doc.db_set("zra_qr_code", zra_data.get("qr_code"))
        doc.db_set("zra_invoice_no", zra_data.get("invoice_number"))
        doc.db_set("zra_fiscal_device", zra_data.get("device_number"))
        doc.db_set("zra_status", "Fiscalized")
        status = "Fiscalized"
        result = response.text
        frappe.msgprint("Invoice successfully fiscalized by ZRA.")
    else:
        doc.db_set("zra_status", "Failed")
        frappe.msgprint("ZRA fiscalization failed. See logs for details.")
    # Log every attempt
    frappe.get_doc({
        "doctype": "ZRA Submission Log",
        "sales_invoice": doc.name,
        "status": status,
        "payload": frappe.as_json(zra_payload),
        "zra_response": result,
    }).insert(ignore_permissions=True)
