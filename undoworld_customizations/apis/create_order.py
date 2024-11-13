import frappe
import erpnext
from frappe.utils import nowdate, add_days, flt
from erpnext.manufacturing.doctype.work_order.work_order import get_default_warehouse



@frappe.whitelist(allow_guest=True, methods="POST")
def endpoint(mobile_number, customer_name, address,  item_codes,discount = None, gst=0, shipping_charge=0):
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
        customer_doc.cu_mobile_number = mobile_number
        customer_doc.insert(ignore_permissions=True)
        customer =  customer_doc.name
    else:
        frappe.db.set_value("Customer", customer, "customer_name", customer_name)
    
    address_doc = create_addres(address, customer)
        
    so = make_sales_order(
        company=erpnext.get_default_company(),
        transaction_date=nowdate(),
        customer=customer,
        item_codes=item_codes,
        warehouse=default_warehouses,
        qty=1,
        do_not_save=do_not_save,
        do_not_submit=do_not_submit,
        address = address_doc,
        gst=gst,
        shipping_charge=shipping_charge,
        discount= discount
    )
    return so.name
def create_addres(address, customer):
    address_doc = frappe.new_doc("Address")
    address_doc.address_type= "Shipping"
    address_doc.address_title = customer
    address_doc.address_line1 = address.get("address_line1")
    address_doc.address_line2 = address.get("address_line2")
    address_doc.city = address.get("city")
    address_doc.state = address.get("state")
    address_doc.country = address.get("country")
    address_doc.pincode = address.get("pincode")
    
    address_doc.append("links",{
        "link_doctype": "Customer",
        "link_name": customer,
    })
    address_doc.insert(ignore_permissions=True)
    return address_doc.name


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
    so.shipping_address_name = args.address
    so.customer_address = args.address
    if args.selling_price_list:
        so.selling_price_list = args.selling_price_list

    if "warehouse" not in args:
        args.warehouse = "_Test Warehouse - _TC"

    for row in args.item_codes:
        so.append(
            "items",
            {
                "item_code": row.get("item_code") ,
                "margin_type": "",
                "qty": row.get("qty") ,
                "rate": row.get("rate"),
            },
        )
    if args.gst:
        so.append("taxes", {
            "charge_type": "On Net Total",
            "account_head": frappe.db.get_single_value("OMS Setup", "gst_account"),
            "rate": "18",
            "description": "GST"
        })
    if args.shipping_charge:
        so.append("taxes", {
            "charge_type": "Actual",
            "account_head": frappe.db.get_single_value("OMS Setup", "shipping_account"),
            "tax_amount": args.shipping_charge,
            "description": "Shipping"
        })
    
    if args.discount:
        if args.discount.get("discount_type") == "percentage":
            so.additional_discount_percentage = flt(args.discount.get("discount"))
            so.apply_discount_on = "Net Total"

        if args.discount.get("discount_type") == "amount":
            so.discount_amount = flt(args.discount.get("discount"))
            so.apply_discount_on = "Net Total"

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