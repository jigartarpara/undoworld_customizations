import frappe

@frappe.whitelist(allow_guest=True,methods="POST")
def endpoint(issue):
    try:
        issue = frappe.get_doc("Issue",issue)
        return {
            "status": issue.status,
            "subject": issue.subject,
            "serial_number": issue.serial_number_cu,
            "priority": issue.priority,
            "issue_type": issue.issue_type,
            "description": issue.description,
            "resolution_by": issue.resolution_by,
            "customer_name": issue.customer_name,
            "customer": issue.customer

        }
    except frappe.DoesNotExistError:
        frappe.clear_messages()
        frappe.local.response.http_status_code = 404
        return "Invalid Ticket Number"