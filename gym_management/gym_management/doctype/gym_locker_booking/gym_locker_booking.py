import frappe
from frappe.model.document import Document
from frappe.utils import today


class GymLockerBooking(Document):

    def validate(self):
        self.validate_dates()
        self.validate_locker_availability()
        self.update_status()

    def validate_dates(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            frappe.throw("End Date cannot be before Start Date")

    def validate_locker_availability(self):
        if not (self.locker_id and self.start_date and self.end_date):
            return

        overlapping = frappe.db.exists(
            "Gym Locker Booking",
            {
                "locker_id": self.locker_id,
                "docstatus": 1,
                "start_date": ["<=", self.end_date],
                "end_date": [">=", self.start_date],
                "name": ["!=", self.name]
            }
        )

        if overlapping:
            frappe.throw(
                f"Locker {self.locker_id} is already booked for the selected period."
            )



    def update_status(self):
        today_date = today()

        if self.start_date > today_date:
            self.status = "Draft"
        elif self.start_date <= today_date <= self.end_date:
            self.status = "Active"
            frappe.db.set_value("Gym Locker", self.locker_id, "status", "Occupied")
        else:
            self.status = "Expired"
            frappe.db.set_value("Gym Locker", self.locker_id, "status", "Available")



@frappe.whitelist()
def get_available_lockers(start_date, end_date, docname=None):

    booked = frappe.db.sql("""
        SELECT locker_id
        FROM `tabGym Locker Booking`
        WHERE docstatus = 1
          AND start_date <= %(end_date)s
          AND end_date >= %(start_date)s
          AND (%(docname)s IS NULL OR name != %(docname)s)
    """, {
        "start_date": start_date,
        "end_date": end_date,
        "docname": docname
    }, as_dict=True)

    return [d.locker_id for d in booked]
