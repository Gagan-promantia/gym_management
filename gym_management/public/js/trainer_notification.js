frappe.ready(function () {
    console.log("trainer_notification.js loaded");
    frappe.msgprint("Trainer notification JS loaded (debug)");
});

frappe.realtime.on("new_trainer_subscription", function(data) {
    frappe.msgprint(`
        <b>New Trainer Subscription</b><br><br>
        <b>Member:</b> ${data.member_name}<br>
        <b>Trainer:</b> ${data.trainer}<br>
        <b>Subscription Date:</b> ${data.subscription_date}<br>
        <b>Contact:</b> ${data.contact_number}<br>
    `);
});


