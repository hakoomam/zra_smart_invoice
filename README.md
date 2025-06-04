# ZRA Smart Invoice Frappe App

**Author:** Miyanda Hakooma  
**Company:** Antares Zambia Limited  
**Email:** mh@antares.co.zm

## Features
- Auto-fiscalizes Sales Invoice on Submit with ZRA Smart Invoice API.
- Manual "Send to ZRA" button for retrying failed/pending invoices.
- Logs every submission and result (viewable in ERPNext).
- Stores ZRA UID, QR Code, Fiscal Device on Sales Invoice.

## Installation
1. Extract this folder into your bench `/apps/` directory.
2. Run:
   ```sh
   bench --site [yoursite] install-app zra_smart_invoice
