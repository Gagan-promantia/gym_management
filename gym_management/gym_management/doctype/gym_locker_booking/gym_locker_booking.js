// // // Copyright (c) 2025, Gagan and contributors
// // // For license information, please see license.txt

// // // frappe.ui.form.on("Gym Locker Booking", {
// // // 	refresh(frm) {

// // // 	},
// // // });

frappe.ui.form.on("Gym Locker Booking", {
    refresh(frm) {
        apply_locker_filter(frm);
    },
    start_date(frm) {
        apply_locker_filter(frm);
    },
    end_date(frm) {
        apply_locker_filter(frm);
    }
});

function apply_locker_filter(frm) {

    //  ALWAYS hide occupied lockers
    frm.set_query("locker_id", () => {
        return {
            filters: {
                status: "Available"
            }
        };
    });

    //  If dates selected → apply advanced overlap logic
    if (!frm.doc.start_date || !frm.doc.end_date) return;

    frappe.call({
        method: "gym_management.gym_management.doctype.gym_locker_booking.gym_locker_booking.get_available_lockers",
        args: {
            start_date: frm.doc.start_date,
            end_date: frm.doc.end_date,
            docname: frm.doc.name
        },
        callback(r) {
            if (!r.message) return;

            frm.set_query("locker_id", () => {
                return {
                    filters: [
                        ["Gym Locker", "name", "not in", r.message],
                        ["Gym Locker", "status", "=", "Available"]
                    ]
                };
            });
        }
    });
}
// frappe.ui.form.on("Gym Locker Booking", {
//     refresh(frm) {
//         filter_available_lockers(frm);
//     },
//     start_date(frm) {
//         filter_available_lockers(frm);
//     },
//     end_date(frm) {
//         filter_available_lockers(frm);
//     }
// });

// function filter_available_lockers(frm) {

//     frm.set_query("locker_id", () => {
//         return {
//             filters: {
//                 status: "Available"
//             }
//         };
//     });
// }
