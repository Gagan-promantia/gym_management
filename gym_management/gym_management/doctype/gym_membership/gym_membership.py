# Copyright (c) 2025, gagan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today

class GymMembership(Document):
    def validate(self):
        update_status(self)

    

def auto_expire_gym_memberships():
    today_date = today()

    expired_memberships = frappe.get_all(
        "Gym Membership",
        filters={
            "status": "Active",
            "expiry_date": ["<=", today_date]
        },
        fields=["name", "gym_member", "member_mail_id"]
    )

    for membership in expired_memberships:
        doc = frappe.get_doc("Gym Membership", membership.name)
        doc.status = "Expired"
        doc.save(ignore_permissions=True)

        # Email notification
        if membership.get("member_mail_id"):
            frappe.sendmail(
                recipients=[membership.member_mail_id],
                subject="Gym Membership Expired",
                message=f"""
                Dear {membership.gym_member},<br><br>
                Your gym membership has expired as of {today_date}.<br>
                Please renew your membership to continue enjoying our services.<br><br>
                Best regards,<br>
                Gym Management Team
                """
            )

        #  Audit log
        frappe.log_error(
            title="Gym Membership Auto Expired",
            message=f"Membership {membership.name} expired automatically."
        )

    frappe.db.commit()

def update_status(self):
    if not self.start_date or not self.expiry_date:
        self.status = "Pending"
        return

    start = frappe.utils.getdate(self.start_date)
    end = frappe.utils.getdate(self.expiry_date)
    today = frappe.utils.getdate()

    if today < start:
        self.status = "Upcoming"
    elif start <= today <= end:
        self.status = "Active"
    else:
        self.status = "Expired"

@frappe.whitelist()
def get_print_context(**kwargs):
    if frappe.session.user != "Administrator":
        frappe.throw("You are not permitted to print or download this document.")