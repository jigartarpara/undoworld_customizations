import frappe

@frappe.whitelist(allow_guest=True)
def endpoint(serial_number):
    try:
        serial_number_doc = frappe.get_doc("Serial No", serial_number)
        if serial_number_doc.maintenance_status in ["Out of Warranty", "Out of AMC", ""]:
            frappe.local.response["status"] = "Out of Warranty"
        else:
            frappe.local.response["status"] = "Under Warranty"
        frappe.local.response["warranty_expiry_date"] = serial_number_doc.warranty_expiry_date
        frappe.local.response["product_name"] = serial_number_doc.item_name
        frappe.local.response["other_items"] = get_other_items(serial_number_doc)

    except frappe.DoesNotExistError:
        frappe.clear_messages()
        frappe.local.response["data"] = ""
        frappe.local.response.http_status_code = 404
        return "Invalid Serial Number"

def get_other_items(serial_number_doc):
    final_data = []
    if serial_number_doc.customer:
        dns = frappe.get_all("Delivery Note", {"customer": serial_number_doc.customer})
        for dn in dns:
            dn_doc = frappe.get_doc("Delivery Note", dn)
            for item in dn_doc.items:
                if item.serial_no:
                    for sn in item.serial_no.split("\n"):
                        serial_number_doc = frappe.get_doc("Serial No", sn)
                        final_data.append({
                            "sn": sn,
                            "warranty_expiry_date": serial_number_doc.warranty_expiry_date,
                            "product_name": serial_number_doc.item_name,
                        })

    return final_data