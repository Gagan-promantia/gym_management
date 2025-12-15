# Copyright (c) 2025, gagan and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CardioMachineBooking(Document):
	# def validate(self):
    #     self.validate_machine_slot()

    # def validate_machine_slot(self):
    #     """Prevent booking the same machine for the same date & slot."""
    #     if not (self.cardio_machine and self.date and self.time_slot):
    #         return

    #     existing = frappe.db.exists(
    #         "Cardio Machine Booking",
    #         {
    #             "cardio_machine": self.cardio_machine,
    #             "date": self.date,
    #             "time_slot": self.time_slot,
    #             "name": ("!=", self.name)
    #         }
    #     )

    #     if existing:
    #         frappe.throw(
    #             f"Cardio Machine <b>{self.cardio_machine}</b> is already booked for this time slot."
    #         )
    pass