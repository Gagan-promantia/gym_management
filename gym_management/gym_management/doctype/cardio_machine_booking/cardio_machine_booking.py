# Copyright (c) 2025, gagan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class CardioMachineBooking(Document):

    def validate(self):
        self.validate_double_booking()

    def validate_double_booking(self):
        """
        Prevent double booking of the same cardio machine
        for the same date and time slot
        """

        if not (self.cardio_machine and self.booking_date and self.time_slot):
            return

        existing_booking = frappe.db.exists(
            "Cardio Machine Booking",
            {
                "cardio_machine": self.cardio_machine,
                "booking_date": self.booking_date,
                "time_slot": self.time_slot,
                "name": ["!=", self.name]  
            }
        )

        if existing_booking:
            frappe.throw(
                f"{self.cardio_machine} is already booked on "
                f"{self.booking_date} during {self.time_slot}."
            )
