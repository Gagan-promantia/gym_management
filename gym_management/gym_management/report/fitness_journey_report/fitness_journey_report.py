# Copyright (c) 2025, gagan and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart(data)

	return columns, data, None,chart

def get_columns():
	return [
        {"label": "Member", "fieldname": "gym_member", "fieldtype": "Link", "options": "Gym Member", "width": 200},
        {"label": "Date", "fieldname": "record_date", "fieldtype": "Date", "width": 120},
        {"label": "Weight (kg)", "fieldname": "weight_kg", "fieldtype": "Float", "width": 120},
        {"label": "Calories", "fieldname": "calories", "fieldtype": "Int", "width": 120},
    ]

def get_data(filters):
    conditions = ""
    values = {}

    if filters.get("gym_member"):
        conditions += " AND gym_member = %(gym_member)s"
        values["gym_member"] = filters.get("gym_member")

    return frappe.db.sql(f"""
        SELECT 
            gym_member,
            record_date,
            weight_kg,
            calories
        FROM `tabFitness Journey`
        WHERE 1=1 {conditions}
        ORDER BY record_date ASC
    """, values=values, as_dict=True)

def get_chart(data):
    labels = []
    weight_values = []
    calorie_values = []

    for row in data:
        labels.append(row["record_date"])
        weight_values.append(row["weight_kg"])
        calorie_values.append(row["calories"])

    return {
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "name": "Weight",
                    "values": weight_values
                },
                {
                    "name": "Calories",
                    "values": calorie_values
                }
            ]
        },
        "type": "line",
        "colors": ["#007bff", "#ff4757"],
        "axisOptions": {
            "y": {"label": "Weight (kg)", "min": 40, "max": 120},
            "y2": {"label": "Calories", "min": 1000, "max": 4000}
    }
	}