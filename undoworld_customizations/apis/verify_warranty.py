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
        frappe.local.response["product_name"] = serial_number_doc.item_code
        frappe.local.response["other_items"] = get_other_items(serial_number_doc)

    except frappe.DoesNotExistError:
        frappe.clear_messages()
        frappe.local.response["data"] = ""
        frappe.local.response.http_status_code = 404
        return "Invalid Serial Number"

def get_other_items(serial_number_doc):
    final_data = []
    args = {
        "serial_no": "%%%s%%" % serial_number_doc.name,
    }

    parent = frappe.db.sql(
        """select parent
        from
            `tabDelivery Note Item` dni
        where
            dni.serial_no like %(serial_no)s
        """,
        args,
    )
    print("Parenttttt ",parent, serial_number_doc.name, "'%"+serial_number_doc.name+"%'")
    if not parent:
        return ""
    customer = frappe.db.get_value("Delivery Note", parent, "customer")
    if customer:
        dns = frappe.get_all("Delivery Note", {"customer": customer})
        for dn in dns:
            dn_doc = frappe.get_doc("Delivery Note", dn)
            for item in dn_doc.items:
                if item.serial_no:
                    for sn in item.serial_no.split("\n"):
                        serial_number_doc = frappe.get_doc("Serial No", sn)
                        final_data.append({
                            "sn": sn,
                            "warranty_expiry_date": serial_number_doc.warranty_expiry_date,
                            "product_name": serial_number_doc.item_code,
                        })

    return final_data