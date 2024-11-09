# Copyright (c) 2024, Frappe Customizations and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today, now

class SupportTicket(Document):
    def validate(self):
        if self.serial_number:
            dn = self.get_dn(self.serial_number)
            if dn:
                self.customer = frappe.db.get_value("Delivery Note", dn, "customer")
        self.update_history()

    
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
    def update_history(self):
        if self.has_value_changed("status"):
            self.append("status_tracking", {
                "status": self.status,
                "posting_date": today(),
                "posting_time": now(),
            })
    def get_history(self):
        data = []
        for row in self.status_tracking:
            data.append({
                "status": row.status,
                "posting_date": row.posting_date,
                "posting_time": row.posting_time,
                "remark": row.remark
            })
        return data
