// Copyright (c) 2025, Gagan and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Gym Trainer Subscription", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Gym Trainer Subscription", {
    async plan_type(frm) {
        if (!frm.doc.plan_type) return;

        try {
            const r = await frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Gym Membership Plan",
                    name: frm.doc.plan_type
                }
            });

            if (!r.message) return;

            const plan = r.message;

            // Auto-calc expiry date
            if (frm.doc.start_date) {
                let expiry=frappe.datetime.add_days(frm.doc.start_date,plan.duration)
                frm.set_value("end_date",expiry);
            }

        } catch (err) {
            console.error("Error fetching plan:", err);
        }
    }
});