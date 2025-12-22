# Copyright (c) 2025, gagan and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    filters = filters or {}   # ✅ important fix

    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)

    return columns, data, None, chart


def get_columns():
    return [
        {"label": "Member", "fieldname": "gym_member", "fieldtype": "Link", "options": "Gym Member", "width": 200},
        {"label": "Date", "fieldname": "record_date", "fieldtype": "Date", "width": 120},
        {"label": "Weight (kg)", "fieldname": "weight_kg", "fieldtype": "Float", "width": 120},
        {"label": "Calories", "fieldname": "calories", "fieldtype": "Int", "width": 120},
        {"label":"Workouts","fieldname":"work_out","fieldtype":"select","width":120}
    ]



def get_data(filters):
    conditions = ""
    values = {}

    if filters.get("gym_member"):
        conditions += " AND gym_member = %(gym_member)s"
        values["gym_member"] = filters.get("gym_member")

    if filters.get("month"):
        conditions += " AND MONTH(record_date) = %(month)s"
        values["month"] = get_month_number(filters.get("month"))  # fixed

    return frappe.db.sql(f"""
        SELECT 
            gym_member,
            record_date,
            weight_kg,
            calories,
            work_out
        FROM `tabFitness Journey`
        WHERE 1=1 {conditions}
        ORDER BY record_date ASC
    """, values=values, as_dict=True)


def get_chart(data):
    labels = []
    weight_values = []
    calorie_values = []
    work_out_value=[]
    for row in data:
        labels.append(row["record_date"])
        weight_values.append(row["weight_kg"])
        calorie_values.append(row["calories"])
        work_out_value.append(row["work_out"])

    return {
        "data": {
            "labels": labels,
            "datasets": [
                {"name": "Weight", "values": weight_values},
                {"name": "Calories", "values": calorie_values},
                {"name":"Workout","values":work_out_value}
            ]
        },
        "type": "line"
    }


def get_month_number(month_name):
    months = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }
    return months.get(month_name)
