import frappe
import requests


def on_update(doc, method):
    webhook_url = frappe.db.get_single_value("OMS Setup", "order_status_update_webhook")
    if webhook_url and doc.has_value_changed("so_status"):
        tracking_id, waybill = get_tracking_id(doc.name)
        orde_details = []
        for row in doc.items
            orde_details.append({
                "device": row.item_code,
                "specs": row.description,
                "warranty": ""
            })
        customer = frappe.get_doc("Customer", doc.customer)
        data = {
            "status": doc.so_status,
            "order_placed_on": doc.transaction_date,
            "delivery_status": doc.delivery_status,
            "location": "",
            "remark": "",
            "timestamp": "",
            "expected_delivery_date": "",
            "tracking_id": tracking_id,
            "waybill": waybill,
            "order_details": orde_details,
            "customer_name": doc.customer,
            "customer_phone": customer.cu_mobile_number,
            "shipping_address": customer.shipping_address,
            "paymenttype": doc.payment_type_un,
            "amount": doc.payment_amount_un,
            "paymentmethod": doc.paymentmethod,
            "payment_status": doc.payment_status

        }
        try:
            response = requests.post(url=webhook_url, data=data)
        except:
            pass

def get_tracking_id(so):
    tracking_id = frappe.db.get_value("Clickpost Order", {"sales_order": so}, "tracking_id")
    waybill = frappe.db.get_value("Clickpost Order", {"sales_order": so}, "waybill")
    return tracking_id, waybill