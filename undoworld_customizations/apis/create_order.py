import frappe
import erpnext
from frappe.utils import nowdate, add_days
from erpnext.manufacturing.doctype.work_order.work_order import get_default_warehouse


@frappe.whitelist(allow_guest=True, methods="POST")
def endpoint(mobile_number, customer_name, address,  item_code, rate):
	default_warehouses = get_default_warehouse()
	do_not_save = False
	do_not_submit = False
	customer = frappe.db.get_value("Customer", {"cu_mobile_number": mobile_number}, "name")
	if not customer:
		customer_doc = frappe.new_doc("Customer")
		customer_doc.customer_name = customer_name
		customer_doc.customer_type = "Individual"
		customer_doc.customer_group = "All Customer Groups"
		customer_doc.territory = "All Territories"
		customer_doc.insert(ignore_permissions=True)
		customer =  customer_doc.name
		
	so = make_sales_order(
        company=erpnext.get_default_company(),
        transaction_date=nowdate(),
        customer=customer,
        item_code=item_code,
        warehouse=default_warehouses,
        qty=1,
        rate=rate,
        do_not_save=do_not_save,
        do_not_submit=do_not_submit,
		address = address
    )
	return so.name

def make_sales_order(**args):
	so = frappe.new_doc("Sales Order")
	args = frappe._dict(args)
	if args.transaction_date:
		so.transaction_date = args.transaction_date

	so.set_warehouse = ""  # no need to test set_warehouse permission since it only affects the client
	so.company = args.company 
	so.customer = args.customer 
	so.currency = "INR"
	so.po_no = args.po_no or ""
	so.so_address = args.address
	if args.selling_price_list:
		so.selling_price_list = args.selling_price_list

	if "warehouse" not in args:
		args.warehouse = "_Test Warehouse - _TC"

	if args.item_list:
		for item in args.item_list:
			so.append("items", item)

	else:
		so.append(
			"items",
			{
				"item_code": args.item or args.item_code or "_Test Item",
				# "warehouse": args.warehouse,
				"qty": args.qty or 1,
				"uom": args.uom or None,
				"price_list_rate": args.price_list_rate or None,
				"discount_percentage": args.discount_percentage or None,
				"rate": args.rate or (None if args.price_list_rate else 100),
				"against_blanket_order": args.against_blanket_order,
			},
		)

	so.delivery_date = add_days(so.transaction_date, 10)

	if not args.do_not_save:
		so.insert(ignore_permissions=True)
		if not args.do_not_submit:
			so.submit()
		else:
			so.payment_schedule = []
	else:
		so.payment_schedule = []

	return so