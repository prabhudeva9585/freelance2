# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
	_inherit = "sale.order"

	receipt_count = fields.Integer(string='Invoice Count', compute='_get_receipts')
	receipt_ids = fields.Many2many('account.move', string='Invoices', compute='_get_receipts')
	active_receips = fields.Boolean(compute='_compute_active_receips', string='Active Receips')
	
	@api.depends('receipt_ids', 'receipt_ids.state')
	def _compute_active_receips(self):
		for rec in self:
			if rec.receipt_ids and all(receipt.state == 'cancel' for receipt in rec.receipt_ids):
				rec.active_receips = True
			else:
				rec.active_receips = False

	@api.depends('order_line.invoice_lines')
	def _get_receipts(self):
		for order in self:
			receipts = order.order_line.invoice_lines.move_id.filtered(lambda r: r.move_type == 'out_receipt')
			order.receipt_ids = receipts
			order.receipt_count = len(receipts)

	def create_receipt(self):
		self.with_context(create_receipt=True)._create_invoices()
		return self.action_view_receipts()

	def _prepare_invoice(self):
		vals = super(SaleOrder, self)._prepare_invoice()
		if self.user_has_groups('account.group_sale_receipts') and self._context.get('create_receipt'):
			vals['move_type'] = 'out_receipt'
		return vals

	def action_view_receipts(self):
		receipts = self.mapped('receipt_ids')
		action = self.env['ir.actions.actions']._for_xml_id('account.action_move_out_receipt_type')
		if len(receipts) > 1:
			action['domain'] = [('id', 'in', receipts.ids)]
		elif len(receipts) == 1:
			form_view = [(self.env.ref('account.view_move_form').id, 'form')]
			if 'views' in action:
				action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
			else:
				action['views'] = form_view
			action['res_id'] = receipts.id
		else:
			action = {'type': 'ir.actions.act_window_close'}

		context = {
			'default_move_type': 'out_receipt',
		}
		if len(self) == 1:
			context.update({
				'default_partner_id': self.partner_id.id,
				'default_partner_shipping_id': self.partner_shipping_id.id,
				'default_invoice_payment_term_id': self.payment_term_id.id or self.partner_id.property_payment_term_id.id or self.env['account.move'].default_get(['invoice_payment_term_id']).get('invoice_payment_term_id'),
				'default_invoice_origin': self.name,
			})
		action['context'] = context
		return action