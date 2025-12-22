# Copyright (c) 2025, Gagan and Contributors
# See license.txt

import frappe
import unittest
from frappe.utils import today, add_days


class TestGymLockerBooking(unittest.TestCase):

    def setUp(self):
        frappe.set_user("Administrator")

        # Create Gym Locker with VALID status
        self.locker = frappe.get_doc({
            "doctype": "Gym Locker",
            "locker_code": "LOCK-TEST-001",
            "status": "Available",
            "is_active": 1
        }).insert(ignore_permissions=True)

        self.start_date = add_days(today(), -1)
        self.end_date = add_days(today(), 5)

    def tearDown(self):
        frappe.db.rollback()

    # TEST 1: Overlapping booking should fail
    def test_overlapping_locker_booking_not_allowed(self):
        booking1 = frappe.get_doc({
            "doctype": "Gym Locker Booking",
            "locker_id": self.locker.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": "Draft"
        }).insert(ignore_permissions=True)

        booking1.submit()

        booking2 = frappe.get_doc({
            "doctype": "Gym Locker Booking",
            "locker_id": self.locker.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": "Draft"
        })

        self.assertRaises(
            frappe.ValidationError,
            booking2.insert,
            ignore_permissions=True
        )

    # TEST 2: Active booking updates locker status
    
    def test_active_booking_updates_locker_status(self):
        booking = frappe.get_doc({
            "doctype": "Gym Locker Booking",
            "locker_id": self.locker.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": "Draft"
        }).insert(ignore_permissions=True)

        booking.submit()
        booking.reload()

        locker = frappe.get_doc("Gym Locker", self.locker.name)

        self.assertEqual(booking.status, "Active")
        self.assertEqual(locker.status, "Occupied")
