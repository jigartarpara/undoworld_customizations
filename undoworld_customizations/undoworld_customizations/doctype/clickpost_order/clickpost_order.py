# Copyright (c) 2024, Frappe Customizations and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import requests
import json
from frappe.utils.password import get_decrypted_password

CLICKPOST_URL = "https://www.clickpost.in/api/v3/create-order/"

class ClickpostOrder(Document):
    def validate(self):
        payload = {}
        self.set_payload(payload)
        self.payload = json.dumps(payload, indent=4)
        
    def on_submit(self):
        self.create_clickpost_order()
    
    def create_clickpost_order(self):
        headers = {
            "x-api-key": "key_live_6yXxKHeZYNgC6tTQCxEbbOaNme3aIOOM",
            "x-api-secret": "secret_live_3MtPEBQCuUHXQXQ5BNmKkqhTNPJvI6l2",
            "x-api-version": "1.0",
        }
        payload = {}
        self.set_payload(payload)
        params = {
            'username': frappe.db.get_single_value('Clickpost Setup', 'username'),
            'key': get_decrypted_password("Clickpost Setup", "Clickpost Setup", fieldname="key"),
        }
        order_response = requests.post(CLICKPOST_URL, headers=headers,json=payload, params=params)
        self.api_respone = order_response.text
    
    def set_payload(self, payload):
        payload["drop_info"] = self.get_dropinfo()
        payload["pickup_info"] = self.get_pickup_info()
        payload["shipment_details"] = self.get_shipment_details()
    
    def get_dropinfo(self):
        drop_payload =  {}
        if self.drop_location:
            drop_location = frappe.get_doc("Drop Location",self.drop_location)
            drop_payload['drop_lat'] = drop_location.drop_lat
            drop_payload['drop_long'] = drop_location.drop_long
            drop_payload['drop_city'] = drop_location.drop_city
            drop_payload['drop_name'] = drop_location.drop_name
            drop_payload['drop_email'] = drop_location.drop_email
            drop_payload['drop_phone'] = drop_location.drop_phone
            drop_payload['drop_state'] = drop_location.drop_state
            drop_payload['drop_address'] = drop_location.drop_address
            drop_payload['drop_district'] = drop_location.drop_district
            drop_payload['drop_landmark'] = drop_location.drop_landmark
            drop_payload['drop_pincode'] = drop_location.drop_pincode
            drop_payload['drop_country'] = drop_location.drop_country
            drop_payload['drop_address_type'] = drop_location.drop_address_type
        return drop_payload
    
    def get_pickup_info(self):
        pickup_payload =  {}
        pickup_payload['pickup_lat'] = self.pickup_lat
        pickup_payload['pickup_long'] = self.pickup_long
        pickup_payload['pickup_name'] = self.pickup_name
        pickup_payload['pickup_time'] = self.pickup_time
        pickup_payload['pickup_email'] = self.pickup_email
        pickup_payload['pickup_phone'] = self.pickup_phone
        pickup_payload['pickup_state'] = self.pickup_state
        pickup_payload['pickup_address'] = self.pickup_address
        pickup_payload['pickup_district'] = self.pickup_district
        pickup_payload['pickup_landmark'] = self.pickup_landmark
        pickup_payload['pickup_phone_code'] = self.pickup_phone_code
        pickup_payload['pickup_pincode'] = self.pickup_pincode
        pickup_payload['pickup_country'] = self.pickup_country
        pickup_payload['pickup_address_type'] = self.pickup_address_type
        return pickup_payload
    
    def get_shipment_details(self):
        shipment_payload =  {}
        shipment_payload['height'] = self.height
        shipment_payload['length'] = self.length
        shipment_payload['weight'] = self.weight
        shipment_payload['breadth'] = self.breadth
        shipment_payload['order_id'] = self.order_id
        shipment_payload['cod_value'] = self.cod_value
        shipment_payload['order_type'] = self.order_type
        shipment_payload['invoice_date'] = self.invoice_date
        shipment_payload['delivery_type'] = self.delivery_type
        shipment_payload['invoice_value'] = self.invoice_value
        shipment_payload['invoice_number'] = self.invoice_number
        shipment_payload['courier_partner'] = self.courier_partner
        shipment_payload['reference_number'] = self.reference_number
        shipment_payload['account_code'] = self.account_code
        shipment_payload['items'] = self.get_shipment_items()
        return shipment_payload
    
    def get_shipment_items(self):
        payload= []
        for row in self.clickpost_shipment_item:
            item = {}
            item['sku'] =  row.sku
            item['price'] =  row.price
            item['weight'] =  row.weight
            item['hs_code'] =  row.hs_code
            item['quantity'] =  row.quantity
            item['description'] =  row.description
            item['product_id'] =  row.product_id
            item['variant_id'] =  row.variant_id
            item['manufacture_country'] =  row.manufacture_country
            item['manufacture_country_code'] =  row.manufacture_country_code
            item['cat'] =  row.cat
            item['images'] =  row.images
            item['product_url'] =  row.product_url
            item['return_days'] =  row.return_days
            item['exchange_days'] =  row.exchange_days
            item['length'] =  row.length
            item['breadth'] =  row.breadth
            item['height'] =  row.height
            item['brand'] =  row.brand
            item['color'] =  row.color
            item['size'] =  row.size
            item['serial_no'] =  row.serial_no
            item['emei'] =  row.emei
            item['ean'] =  row.ean
            item['sub_category'] =  row.sub_category
            item['return_reason'] =  row.return_reason
            payload.append(item)
        
        return payload
