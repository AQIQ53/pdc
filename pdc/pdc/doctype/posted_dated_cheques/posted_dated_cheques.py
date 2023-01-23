# Copyright (c) 2022, Codes Soft and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class PostedDatedCheques(Document):

	def on_cancel(self):
		self.docstatus=0
		self.status = 'Cancelled'
		self.save(ignore_permissions=True)
		self.docstatus=2
