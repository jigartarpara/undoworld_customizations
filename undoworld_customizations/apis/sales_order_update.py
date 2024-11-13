import frappe
import requests


def on_update(doc, method):
    webhook_url = frappe.db.get_single_value("OMS Setup", "order_status_update_webhook")
    if doc.has_value_changed("so_status"):
        data = {
            "status": doc.so_status
        }
        response = requests.post(url=webhook_url, data=data)