# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class omegasoft_website_default_fields(models.Model):
#     _name = 'omegasoft_website_default_fields.omegasoft_website_default_fields'
#     _description = 'omegasoft_website_default_fields.omegasoft_website_default_fields'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
