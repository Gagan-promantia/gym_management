# Copyright (c) 2025, Gagan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class GymTrainer(Document):
	def autoname(self):
		self.name=frappe.model.naming.make_autoname("GYM-Coach-.#####")
		self.trainer_id=self.name