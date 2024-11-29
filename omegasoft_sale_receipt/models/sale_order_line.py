# -*- coding: utf-8 -*-

from odoo import models, api

class SaleOrderLine(models.Model):
	_inherit = "sale.order.line"

	@api.depends('invoice_lines.move_id.state', 'invoice_lines.quantity')
	def _compute_qty_invoiced(self):
		for line in self:
			qty_invoiced = 0.0
			for invoice_line in line._get_invoice_lines():
				if invoice_line.move_id.state != 'cancel' or invoice_line.move_id.payment_state == 'invoicing_legacy':
					if invoice_line.move_id.move_type in ('out_invoice', 'out_receipt'):
						qty_invoiced += invoice_line.product_uom_id._compute_quantity(invoice_line.quantity, line.product_uom)
					elif invoice_line.move_id.move_type == 'out_refund':
						qty_invoiced -= invoice_line.product_uom_id._compute_quantity(invoice_line.quantity, line.product_uom)
			line.qty_invoiced = qty_invoiced

	def _prepare_invoice_line(self, **optional_values):
		res = super(SaleOrderLine,self)._prepare_invoice_line(**optional_values)
		if self.user_has_groups('account.group_sale_receipts') and self._context.get('create_receipt'):
			res['tax_ids'] = [(5,0,0)]
		return res