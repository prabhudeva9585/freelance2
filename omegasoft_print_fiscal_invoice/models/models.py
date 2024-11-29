# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    @api.depends('invoice_line_ids')
    def _compute_total_discount(self):
        for record in self:
            total_discount = 0
            for line in record.invoice_line_ids:
                total_discount += line.price_unit * line.quantity * line.discount / 100
            return total_discount

     # Funcion para calcular los totales segun las lineas de factura
    def get_account_move_line_totals(self):
        total_exent = 0.0
        total_tax = 0.0
        total_iva = 0.0
        total_discount = 0.0
        for linea in self.invoice_line_ids:
            if linea.tax_ids.fiscal_tax_type == 'exempt':
                total_exent += linea.credit
                if linea.discount:
                    discount = (linea.credit * linea.discount) / 100
                    total_discount += discount
            else:
                total_tax += linea.credit
                if linea.discount:
                    discount = (linea.credit * linea.discount) / 100
                    total_discount += discount
                
        record_move_line = self.env['account.move.line'].search([('move_id', '=', self.id),('display_type', '=', 'tax')])
        if record_move_line:
            for iva in record_move_line:
                total_iva = total_iva + iva.credit
        return {
            'total_exent': round(total_exent,2),
            'total_tax': round(total_tax,2),
            'total_iva': round(total_iva,2),
            'total_discount': round(total_discount,2)
        }

    def get_date_order(self):
        order = self.env['sale.order'].search([('name','=', self.invoice_origin)])

        date_order = {
            'date_order': order.date_order.strftime('%d/%m/%Y') if order.date_order else ''
        }

        return date_order

    def get_date_today(self):
        today = date.today()
        return today

class FiscalInvoiceReport(models.AbstractModel):
    _name = 'report.omegasoft_print_fiscal_invoice.fi_report'
    _description = 'Fiscal Invoice FI Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.move'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'account.move',
            'docs': docs,
        }
