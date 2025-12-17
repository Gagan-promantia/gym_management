// Copyright (c) 2025, Gagan and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Gym Trainer Subscription", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Gym Trainer Subscriptions", {
    async gym_member_plan_type(frm) {

        try {
            const r = await frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Gym Membership Plan",
                }
            });

            if (!r.message) return;

            const plan = r.message;

            // Set cost
            frm.set_value("amount", plan.amount);

            // Auto-calc expiry date
            if (frm.doc.start_date) {
                let expiry=frappe.datetime.add_days(frm.doc.start_date,plan.duration)
                frm.set_value("expiry_date",expiry);
            }

        } catch (err) {
            console.error("Error fetching plan:", err);
        }
     }
    });