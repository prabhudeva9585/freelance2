# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    package_quantities = fields.Integer(
        'Package Quantities',
        required = True,
        default = 1,
        tracking = True)
    @api.constrains('package_quantities')
    def _constrains_check_package_quantities(self):
        self._check_package_quantities()

    def _check_package_quantities(self):
        for record in self:
            if record.picking_type_code != 'outgoing':
                continue

            if not record.package_quantities:
                raise ValidationError(_('The number of package/sacks is not set for this transfer.'))
            if record.package_quantities < 0:
                raise ValidationError(_('The number of package/sacks cannot be negative.'))

    def button_validate(self):
        self._constrains_check_package_quantities()
        result = super(StockPicking, self).button_validate()
        return result

    def action_confirm(self):
        self._constrains_check_package_quantities()
        result = super(StockPicking, self).action_confirm()
        return result