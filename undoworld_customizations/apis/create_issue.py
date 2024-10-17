import frappe

@frappe.whitelist(allow_guest=True,methods="POST")
def endpoint(subject, description, serial_number, customer):
    issue = frappe.get_doc(
        {
            "doctype": "Issue",
            "subject": subject,
            "description": description,
            "serial_number_cu": serial_number,
            "customer_name_cu": customer
        }
    )
    issue.insert(ignore_permissions=True)
    return issue.name