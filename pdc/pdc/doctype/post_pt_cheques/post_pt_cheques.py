# Copyright (c) 2022, Codes Soft and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PostPTCheques(Document):
	pass

	def on_submit(self):
		pe = ""
		for d in self.details:
			if not d.bank_account:
				frappe.throw("Bank Account required on row {}".format(str(d.idx)))
			check = frappe.db.get_value("Payment Entry", {"posted_dated_cheques": d.posted_dated_cheques, "docstatus": ("!=", 2)}, "name")
			if not check:
				pdc = frappe.get_doc("Posted Dated Cheques", d.posted_dated_cheques)
				doc = frappe.new_doc("Payment Entry")
				doc.company = d.company
				doc.cost_center = d.cost_center
				doc.department = d.department
				doc.project = d.project
				doc.mode_of_payment = d.mode_of_payment
				doc.payment_type = d.payment_type
				doc.reference_no = d.reference_no
				doc.reference_date = d.reference_date
				doc.party_type = d.party_type
				doc.party = d.party
				doc.paid_amount = d.amount
				doc.received_amount = pdc.base_amount
				doc.source_exchange_rate = 1
				doc.target_exchange_rate = pdc.target_exchange_rate
				doc.posted_dated_cheques = d.posted_dated_cheques
				# currency = frappe.db.get_value("Company", d.company, "default_currency")
				paid_from_account_currency = pdc.company_currency
				paid_to_account_currency = pdc.currency
				doc.paid_from_account_currency = paid_from_account_currency
				doc.paid_to_account_currency = paid_to_account_currency
				doc.remarks = pdc.additional_notes
				account = frappe.db.get_value("Party Account", {"company": d.company, "parent": d.party}, "account")
				if d.party_type == "Customer":
					if not account:
						account = frappe.db.get_value("Company", d.company, "default_receivable_account")
					doc.paid_to = d.bank_account
					doc.paid_from = account
				else:
					if not account:
						account = frappe.db.get_value("Company", d.company, "default_payable_account")
					doc.paid_from = d.bank_account
					doc.paid_to = account
				# doc.set_missing_values()
				doc.save(ignore_permissions=True)
				pe+= doc.name+", "
		if pe:
			frappe.msgprint("Payment Entries created "+pe)

@frappe.whitelist()
def get_posted_dated_cheques(company=None, cost_center=None, department=None, from_date=None, to_date=None):
	cond = ""
	if company:
		cond += " and company = '{}'".format(company)
	if cost_center:
		cond += " and cost_center = '{}'".format(cost_center)
	if department:
		cond += " and department = '{}'".format(department)
	if department:
		cond += " and department = '{}'".format(department)
	if from_date:
		cond += " and posting_date >= '{}'".format(from_date)
	if to_date:
		cond += " and posting_date <= '{}'".format(to_date)

	data = frappe.db.sql("""select company, cost_center, department, project, mode_of_payment, posting_date, 
		payment_type, reference_no, reference_date, party_type, party, amount, name as posted_dated_cheques,
		company_currency,currency
		from `tabPosted Dated Cheques` where docstatus = 1 and status = 'Pending' {}""".format(cond), as_dict=1)
	return data