from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
import frappe

def setup_custom_fields():
	custom_fields = {
		"Issue": [
			dict(fieldname='serial_number_cu',
				label='Serial Number',
				fieldtype='Data',
				insert_after='subject'
			),
			dict(fieldname='customer_name_cu',
				label='Customer Name',
				fieldtype='Data',
				insert_after='serial_number_cu'
			),
		],
		"Customer": [
			dict(fieldname='cu_mobile_number',
				label='Mobile Number',
				fieldtype='Data',
				insert_after='customer_group'
			),
			dict(fieldname='cu_email',
				label='Email',
				fieldtype='Data',
				insert_after='cu_mobile_number'
			),
		],
		"Sales Order": [
			dict(fieldname='so_status',
				label='Sales Order Status',
				fieldtype='Select',
				options='Pending\nApproved\nCancelled',
				allow_on_submit=True,
				insert_after='delivery_date'
			),
			dict(fieldname='so_address',
				label='Shipping Address',
				fieldtype='Small Text',
				allow_on_submit=True,
				insert_after='so_status'
			),
		],
		"Sales Order Item": [
			dict(fieldname='is_addons',
				label='Is Addons',
				fieldtype='Check',
				insert_after='item_code'
			),
			dict(fieldname='addons_for',
				label='Addons For',
				fieldtype='Data',
				insert_after='is_addons'
			),
		]
	}
	try:
		create_custom_fields(custom_fields)
		frappe.db.commit()
	except:
		print("Exception while createing customfield")