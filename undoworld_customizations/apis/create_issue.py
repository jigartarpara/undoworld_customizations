import frappe
from frappe.utils.file_manager import save_file

#fname, content, dt, dn, folder=None, decode=False, is_private=0, df=None

@frappe.whitelist(allow_guest=True,methods="POST")
def endpoint(**kwargs):
    body = form_body()
    ticket = frappe.get_doc(
        {
            "doctype": "Support Ticket",
            "subject": kwargs.get("issue_faced"),
           
            "serial_number": kwargs.get("serial_number"),
            
            
            "customer_name": kwargs.get("customer_name"),
            "mobile_number": kwargs.get("mobile_number"),
            "email": kwargs.get("email"),
            "invoice_date": kwargs.get("invoice_date"),
            "order_id": kwargs.get("order_id"),
            "platform": kwargs.get("platform"),
            "description": kwargs.get("description"),
            "brand": kwargs.get("brand"),
            "device_model": kwargs.get("device_model"),
            "issue_faced": kwargs.get("issue_faced"),
            "sub_issue": kwargs.get("sub_issue"),
            "house_number": kwargs.get("house_number"),
            "street_line_1": kwargs.get("street_line_1"),
            "street_line_2": kwargs.get("street_line_2"),
            "state": kwargs.get("state"),
            "pincode": kwargs.get("pincode"),
            "landmark": kwargs.get("landmark"),
        }
    )

    ticket.insert(ignore_permissions=True)
    frappe.db.commit()
    
    audio_recording = body.get("audio_recording")
    if audio_recording:
        audio_file = save_file(
            audio_recording.filename,
            audio_recording.stream.read(), 
            "Support Ticket", 
            ticket.name, 
            df= "audio_recording"
        )
        ticket.audio_recording = audio_file.file_url
    
    video_recording = body.get("video_recording")
    if video_recording:
        video_file = save_file(
            video_recording.filename,
            video_recording.stream.read(), 
            "Support Ticket", 
            ticket.name, 
            df= "video_recording"
        )
        ticket.video_recording = video_file.file_url
    
    img1 = body.get("img1")
    if img1:
        video_file = save_file(
            img1.filename,
            img1.stream.read(), 
            "Support Ticket", 
            ticket.name, 
        )
        ticket.append("support_image_table",{"image_url" : video_file.file_url})
    
    img2 = body.get("img2")
    if img2:
        video_file = save_file(
            img2.filename,
            img2.stream.read(), 
            "Support Ticket", 
            ticket.name, 
        )
        ticket.append("support_image_table",{"image_url" : video_file.file_url})
    
    img3 = body.get("img3")
    if img3:
        video_file = save_file(
            img3.filename,
            img3.stream.read(), 
            "Support Ticket", 
            ticket.name, 
        )
        ticket.append("support_image_table",{"image_url" : video_file.file_url})
    
    
    
    ticket.save()
    return ticket.name

def form_body():
    """Returns a dictionary representing the form body parameters including files."""
    body = frappe.request.form.copy()

    # Add files directly as well. Iterating yields the file parameter names. Indexing with the
    # name yields a werkzeug.datastructures.FileStorage which we use as the value
    for f in frappe.request.files:
        body[f] = frappe.request.files[f]

    return body