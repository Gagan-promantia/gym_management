// Copyright (c) 2025, gagan and contributors
// For license information, please see license.txt

frappe.query_reports["Fitness Journey Report"] = {
    "filters": [
        {
            fieldname: "gym_member",
            label: "Gym Member",
            fieldtype: "Link",
            options: "Gym Member",
            reqd: 0
        }
    ]
};

