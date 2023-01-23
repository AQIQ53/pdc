# Copyright (c) 2022, Codes Soft and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class PostedDatedCheques(Document):

	def on_cancel(self):
		frappe.db.set_value('Posted Dated Cheques', self.name, 'status', 'Cancelled')
