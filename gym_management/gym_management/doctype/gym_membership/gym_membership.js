// Copyright (c) 2025, gagan and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Gym Membership", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Gym Membership", {
    async gym_member_plan_type(frm) {
        if (!frm.doc.gym_member_plan_type) return;

        try {
            const r = await frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Gym Membership Plan",
                    name: frm.doc.gym_member_plan_type
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
    // },
    // refresh(frm) {
    //     const roles = frappe.user_roles;

    //     // Roles allowed to print
    //     const allowed_roles = ["System Manager", "Gym Admin"];

    //     // If user does NOT have any allowed role → hide print options
    //     const can_print = roles.some(role => allowed_roles.includes(role));

    //     if (!can_print) {
    //         frm.page.hide_menu_item("Print");
    //         frm.page.hide_menu_item("PDF");
    //         frm.disable_print();
    //     }
     }
});

