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
     },
      refresh(frm) {
        frappe.call({
            method: "frappe.client.get_value",
            args: {
                doctype: "User",
                filters: { "name": frappe.session.user },
                fieldname: ["name"]
            },
            callback: function(r) {
                let current_user = frappe.session.user;

                // Allow only 'Administrator' to print or download
                if (current_user !== "Administrator") {

                    // Hide print button
                    frm.page.hide_icon_group();  

                    // Disable Print action dropdown
                    frm.page.wrapper.find('.menu-btn-group').hide();

                    // Disable print icon
                    frm.page.wrapper.find('.btn-print-print').hide();

                    // Disable PDF icon
                    frm.page.wrapper.find('.btn-download-pdf').hide();
                }
            }
        });
    }
});

