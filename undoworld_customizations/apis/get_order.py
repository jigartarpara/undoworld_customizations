import frappe

@frappe.whitelist(allow_guest=True,methods="POST")
def endpoint(mobile_number):
    try:
        customer = frappe.db.get_value("Customer", {"cu_mobile_number": mobile_number})
        if not customer:
            raise frappe.DoesNotExistError
        sos = frappe.get_all("Sales Order", {"customer":customer})
        data = []
        for so in sos:
           so_doc = frappe.get_doc("Sales Order", so['name']) 
           items = []
           for item in so_doc.items:
               items.append({
                   "item_code": item.item_code,
                   "item_name": item.item_name,
                   "description": item.description,
                   "image_view": frappe.utils.get_url(item.image) if item.image else ""
               })
           data.append({
               "items": items,
               "order_id": so_doc.name,
               "posting_date": so_doc.transaction_date,
               "customer_name": so_doc.customer,
               "mobile_number": frappe.db.get_value("Customer", so_doc.customer, "cu_mobile_number"),
               "email": frappe.db.get_value("Customer", so_doc.customer, "cu_email")
           })
        return data
        
    except frappe.DoesNotExistError:
        frappe.clear_messages()
        frappe.local.response.http_status_code = 404
        return "No Record Exist."