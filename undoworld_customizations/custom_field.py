from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
import frappe

def setup_custom_fields():
	custom_fields = {
		"Issue": [
			dict(fieldname='serial_number_cu',
				label='Serial Number',
				fieldtype='Data',
				insert_after='subject'
			)
		],
	}
	try:
		create_custom_fields(custom_fields)
		frappe.db.commit()
	except:
		print("Exception while createing customfield")