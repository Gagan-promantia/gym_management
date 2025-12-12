# # Copyright (c) 2025, Gagan and contributors
# # For license information, please see license.txt

import frappe
from frappe.model.document import Document


class GymTrainerSubscription(Document):
    def after_insert(self):
        send_realtime_trainer_alert(self)


def send_realtime_trainer_alert(doc):
    # Fetch Gym Member details
    member = frappe.get_doc("Gym Member", doc.gym_member)

    member_name = member.member_name
    contact_number = member.phone_number
    subscription_date = doc.start_date
    trainer = doc.gym_trainer

    # Fetch Trainer Email
    trainer_email = frappe.db.get_value("Gym Trainer", trainer, "email")

    # Prepare Notification Message
    message = {
        "member_name": member_name,
        "contact_number": contact_number,
        "subscription_date": subscription_date,
        "trainer": trainer,
    }

    # Send Realtime Notification
    if trainer_email:
        frappe.publish_realtime(
            event="new_trainer_subscription",
            message=message,
            user=trainer_email
        )
