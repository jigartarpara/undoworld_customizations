import frappe

@frappe.whitelist(allow_guest=True,methods="POST")
def endpoint(sales_order, address):
    try:
        so = frappe.get_doc("Sales Order",sales_order)
        so.so_address = address
        so.save(ignore_permissions=True)
        return "Updated"
    except frappe.DoesNotExistError:
        frappe.clear_messages()
        frappe.local.response.http_status_code = 404
        return "Invalid Sales Order Number"