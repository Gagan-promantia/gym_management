# # Copyright (c) 2025, Gagan and contributors
# # For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today


class GymTrainerSubscription(Document):
    def after_insert(doc, method):
        trainer_user = frappe.db.get_value("Gym Trainer", doc.trainer, "trainer_user")

        if not trainer_user:
            frappe.throw(f"Trainer '{doc.trainer}' does not have a linked User account!")

        # 1️⃣ Real-time popup notification
        frappe.publish_realtime(
            event="trainer_subscription_alert",
            message={
                "member": doc.member,
                "plan": doc.plan_name,
                "start_date": str(doc.subscription_date),
                "status": doc.status
            },
            user=trainer_user
        )

        message = f"""
        Member: {doc.member}<br>
        Plan: {doc.plan_name}<br>
        Subscription Date: {doc.subscription_date}<br>
        Status: {doc.status}
        """

        notification = frappe.get_doc({
            "doctype": "Notification Log",
            "subject": "New Subscription",
            "email_content": message,
            "for_user": trainer_user,
            "document_type": doc.doctype,
            "document_name": doc.name,
            "type": "Alert",
            "read": 0
        })

        notification.insert(ignore_permissions=True)
        frappe.db.commit()

    def validate(self):
        validate_duplicate_subscription(self)
        validate_dates(self)
        update_status(self)
        
def update_status(self):
    if not self.start_date or not self.end_date:
        self.status = "Pending"
        return

    start = frappe.utils.getdate(self.start_date)
    end = frappe.utils.getdate(self.end_date)
    today = frappe.utils.getdate()

    if today < start:
        self.status = "Upcoming"
    elif start <= today <= end:
        self.status = "Active"
    else:
        self.status = "Expired"




def validate_dates(self):
    if not self.start_date or not self.end_date:
        # Skip validation if dates are missing
        return  

    start = getdate(self.start_date)
    end = getdate(self.end_date)

    if end < start:
        frappe.throw("End Date cannot be earlier than Start Date.")

    # For new records end_date must not be in the past
    if self.is_new() and end < getdate(today()):
        frappe.throw("End Date cannot be in the past for a new subscription.")


def validate_duplicate_subscription(self):
    #checking if memeber alreday subscribed to  same trainer
    existing=frappe.db.exists(
        "Gym Trainer Subscription",
            {
            "gym_member":self.gym_member,
            "gym_trainer":self.gym_trainer
        }
    )

    if existing and existing != self.name:
            member_name = frappe.db.get_value("Gym Member", self.gym_member, "member_name")
            trainer_name = frappe.db.get_value("Gym Trainer", self.gym_trainer, "trainer_name")

            frappe.throw(
                f"Member <b>{member_name}</b> is already subscribed to Trainer <b>{trainer_name}</b>. "
                "Duplicate subscriptions are not allowed."
            )


