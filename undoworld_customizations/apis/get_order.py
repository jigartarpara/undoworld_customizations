import frappe
from frappe.utils import getdate,nowdate

@frappe.whitelist(methods="POST")
def endpoint(mobile_number):
    try:
        customer = frappe.db.get_value("Customer", {"cu_mobile_number": mobile_number})
        if not customer:
            raise frappe.DoesNotExistError
        dns = frappe.get_all("Delivery Note", {"customer":customer, "docstatus": "1"})
        data = []
        for dn in dns:
            dn_doc = frappe.get_doc("Delivery Note", dn['name']) 
            items = []
            against_sales_order = ""
            so_doc = None
            for item in dn_doc.items:
                warranty_expiry_date = ""
                custom_imei1 = ""
                warranty_status = ""
                if item.serial_no:
                    for serial_no in item.serial_no.split("\n"):
                        srn_doc = frappe.get_doc("Serial No", serial_no)
                        warranty_expiry_date = srn_doc.warranty_expiry_date
                        custom_imei1 = srn_doc.custom_imei1
                        warranty_status = set_maintenance_status(srn_doc)
                image = frappe.db.get_value("Item", item.item_code, "image")   
                items.append({
                   "item_code": item.item_code,
                   "item_name": item.item_name,
                   "description": item.description,
                   "image_view": frappe.utils.get_url(image) if image else "",
                   "warranty_expiry_date": warranty_expiry_date,
                   "imei": custom_imei1,
                   "warranty_status": warranty_status
                })
                if item.against_sales_order:
                   against_sales_order = item.against_sales_order
                   so_doc = frappe.get_doc("Sales Order", against_sales_order)
            data.append({
                "items": items,
                "order_id": against_sales_order,
                "posting_date": so_doc.transaction_date if so_doc else "",
                "develivered_on": dn_doc.posting_date,
                "customer_name": dn_doc.customer,
                "mobile_number": frappe.db.get_value("Customer", dn_doc.customer, "cu_mobile_number"),
                "email": frappe.db.get_value("Customer", dn_doc.customer, "cu_email")
            })
        return data
        
    except frappe.DoesNotExistError:
        frappe.clear_messages()
        frappe.local.response.http_status_code = 404
        return "No Record Exist."
    

def set_maintenance_status(serial_number_doc):

    if serial_number_doc.warranty_expiry_date and getdate(serial_number_doc.warranty_expiry_date) < getdate(nowdate()):
        return "Out of Warranty"

    if serial_number_doc.warranty_expiry_date and getdate(serial_number_doc.warranty_expiry_date) >= getdate(nowdate()):
        return "Under Warranty"