# -*- coding: utf-8 -*-

from odoo import api, fields, models

class DispatchControl(models.Model):
    _inherit = 'dispatch.control'

    package_quantities = fields.Integer(
        'Package Quantities',
        compute = '_compute_package_quantities',
        store = True,
        tracking = True)
    # NOTE: as we can have multiple pickings assosiated with a single dispatch control,
    #       we must ensure that the results are consistent. This implies that we must
    #       sum all the values in order to have the expected package_quantities of all
    #       the pickings.
    @api.depends('picking_ids', 'picking_ids.package_quantities')
    def _compute_package_quantities(self):
        for record in self:
            record.package_quantities = sum(
                picking.package_quantities
                for picking
                in record.picking_ids)
