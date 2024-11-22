import frappe

def on_submit(doc, method):
    if doc.stock_entry_type == "Courier Receive":
        for row in doc.items:
            if row.serial_no:
                for serial_no in row.serial_no.split("\n"):
                    support_ticket = frappe.db.get_value("Support Ticket", {"serial_number":  serial_no},"name")
                    if support_ticket:
                        frappe.db.set_value("Support Ticket",support_ticket,  "status", "Device Received")