import frappe

def execute():
    """Update all Gym Locker records status to Available"""

    # Reload DocType to ensure schema is in sync
    frappe.reload_doc("Gym Management", "doctype", "gym_locker")

    # Correct SQL (table name wrapped in backticks)
    frappe.db.sql("""
        UPDATE `tabGym Locker`
        SET status = 'Available'
        WHERE status IS NULL OR status != 'Available'
    """)

    frappe.db.commit()

    print("All Gym Locker records updated to status = 'Available'")
