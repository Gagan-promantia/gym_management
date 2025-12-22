// Copyright (c) 2025, Gagan and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Gym Member", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Gym Member", {
    refresh(frm) {

        // Optional: role-based access
        if (!frm.is_new()) {

            frm.add_custom_button("Update Profile", () => {
                open_update_member_dialog(frm);
            });
        }
    }
});

function open_update_member_dialog(frm) {

    let d = new frappe.ui.Dialog({
        title: "Update Member Details",
        fields: [
            {
                label: "Member Name",
                fieldname: "member_name",
                fieldtype: "Data",
                default: frm.doc.member_name,
                reqd: 1
            },
            {
                label: "Email",
                fieldname: "email",
                fieldtype: "Data",
                default: frm.doc.email
            },
            {
                label: "Phone Number",
                fieldname: "phone_number",
                fieldtype: "Data",
                default: frm.doc.phone_number
            },
            {
                label: "Address",
                fieldname: "address",
                fieldtype: "Small Text",
                default: frm.doc.address
            }
        ],
        primary_action_label: "Update",
        primary_action(values) {

            frappe.call({
                method: "frappe.client.set_value",
                args: {
                    doctype: "Gym Member",
                    name: frm.doc.name,
                    fieldname: {
                        member_name: values.member_name,
                        email: values.email,
                        phone_number: values.phone_number,
                        address: values.address
                    }
                },
                callback(r) {
                    if (!r.exc) {
                        frappe.msgprint("Member updated successfully");
                        d.hide();
                        frm.reload_doc();
                    }
                }
            });
        }
    });

    d.show();
}
