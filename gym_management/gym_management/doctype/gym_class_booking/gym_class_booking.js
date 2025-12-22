// Copyright (c) 2025, Gagan and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Gym class Booking", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Gym class Booking", {

    refresh(frm) {
        // Make status read-only for non-admin users
        if (!frappe.user_roles.includes("System Manager") &&
            !frappe.user_roles.includes("Gym Admin")) {
            frm.set_df_property("booking_status", "read_only", 1);
        }
    },

    start_time(frm) {
        validate_time(frm);
    },

    end_time(frm) {
        validate_time(frm);
    },

    class_date(frm) {
        // Auto mark upcoming classes as Scheduled
        if (frm.doc.class_date && frm.doc.class_date >= frappe.datetime.get_today()) {
            frm.set_value("booking_status", "Scheduled");
        }
    }
});


function validate_time(frm) {

    if (!frm.doc.start_time || !frm.doc.end_time) return;

    if (frm.doc.end_time <= frm.doc.start_time) {
        frappe.msgprint({
            title: "Invalid Time",
            message: "End Time must be after Start Time",
            indicator: "red"
        });
        frm.set_value("end_time", "");
    }
}


