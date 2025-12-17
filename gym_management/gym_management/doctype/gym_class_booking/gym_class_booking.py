# Copyright (c) 2025, Gagan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, add_days, today

class GymclassBooking(Document):

    def on_submit(self):
        self.update_class_status()

    def update_class_status(self):
        """
        If class_date is before today,
        automatically mark booking_status as Completed
        """

        if not self.class_date:
            return

        class_date = getdate(self.class_date)
        today_date = getdate(today())

        if class_date < today_date:
            self.booking_status = "Completed"

def send_weekly_class_summary():
    end_date = today()
    start_date = add_days(end_date, -7)

    # Fetch attended classes
    bookings = frappe.get_all(
        "Gym class Booking",
        filters={
            "class_date": ["between", [start_date, end_date]],
            "booking_status": "Completed"
        },
        fields=["member", "class_type", "class_date"],
        ignore_permissions=True
    )

    if not bookings:
        return

    #  Group by member
    member_map = {}
    for b in bookings:
        member_map.setdefault(b.member, []).append(b)

    #  Send email to each member
    for member, classes in member_map.items():
        member_doc = frappe.get_doc("Gym Member", member)

        rows = ""
        for c in classes:
            rows += f"""
                <tr>
                    <td>{c.class_type}</td>
                    <td>{c.class_date}</td>
                </tr>
            """

        message = f"""
        <h3>Weekly Class Summary</h3>
        <p>Hello {member_doc.member_name},</p>
        <table border="1" cellpadding="6">
            <tr>
                <th>Class</th>
                <th>Date</th>
            </tr>
            {rows}
        </table>
        """

        frappe.sendmail(
            recipients=[member_doc.email],
            subject="Your Weekly Gym Class Summary",
            message=message
        )



