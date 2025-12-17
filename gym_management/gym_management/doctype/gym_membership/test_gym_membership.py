import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import today, add_days


class TestGymMembership(FrappeTestCase):

    def setUp(self):
        # Create Gym Member (valid phone with country code)
        self.member = frappe.get_doc({
            "doctype": "Gym Member",
            "member_name": "Test Member",
            "phone_number": "+919876543210",
            "email": "testmember@example.com"
        }).insert(ignore_permissions=True)

        # Create Active Gym Membership
        self.membership = frappe.get_doc({
            "doctype": "Gym Membership",
            "gym_member": self.member.name,
            "member_mail_id": "testmember@example.com",
            "start_date": add_days(today(), -5),
            "expiry_date": add_days(today(), 5),
            "status": "Active"
        }).insert(ignore_permissions=True)


    # TEST 2: auto_expire_gym_memberships
   
    def test_auto_expire_gym_membership(self):
        # Force expiry
        self.membership.expiry_date = add_days(today(), -1)
        self.membership.status = "Active"
        self.membership.save(ignore_permissions=True)

        # Call scheduled method
        from gym_management.gym_management.doctype.gym_membership.gym_membership import auto_expire_gym_memberships
        auto_expire_gym_memberships()

        # Reload & check
        self.membership.reload()

        self.assertEqual(
            self.membership.status,
            "Expired",
            "Membership should be auto-expired"
        )
