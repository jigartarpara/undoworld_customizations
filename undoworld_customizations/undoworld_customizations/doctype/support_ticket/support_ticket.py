# Copyright (c) 2024, Frappe Customizations and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today, now
from frappe.desk.form import assign_to

class SupportTicket(Document):
    def validate(self):
        self.update_serial_number()
        if self.serial_number:
            dn = self.get_dn(self.serial_number)
            if dn:
                self.customer = frappe.db.get_value("Delivery Note", dn, "customer")
        self.update_history()
        self.assigned_user()
    
    def assigned_user(self):
        for row in self.repairing_planning:
            if row.user:
                filters = {
                    "reference_type": self.doctype,
                    "reference_name": self.name,
                    "status": "Open",
                    "allocated_to": row.user,
                }
                if not frappe.get_all("ToDo", filters=filters):
                    assign_to.add(
                        {
                            "assign_to": [row.user],
                            "doctype": self.doctype,
                            "name": self.name,
                            "description": "Close this task",
                        }
                    )

    
    def update_serial_number(self):
        if self.imei:
            srn = frappe.db.get_value("Serial No",{"custom_imei1": self.imei},"name")
            if not srn:
                srn = frappe.db.get_value("Serial No",{"custom_imei2": self.imei},"name")
            if srn:
                self.serial_number = srn

    
    def get_dn(self, srn):
        args = {
            "serial_no": "%%%s%%" % srn,
        }

        parent = frappe.db.sql(
            """
            select 
                dni.parent
            from
                `tabDelivery Note Item` dni,
                `tabDelivery Note` as dn
            where
                dn.name = dni.parent
                and dni.serial_no like %(serial_no)s
            order by dn.posting_date, dn.posting_time DESC
            """,
            args,
        )
        return parent
    def update_history(self):
        if self.has_value_changed("status"):
            if not self.has_value_changed("status_reason"):
                self.status_reason = ""
            self.append("status_tracking", {
                "status": self.status,
                "posting_date": today(),
                "posting_time": now(),
                "remark": self.status_reason
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

