# Copyright (c) 2024, Frappe Customizations and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SupportTicket(Document):
    def validate(self):
        if self.serial_number:
            dn = self.get_dn(self.serial_number)
            if dn:
                self.customer = frappe.db.get_value("Delivery Note", dn, "customer")

    
    def get_dn(self, srn):
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
    
    def get_history(self):
        return {}
