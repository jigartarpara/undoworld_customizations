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
        frappe.local.response["product_code"] = serial_number_doc.item_code
        frappe.local.response["product_name"] = serial_number_doc.item_name
        img_url = frappe.db.get_value("Item", serial_number_doc.item_code, "image")
        frappe.local.response["product_image"] = frappe.utils.get_url(img_url) if img_url else ""
        parent = get_dn(serial_number)
        frappe.local.response["customer_name"] = ""
        frappe.local.response["email"] = ""
        frappe.local.response["mobile_number"] = ""
        frappe.local.response["history"] = get_history(serial_number)
        if parent:
            customer = frappe.db.get_value("Delivery Note", parent, "customer")
            customer_doc = frappe.get_doc("Customer", customer)
            frappe.local.response["customer_name"] = customer_doc.customer_name
            frappe.local.response["mobile_number"] = customer_doc.cu_mobile_number
            frappe.local.response["email"] = customer_doc.cu_email
        frappe.local.response["other_items"] = get_other_items(serial_number_doc)

    except frappe.DoesNotExistError:
        frappe.clear_messages()
        frappe.local.response["data"] = ""
        frappe.local.response.http_status_code = 404
        return "Invalid Serial Number"
def get_history(sr):
    dn = get_dn(sr)
    if not dn:
        return
    customer = frappe.db.get_value("Delivery Note", dn, "customer")
    if not customer:
        return
    tickets = frappe.get_all("Support Ticket", {"customer":customer }, ["name as support_ticket","status" ])
    return tickets

def get_dn(srn):
    args = {
        "serial_no": "%%%s%%" % srn,
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
    return parent

def get_other_items(serial_number_doc):
    final_data = []
    parent = get_dn(serial_number_doc.name)
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
                        img_url = frappe.db.get_value("Item", serial_number_doc.item_code, "image")
                        final_data.append({
                            "sn": sn,
                            "warranty_expiry_date": serial_number_doc.warranty_expiry_date,
                            "product_name": serial_number_doc.item_name,
                            "product_code": serial_number_doc.item_code,
                            "product_image" : frappe.utils.get_url(img_url) if img_url else ""
                        })

    return final_data