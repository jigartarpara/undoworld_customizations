import frappe

@frappe.whitelist(allow_guest=True)
def endpoint(serial_number):
    try:
        serial_number_doc = frappe.get_doc("Serial No", serial_number)
        if serial_number_doc.maintenance_status in ["Out of Warranty", "Out of AMC", ""]:
            frappe.local.response["status"] = "Out of Warranty"
        else:
            frappe.local.response["status"] = "Under Warranty"
    except frappe.DoesNotExistError:
        frappe.clear_messages()
        frappe.local.response["data"] = ""
        frappe.local.response.http_status_code = 404
        return "Invalid Serial Number"